# FIX — ONNX Default Model: Latency + Binary Packet Errors

> **Status:** Ready to implement  
> **Error logs:** `/workspaces/codespaces-blank/voice-changer/errorlogs.txt`  
> **Symptom:** ONNX default model loads and produces audio but with heavy delay, then throws `ValueError: Unexpected binary packet` errors in the socket.io layer.

---

## Root Causes (Two Separate Problems)

### Problem 1 — `onnxruntime-gpu` CUDA version mismatch → CPU fallback → slowness

**Error (logs line 8–11):**
```
Failed to load library libonnxruntime_providers_cuda.so:
  libcublasLt.so.13: cannot open shared object file: No such file or directory

Require cuDNN 9.* and CUDA 13.*
```

**Why:** `onnxruntime-gpu>=1.17` (unpinned upper bound) resolves to **onnxruntime-gpu 1.19+** on Colab, which requires **CUDA 13 + cuDNN 9**. Colab provides **CUDA 12.x**, so `CUDAExecutionProvider` fails silently. The ONNX model falls back to 8-thread **CPU** inference — functional but very slow.

`DeviceManager.getOnnxExecutionProvider()` correctly detects `CUDAExecutionProvider` as available (it's in `onnxruntime.get_available_providers()`) but the runtime load of the CUDA SO fails, producing warnings and falling through to CPU.

**Fix:** Pin `onnxruntime-gpu` to `>=1.17,<1.19` (last release that works with CUDA 12.x). Additionally, suppress the repeated CUDA warnings by catching the provider load error.

---

### Problem 2 — `ValueError: Unexpected binary packet` in python-socketio

**Error (logs lines 78–107):**
```python
# socketio/async_server.py:722
raise ValueError('Unexpected binary packet')

# socketio/async_server.py:706 → packet.py:77
self.packet_type = int(ep[0:1])
ValueError: invalid literal for int() with base 10: b'\x17'
```

**Why:** Two contributing factors:

1. **CPU slowness causes frame ordering issues.** The JS client (`socket.io-client ^4.7.4`) sends binary audio frames (Socket.IO BINARY_EVENT, type 5) as a text frame announcing the attachment followed immediately by a binary websocket frame. When the server is CPU-bound processing ONNX, it processes these out of the expected order, and `python-socketio` receives a binary websocket frame when it isn't tracking a pending attachment — hence `Unexpected binary packet`.

2. **`python-socketio` is unpinned in `requirements.txt`** (line 19: just `python-socketio`). Colab may install a newer version (≥5.11) that changed binary frame dispatching behaviour in `_handle_eio_message`, introducing a regression with the binary audio payloads this server sends/receives.

The client uses:
```json
"socket.io-client": "^4.7.4"
```
which speaks **Socket.IO protocol v5 / Engine.IO v4**. The server must use `python-socketio` 5.x + `python-engineio` 4.x.

---

## Files to Change

### 1. `server/requirements.txt` — pin `python-socketio`, `python-engineio`, and `onnxruntime-gpu`

**Current (broken):**
```
python-socketio
...
onnxruntime-gpu>=1.17
```

**Replace lines 19 and 22 with:**
```
python-socketio>=5.7,<6
python-engineio>=4.3,<5
...
onnxruntime-gpu>=1.17,<1.19
```

**Exact diff:**
```diff
-python-socketio
 fastapi
 python-multipart
-onnxruntime-gpu>=1.17
+python-socketio>=5.7,<6
+python-engineio>=4.3,<5
+fastapi
+python-multipart
+onnxruntime-gpu>=1.17,<1.19
```

> [!IMPORTANT]
> Also add `python-engineio` explicitly — `python-socketio` pulls it as a dep but without a pin it may grab an incompatible version.

---

### 2. `server/voice_changer/RVC/deviceManager/DeviceManager.py` — graceful CUDA provider fallback

**Current `getOnnxExecutionProvider` (line 36–60):** selects `CUDAExecutionProvider` if it's in `get_available_providers()` AND torch sees a GPU. But it doesn't catch the actual SO load failure that onnxruntime emits as a warning — so the session still tries CUDA, logs the wall of warnings, and silently falls to CPU.

**Fix:** Probe whether the CUDA provider actually works before committing to it, and fall back cleanly with a single clear log message.

```python
def getOnnxExecutionProvider(self, gpu: int):
    availableProviders = onnxruntime.get_available_providers()
    devNum = torch.cuda.device_count()
    if gpu >= 0 and "CUDAExecutionProvider" in availableProviders and devNum > 0:
        if gpu < devNum:
            # Probe: try to create a tiny session with CUDAExecutionProvider.
            # onnxruntime-gpu built for a different CUDA version will fail here
            # with a RuntimeError about missing SO files rather than just a warning.
            try:
                import numpy as np, tempfile, os
                # Minimal 1-op ONNX model to probe the provider
                import onnx
                from onnx import helper, TensorProto
                node = helper.make_node("Identity", ["x"], ["y"])
                graph = helper.make_graph([node], "probe", [helper.make_tensor_value_info("x", TensorProto.FLOAT, [1])], [helper.make_tensor_value_info("y", TensorProto.FLOAT, [1])])
                model_proto = helper.make_model(graph)
                with tempfile.NamedTemporaryFile(suffix=".onnx", delete=False) as f:
                    f.write(model_proto.SerializeToString())
                    probe_path = f.name
                try:
                    sess = onnxruntime.InferenceSession(probe_path, providers=["CUDAExecutionProvider"], provider_options=[{"device_id": gpu}])
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

    return ["CPUExecutionProvider"], [{
        "intra_op_num_threads": 8,
        "execution_mode": onnxruntime.ExecutionMode.ORT_PARALLEL,
        "inter_op_num_threads": 8,
    }]
```

> [!NOTE]
> The probe approach is heavier but gives a definitive answer. Alternatively, just suppress the `onnxruntime` logger for the CUDA provider warnings with:
> ```python
> import logging
> logging.getLogger("onnxruntime").setLevel(logging.ERROR)
> ```
> — but this only hides the noise, doesn't fix the CPU fallback path.

> [!TIP]
> **Simpler alternative fix for DeviceManager:** Just catch the ORT exception when creating the real session in `OnnxRVCInferencer.loadModel()` and retry with CPUExecutionProvider. The probe approach is cleaner but adds `onnx` as a dependency.

---

### 3. `server/voice_changer/RVC/inferencer/OnnxRVCInferencer.py` — retry with CPU on CUDA failure

This is the **simplest and most robust fix** — no probe needed. Modify `loadModel()` to retry with CPU if the CUDA session fails:

```python
def loadModel(self, file: str, gpu: int, inferencerTypeVersion: str | None = None):
    self.setProps(EnumInferenceTypes.onnxRVC, file, True, gpu)
    (onnxProviders, onnxProviderOptions) = DeviceManager.get_instance().getOnnxExecutionProvider(gpu)

    try:
        onnx_session = onnxruntime.InferenceSession(
            file, providers=onnxProviders, provider_options=onnxProviderOptions
        )
    except Exception as e:
        print(f"[Voice Changer][ONNX] Primary provider failed ({e}), falling back to CPU")
        onnx_session = onnxruntime.InferenceSession(
            file,
            providers=["CPUExecutionProvider"],
            provider_options=[{"intra_op_num_threads": 8}],
        )

    # check half-precision
    first_input_type = onnx_session.get_inputs()[0].type
    self.isHalf = first_input_type != "tensor(float)"
    self.model = onnx_session
    self.inferencerTypeVersion = inferencerTypeVersion
    return self
```

---

## Implementation Order

1. **`server/requirements.txt`** — pin `python-socketio>=5.7,<6`, `python-engineio>=4.3,<5`, `onnxruntime-gpu>=1.17,<1.19`
2. **`server/voice_changer/RVC/inferencer/OnnxRVCInferencer.py`** — add CPU retry in `loadModel()`
3. **(Optional)** **`server/voice_changer/RVC/deviceManager/DeviceManager.py`** — suppress repeated CUDA warnings

> [!WARNING]
> Fixing the `requirements.txt` pin only helps **on new installs**. In an existing Colab session where `onnxruntime-gpu 1.19+` is already installed, the `OnnxRVCInferencer.py` CPU retry (step 2) is the **effective fix** regardless of the version pin.

---

## Testing Checklist

- [ ] No `libcublasLt.so` warnings spam on ONNX model load
- [ ] ONNX model inference latency is low (GPU path confirmed, or CPU path explicitly logged once)  
- [ ] No `ValueError: Unexpected binary packet` errors during audio streaming
- [ ] `python-socketio` version in Colab is 5.x: `import socketio; print(socketio.__version__)`
- [ ] Voice output still works with ONNX default model
- [ ] PyTorch `.pth` model still works (regression check)
