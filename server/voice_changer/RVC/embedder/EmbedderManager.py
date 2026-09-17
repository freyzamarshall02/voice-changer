from torch import device

from const import EmbedderType
from voice_changer.RVC.embedder.Embedder import Embedder
from voice_changer.RVC.embedder.FairseqContentvec import FairseqContentvec
from voice_changer.RVC.embedder.FairseqHubert import FairseqHubert
from voice_changer.RVC.embedder.FairseqHubertJp import FairseqHubertJp
from voice_changer.RVC.embedder.OnnxContentvec import OnnxContentvec
from voice_changer.RVC.embedder.Whisper import Whisper
from voice_changer.utils.VoiceChangerParams import VoiceChangerParams


class EmbedderManager:
    currentEmbedder: Embedder | None = None
    params: VoiceChangerParams

    @classmethod
    def initialize(cls, params: VoiceChangerParams):
        cls.params = params

    @classmethod
    def getEmbedder(cls, embederType: EmbedderType, isHalf: bool, dev: device) -> Embedder:
        if cls.currentEmbedder is None:
            print("[Voice Changer] generate new embedder. (no embedder)")
            cls.currentEmbedder = cls.loadEmbedder(embederType, isHalf, dev)
        elif cls.currentEmbedder.matchCondition(embederType) is False:
            print("[Voice Changer] generate new embedder. (not match)")
            cls.currentEmbedder = cls.loadEmbedder(embederType, isHalf, dev)
        else:
            print("[Voice Changer] reuse existing embedder. (match)")
            # Embedder type matches — reuse the cached instance.
            # Device / half-precision updates are handled on the model side.
        return cls.currentEmbedder

    @classmethod
    def loadEmbedder(cls, embederType: EmbedderType, isHalf: bool, dev: device) -> Embedder:
        if embederType == "hubert_base":
            try:
                if cls.params.content_vec_500_onnx_on is False:
                    raise Exception("[Voice Changer][Embedder] onnx is off")
                file = cls.params.content_vec_500_onnx
                return OnnxContentvec().loadModel(file, dev)
            except Exception as e:  # noqa
                print("[Voice Changer] use torch contentvec", e)
                file = cls.params.hubert_base
                return FairseqHubert().loadModel(file, dev, isHalf)
        elif embederType == "hubert-base-japanese":
            file = cls.params.hubert_base_jp
            return FairseqHubertJp().loadModel(file, dev, isHalf)
        elif embederType == "contentvec":
            try:
                if cls.params.content_vec_500_onnx_on is False:
                    raise Exception("[Voice Changer][Embedder] onnx is off")
                file = cls.params.content_vec_500_onnx
                return OnnxContentvec().loadModel(file, dev)
            except Exception as e:
                print(e)
                file = cls.params.content_vec_500
                return FairseqContentvec().loadModel(file, dev, isHalf)
        elif embederType == "whisper":
            file = cls.params.whisper_tiny
            return Whisper().loadModel(file, dev, isHalf)
        else:
            raise ValueError(f"[Voice Changer][Embedder] Unknown embedder type: {embederType!r}")
