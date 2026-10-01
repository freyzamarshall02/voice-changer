import torch
from torch import device, nn
from transformers import HubertModel
from voice_changer.RVC.embedder.Embedder import Embedder


class HubertModelWithFinalProj(HubertModel):
    """
    Subclasses transformers.HubertModel and adds the final_proj linear layer
    that RVC v1 needs for 256-dim output.  Matches Applio's implementation
    exactly (rvc/lib/utils.py).
    """

    def __init__(self, config):
        super().__init__(config)
        self.final_proj = nn.Linear(config.hidden_size, config.classifier_proj_size)


class FairseqHubert(Embedder):
    def loadModel(self, file: str, dev: device, isHalf: bool = True) -> Embedder:
        """
        Load a HuggingFace-format HuBERT model from a directory.

        Args:
            file: Path to the model directory containing config.json and
                  pytorch_model.bin (e.g. 'pretrain/contentvec').
            dev:  Torch device to place the model on.
            isHalf: Whether to use half-precision (fp16).
        """
        super().setProps("hubert_base", file, dev, isHalf)

        try:
            model = HubertModelWithFinalProj.from_pretrained(file)
        except Exception as e:
            raise RuntimeError(
                f"[Voice Changer][HuBERT] Failed to load model from '{file}': {e}"
            ) from e

        model.eval()
        model = model.to(dev)
        if isHalf:
            model = model.half()

        self.model = model
        return self

    def extractFeatures(
        self, feats: torch.Tensor, embOutputLayer=9, useFinalProj=True
    ) -> torch.Tensor:
        """
        Extract HuBERT features from audio.

        Matches Applio's pipeline.py approach exactly:
          - Always uses last_hidden_state (not an intermediate layer).
          - Applies final_proj only when useFinalProj=True (RVC v1 → 256-dim).
          - embOutputLayer is accepted for API compatibility but not used.

        Args:
            feats:          Input tensor of shape (1, T).
            embOutputLayer: Ignored — kept for API compatibility with Pipeline.py.
            useFinalProj:   True for RVC v1 (256-dim), False for RVC v2 (768-dim).
        """
        with torch.no_grad():
            outputs = self.model(feats.to(self.dev))
            hidden = outputs["last_hidden_state"]   # always last hidden state
            if useFinalProj and self.model.final_proj is not None:
                return self.model.final_proj(hidden[0]).unsqueeze(0)
            return hidden
