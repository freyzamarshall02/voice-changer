from torch import device
from voice_changer.RVC.embedder.Embedder import Embedder
from voice_changer.RVC.embedder.FairseqHubert import FairseqHubert


class FairseqHubertJp(FairseqHubert):
    def loadModel(self, file: str, dev: device, isHalf: bool = True) -> Embedder:
        """
        Load the Japanese HuBERT model from a HuggingFace-format directory.

        Args:
            file: Path to the HuggingFace model directory containing config.json
                  and pytorch_model.bin (e.g. 'pretrain/rinna_hubert_base_jp').
            dev:  Torch device.
            isHalf: Whether to use half-precision.
        """
        super().loadModel(file, dev, isHalf)
        super().setProps("hubert-base-japanese", file, dev, isHalf)
        return self
