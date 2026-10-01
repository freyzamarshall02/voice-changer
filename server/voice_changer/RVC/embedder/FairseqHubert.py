import sys
import types
import torch
import torchaudio
from torch import device, nn
from voice_changer.RVC.embedder.Embedder import Embedder


def _load_fairseq_checkpoint_without_fairseq(file: str) -> dict:
    """
    Load a fairseq-format checkpoint (.pt) without having fairseq installed.

    Fairseq checkpoints are pickled with fairseq classes embedded (e.g.
    fairseq.dataclass.configs.FairseqConfig, omegaconf types, etc.).
    torch.load with weights_only=False tries to deserialize those classes
    and raises ModuleNotFoundError when fairseq is absent.

    Strategy: inject lightweight stub modules into sys.modules for every
    fairseq.* and omegaconf namespace that the pickler references, so that
    pickle can reconstruct the objects as plain stub instances.  We only care
    about the 'model' state-dict and a few scalar cfg fields, so the stubs
    just need to be pickle-constructible (they implement __reduce__).
    """

    class _Stub:
        """Generic stub for any fairseq / omegaconf class."""
        def __init__(self, *args, **kwargs):
            self._args = args
            self._kwargs = kwargs

        # Allow attribute access so cfg.model.encoder_layers works
        def __getattr__(self, name):
            return None

        def get(self, key, default=None):
            return default

    class _StubModule(types.ModuleType):
        """Module stub that returns _Stub for any attribute lookup."""
        def __getattr__(self, name):
            # Return a class (not instance) so pickle can call it as constructor
            return _Stub

    # Build stub modules for all fairseq sub-packages referenced by typical checkpoints
    _stub_prefixes = [
        "fairseq",
        "fairseq.dataclass",
        "fairseq.dataclass.configs",
        "fairseq.models",
        "fairseq.models.wav2vec",
        "fairseq.models.wav2vec.wav2vec2",
        "fairseq.models.roberta",
        "fairseq.tasks",
        "fairseq.tasks.audio_pretraining",
        "fairseq.data",
        "omegaconf",
        "omegaconf._utils",
        "omegaconf.omegaconf",
    ]

    # Save original modules so we can restore them after loading
    _saved = {k: sys.modules.get(k) for k in _stub_prefixes}

    try:
        for prefix in _stub_prefixes:
            if prefix not in sys.modules:
                sys.modules[prefix] = _StubModule(prefix)

        checkpoint = torch.load(file, map_location="cpu", weights_only=False)
        return checkpoint
    finally:
        # Restore original sys.modules state
        for prefix in _stub_prefixes:
            original = _saved[prefix]
            if original is None:
                sys.modules.pop(prefix, None)
            else:
                sys.modules[prefix] = original


class HubertModelWithFinalProj(nn.Module):
    """
    Wraps a torchaudio HuBERT model and restores the `final_proj` linear layer
    that fairseq checkpoints include (used by RVC v1 for 256-dim output).
    """

    def __init__(self, model: nn.Module, final_proj: nn.Linear | None):
        super().__init__()
        self.model = model
        self.final_proj = final_proj

    def extract_features(
        self, source: torch.Tensor, padding_mask: torch.Tensor, output_layer: int
    ):
        # torchaudio extract_features returns (features, lengths)
        # We ask for features at a specific encoder layer (1-indexed in torchaudio).
        features, _ = self.model.extract_features(
            source,
            num_layers=output_layer,
        )
        # features is a list of tensors — one per layer; take the last one
        hidden = features[-1]
        return (hidden,)


