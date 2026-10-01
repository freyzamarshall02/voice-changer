import pickle
import torch
import torchaudio
from torch import device, nn
from voice_changer.RVC.embedder.Embedder import Embedder

# ── fairseq-free checkpoint loader ──────────────────────────────────────────

class _Stub:
    """
    Generic stand-in for any fairseq / omegaconf class that gets pickled
    into the checkpoint's `cfg` section.  We only care about reading a
    handful of scalar fields (encoder_layers, encoder_embed_dim) from it;
    everything else can safely return a default.
    """
    def __init__(self, *args, **kwargs):
        # Store kwargs so .get() can reflect them; positional args are ignored.
        self._data: dict = kwargs

    def __getattr__(self, name: str) -> "_Stub":
        # Chained access (e.g. cfg.model.encoder_layers) returns another stub.
        return _Stub()

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def __iter__(self):
        return iter([])

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return f"_Stub({self._data})"


class _FairseqPickleModule:
    """
    Drop-in replacement for the `pickle` module that torch.serialization
    uses internally.  We wrap `Unpickler` so that `find_class` stubs out
    any fairseq.* / omegaconf.* reference instead of trying to import it.
    """

    # Expose every attribute of the real pickle module transparently.
    def __getattr__(self, name):
        return getattr(pickle, name)

    class Unpickler(pickle.Unpickler):
        _STUB_PREFIXES = ("fairseq.", "omegaconf.")

        def find_class(self, module: str, name: str):
            if module.startswith(self._STUB_PREFIXES):
                return _Stub
            return super().find_class(module, name)


def _load_fairseq_checkpoint_without_fairseq(file: str) -> dict:
    """
    Load a fairseq-format .pt checkpoint without fairseq being installed.

    torch.serialization uses `pickle` internally.  We temporarily swap it
    for `_FairseqPickleModule` whose `Unpickler.find_class` returns `_Stub`
    for every `fairseq.*` / `omegaconf.*` class reference — so the import
    system is never consulted for those modules.

    torch still handles all zip-reading, storage reconstruction, and device
    mapping; we only intercept the class-name → class lookup step.
    """
    import torch.serialization as _ts

    _real_pickle = _ts.pickle          # save
    _ts.pickle = _FairseqPickleModule()  # swap
    try:
        return torch.load(file, map_location="cpu", weights_only=False)
    finally:
        _ts.pickle = _real_pickle      # always restore




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
