import torch
from voice_changer.RVC.embedder.Embedder import Embedder


class OnnxContentvec(Embedder):

    def loadModel(self, file: str, dev: torch.device) -> Embedder:
        raise NotImplementedError("OnnxContentvec is not implemented")

    def extractFeatures(
        self, feats: torch.Tensor, embOutputLayer=9, useFinalProj=True
    ) -> torch.Tensor:
        raise NotImplementedError("OnnxContentvec is not implemented")