class FairseqHubert(Embedder):
    def loadModel(self, file: str, dev: device, isHalf: bool = True) -> Embedder:
        super().setProps("hubert_base", file, dev, isHalf)

        # Load the raw fairseq checkpoint (works without fairseq installed).
        # NOTE: fairseq checkpoints store `cfg` as an omegaconf.DictConfig.
        # If omegaconf is not installed, torch.load itself may raise. We default
        # to hubert_base (12 layers, 768 dim) in that case — correct for all
        # standard RVC pretrain weights.
        num_layers = 12
        encoder_embed_dim = 768
        try:
            checkpoint = _load_fairseq_checkpoint_without_fairseq(file)
            cfg = checkpoint.get("cfg", None)
            if cfg is not None:
                # cfg can be omegaconf.DictConfig or a plain dict
                try:
                    model_cfg = cfg.get("model", {}) or {}
                    num_layers = int(model_cfg.get("encoder_layers", 12))
                    encoder_embed_dim = int(model_cfg.get("encoder_embed_dim", 768))
                except Exception:
                    pass  # fall back to defaults above
        except Exception as e:
            raise RuntimeError(f"[Voice Changer][HuBERT] Failed to load checkpoint '{file}': {e}") from e

        # torchaudio ships hubert_base (12 layers, 768 dim)
        # and hubert_large (24 layers, 1024 dim)
        if num_layers <= 12 and encoder_embed_dim <= 768:
            hubert = torchaudio.models.hubert_base()
        else:
            # hubert_large (24 layers, 1024 dim) is never used by standard RVC.
            # If a checkpoint reports num_layers > 12 it is almost certainly
            # a non-standard or corrupted file — raise early rather than producing
            # silently wrong embeddings with untested key-remapping logic.
            raise RuntimeError(
                f"[Voice Changer][HuBERT] Checkpoint '{file}' reports "
                f"num_layers={num_layers}, encoder_embed_dim={encoder_embed_dim}. "
                "hubert_large is not supported by RVC — check that you are loading "
                "the correct pretrained model (expected hubert_base: 12 layers / 768 dim)."
            )

        # Load weights — fairseq checkpoints store the model under "model" key
        state_dict = checkpoint["model"]

        # torchaudio's HuBERT has a slightly different key namespace;
        # strip the "w2v_encoder.w2v_model." prefix if present
        def _remap(state_dict):
            new_sd = {}
            for k, v in state_dict.items():
                # fairseq wraps with w2v_encoder.w2v_model in some checkpoints
                if k.startswith("w2v_encoder.w2v_model."):
                    k = k[len("w2v_encoder.w2v_model."):]
                new_sd[k] = v
            return new_sd

        state_dict = _remap(state_dict)

        # Extract final_proj weights before loading (torchaudio model has no final_proj)
        final_proj_weight = state_dict.pop("final_proj.weight", None)
        final_proj_bias = state_dict.pop("final_proj.bias", None)

        missing, unexpected = hubert.load_state_dict(state_dict, strict=False)
        if missing:
            print(f"[Voice Changer][HuBERT] Missing keys ({len(missing)}): {missing[:5]}...")
        if unexpected:
            print(f"[Voice Changer][HuBERT] Unexpected keys ({len(unexpected)}): {unexpected[:5]}...")

        # Rebuild final_proj if checkpoint had one (RVC v1 needs it for 256-dim output)
        final_proj = None
        if final_proj_weight is not None:
            out_dim, in_dim = final_proj_weight.shape
            final_proj = nn.Linear(in_dim, out_dim, bias=(final_proj_bias is not None))
            final_proj.weight = nn.Parameter(final_proj_weight)
            if final_proj_bias is not None:
                final_proj.bias = nn.Parameter(final_proj_bias)

        model = HubertModelWithFinalProj(hubert, final_proj)
        model.eval()
        model = model.to(dev)
        if isHalf:
            model = model.half()

        self.model = model
        return self

    def extractFeatures(
        self, feats: torch.Tensor, embOutputLayer=9, useFinalProj=True
    ) -> torch.Tensor:
        padding_mask = torch.BoolTensor(feats.shape).to(self.dev).fill_(False)

        # オリジナル_v1は L9にfinal_projをかけていた。(-> 256)
        # オリジナル_v2は L12にfinal_projをかけない。(-> 768)

        with torch.no_grad():
            logits = self.model.extract_features(
                source=feats.to(self.dev),
                padding_mask=padding_mask,
                output_layer=embOutputLayer,
            )
            if useFinalProj and self.model.final_proj is not None:
                feats = self.model.final_proj(logits[0])
            else:
                feats = logits[0]
        return feats
