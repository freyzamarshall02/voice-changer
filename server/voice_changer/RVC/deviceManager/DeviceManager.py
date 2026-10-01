import torch
import onnxruntime


class DeviceManager(object):
    _instance = None
    forceTensor: bool = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.gpu_num = torch.cuda.device_count()
        self.mps_enabled: bool = (
            getattr(torch.backends, "mps", None) is not None
            and torch.backends.mps.is_available()
        )

    def getDevice(self, id: int):
        if id < 0 or self.gpu_num == 0:
            if self.mps_enabled is False:
                dev = torch.device("cpu")
            else:
                dev = torch.device("mps")
        else:
            if id < self.gpu_num:
                dev = torch.device("cuda", index=id)
            else:
                print("[Voice Changer] device detection error, fallback to cpu")
                dev = torch.device("cpu")
        return dev

    def getOnnxExecutionProvider(self, gpu: int):
        availableProviders = onnxruntime.get_available_providers()
        devNum = torch.cuda.device_count()
        if gpu >= 0 and "CUDAExecutionProvider" in availableProviders and devNum > 0:
            if gpu < devNum:
                # Probe: try to create a tiny session with CUDAExecutionProvider.
                # onnxruntime-gpu built for a different CUDA version will fail here
                # with a RuntimeError about missing SO files rather than just a warning.
                try:
                    import numpy as np
                    import os
                    import tempfile
                    import onnx
                    from onnx import helper, TensorProto

                    node = helper.make_node("Identity", ["x"], ["y"])
                    graph = helper.make_graph(
                        [node], "probe",
                        [helper.make_tensor_value_info("x", TensorProto.FLOAT, [1])],
                        [helper.make_tensor_value_info("y", TensorProto.FLOAT, [1])],
                    )
                    model_proto = helper.make_model(graph, opset_imports=[helper.make_opsetid("", 11)])
                    model_proto.ir_version = 7  # pin IR v7 + opset 11 — avoids onnx lib vs onnxruntime version mismatch
                    with tempfile.NamedTemporaryFile(suffix=".onnx", delete=False) as f:
                        f.write(model_proto.SerializeToString())
                        probe_path = f.name
                    try:
                        sess = onnxruntime.InferenceSession(
                            probe_path,
                            providers=["CUDAExecutionProvider"],
                            provider_options=[{"device_id": gpu}],
                        )
                        sess.run(None, {"x": np.zeros([1], dtype=np.float32)})
                        return ["CUDAExecutionProvider"], [{"device_id": gpu}]
                    finally:
                        os.unlink(probe_path)
                except Exception as cuda_err:
                    print(f"[Voice Changer] CUDAExecutionProvider unavailable ({cuda_err}), using CPU")
            else:
                print("[Voice Changer] device detection error, fallback to cpu")
        elif gpu >= 0 and "DmlExecutionProvider" in availableProviders:
            return ["DmlExecutionProvider"], [{"device_id": gpu}]

        return ["CPUExecutionProvider"], [
            {
                "intra_op_num_threads": 8,
                "execution_mode": onnxruntime.ExecutionMode.ORT_PARALLEL,
                "inter_op_num_threads": 8,
            }
        ]


    def setForceTensor(self, forceTensor: bool):
        self.forceTensor = forceTensor

    def halfPrecisionAvailable(self, id: int):
        if self.gpu_num == 0:
            return False
        if id < 0:
            return False
        if self.forceTensor:
            return False

        try:
            gpuName = torch.cuda.get_device_name(id).upper()
            if (
                ("16" in gpuName and "V100" not in gpuName)
                or "P40" in gpuName.upper()
                or "1070" in gpuName
                or "1080" in gpuName
            ):
                return False
        except Exception as e:
            print(e)
            return False

        cap = torch.cuda.get_device_capability(id)
        if cap[0] < 7:  # コンピューティング機能が7以上の場合half precisionが使えるとされている（が例外がある？T500とか）
            return False

        return True

    def getDeviceMemory(self, id: int):
        try:
            return torch.cuda.get_device_properties(id).total_memory
        except Exception as e:
            # except:
            print(e)
            return 0
