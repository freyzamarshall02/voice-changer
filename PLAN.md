# Fix Plan — HuBERT Embedder (transformers-based, Applio approach)

> **Status:** Ready to implement
> **Reference:** `/workspaces/codespaces-blank/Applio/rvc/lib/utils.py` + `rvc/realtime/pipeline.py`

---

## Root Cause

The error logs show in `/workspaces/codespaces-blank/voice-changer/errorlogs.txt`:

```
TypeError: '_Stub' object is not callable
RuntimeError: [Voice Changer][HuBERT] Failed to load checkpoint 'pretrain/hubert_base.pt': '_Stub' object is not callable
```

### Why the current code breaks

`FairseqHubert.py` uses a `_Stub` / `_FairseqPickleModule` pickle hack to load a fairseq `.pt`
checkpoint without fairseq installed. This worked on Python 3.12 but **breaks on Python 3.13**:
Python 3.13 changed how pickle reconstructs objects — it calls the registered class **directly as
a callable with positional arguments**. Our `_Stub.__init__` accepted `*args` but the class itself
was not callable in that context, raising `TypeError: '_Stub' object is not callable`.

No amount of patching `_Stub` can fix this cleanly. The root problem is the file format itself:
fairseq `.pt` checkpoints embed fairseq/omegaconf class references in their pickle stream.

---

## Solution — Copy Applio's Approach Exactly

Applio solved this cleanly. Their code in `rvc/lib/utils.py` and `rvc/realtime/pipeline.py`:

1. Defines `HubertModelWithFinalProj(HubertModel)` — subclasses `transformers.HubertModel`, adds `final_proj`
2. Calls `HubertModelWithFinalProj.from_pretrained(dir_path)` — loads from a HuggingFace directory
3. In inference: `model(feats)["last_hidden_state"]` then applies `final_proj` only for v1

| | Old (broken) | New (Applio-style) |
|---|---|---|
| Checkpoint | `pretrain/hubert_base.pt` — fairseq pickle | `pretrain/contentvec/` — HF dir (`config.json` + `pytorch_model.bin`) |
| Loader | `torch.load()` + pickle hack + torchaudio | `HubertModel.from_pretrained(path)` |
| fairseq/torchaudio dep | Required | **Zero** |
| Python 3.13 | ❌ Breaks | ✅ Works |
| `transformers` dep | Not used | Required (pre-installed on Colab) |

---

## Exact Applio Pattern (from source)

From `Applio/rvc/lib/utils.py` (lines 33–36, 179–180):
```python
class HubertModelWithFinalProj(HubertModel):
    def __init__(self, config):
        super().__init__(config)
        self.final_proj = nn.Linear(config.hidden_size, config.classifier_proj_size)

# Loading:
models = HubertModelWithFinalProj.from_pretrained(model_path)
```

From `Applio/rvc/realtime/pipeline.py` (lines 376–381) and `rvc/infer/pipeline.py` (lines 336–339):
```python
feats = self.hubert_model(feats)["last_hidden_state"]
feats = (
    self.hubert_model.final_proj(feats[0]).unsqueeze(0)
    if self.version == "v1"
    else feats
)
```

> **Key insight:** Applio always uses `["last_hidden_state"]` — it does NOT index into
> `hidden_states[layer]`. The v1/v2 branch is based on `version` string, not `embOutputLayer`.

---

## Adapting to Our `extractFeatures` API

Our `Pipeline.py` calls:
```python
feats = self.embedder.extractFeatures(feats, embOutputLayer, useFinalProj)
```

We preserve this signature. Inside the new `extractFeatures`, we **ignore `embOutputLayer`**
(always use `last_hidden_state`, matching Applio exactly) and use `useFinalProj` to decide
whether to apply `final_proj`:

```python
def extractFeatures(self, feats, embOutputLayer=9, useFinalProj=True):
    with torch.no_grad():
        outputs = self.model(feats.to(self.dev))
        hidden = outputs["last_hidden_state"]          # always last hidden state (Applio-exact)
        if useFinalProj and self.model.final_proj is not None:
            return self.model.final_proj(hidden[0]).unsqueeze(0)
        return hidden
```

This means:
- RVC v1 → `useFinalProj=True`  → `final_proj(last_hidden_state[0])` → 256-dim ✅
- RVC v2 → `useFinalProj=False` → raw `last_hidden_state` → 768-dim ✅
- `embOutputLayer` is accepted but unused (backward-compatible, no callers need to change)

---

## Files to Change

### 1. `server/voice_changer/RVC/embedder/FairseqHubert.py` — **Full rewrite**

**Remove entirely:**
- `_Stub` class
- `_FairseqPickleModule` class
- `_load_fairseq_checkpoint_without_fairseq()` function
- `HubertModelWithFinalProj(nn.Module)` (torchaudio-based wrapper)
- All `torchaudio` imports
- All `pickle` imports

**Add:**
- `from transformers import HubertModel`
- `from torch import nn`
- New `HubertModelWithFinalProj(HubertModel)` — exact copy from Applio `rvc/lib/utils.py`
- New `FairseqHubert.loadModel()` — calls `HubertModelWithFinalProj.from_pretrained(file)` where `file` is a **directory path** (e.g. `pretrain/contentvec`)
- New `FairseqHubert.extractFeatures()` — uses `model(feats)["last_hidden_state"]`, applies `final_proj` based on `useFinalProj` flag

### 2. `server/voice_changer/RVC/embedder/FairseqContentvec.py` — **No change needed**

Already subclasses `FairseqHubert` and just calls `super().loadModel()` then overrides `embedderType`.
Works as-is once `FairseqHubert` is fixed. The `file` arg must be a directory path.

### 3. `server/downloader/WeightDownloader.py` — **Change download target**

- **Old:** downloads `hubert_base.pt` from `ddPn08/rvc-webui-models` as a single file
- **New:** downloads `contentvec/pytorch_model.bin` + `contentvec/config.json` from `IAHispano/Applio` into `pretrain/contentvec/`
- **Existence check:** check for `pretrain/contentvec/pytorch_model.bin` (file), not the old `.pt` path
- Both `hubert_base` and `content_vec_500` routes point to same `pretrain/contentvec/` dir
- Remove the final hard-fail check on `hubert_base` existing as a single file — replace with dir check
- Use `requests` or `urllib` (already available) instead of `wget` (which Applio uses but may not be installed)

### 4. `server/Okada.py` — **Change default arg paths**

| Arg | Old default | New default |
|---|---|---|
| `--hubert_base` | `pretrain/hubert_base.pt` | `pretrain/contentvec` |
| `--content_vec_500` | `pretrain/checkpoint_best_legacy_500.pt` | `pretrain/contentvec` |

Everything else stays the same.

### 5. `server/requirements.txt` — **Add `transformers`, remove `torchaudio`**

- Add: `transformers>=4.27.0`
- Remove or comment out: `torchaudio` (no longer needed for HuBERT loading)
  - Keep only if other parts of the codebase use it (check first)

---

## Download URLs (from Applio's `load_embedding()` in `rvc/lib/utils.py`)

| File | URL |
|---|---|
| `pretrain/contentvec/pytorch_model.bin` | `https://huggingface.co/IAHispano/Applio/resolve/main/Resources/embedders/contentvec/pytorch_model.bin` |
| `pretrain/contentvec/config.json` | `https://huggingface.co/IAHispano/Applio/resolve/main/Resources/embedders/contentvec/config.json` |

These are the exact URLs from Applio's `online_embedders` and `config_files` dicts (lines 142–157 of `rvc/lib/utils.py`).

---

## What Does NOT Change

| Component | Status |
|---|---|
| `EmbedderManager.py` | No change — routing to `FairseqHubert` / `FairseqContentvec` stays the same |
| `Embedder.py` (base class) | No change |
| `FairseqContentvec.py` | No change |
| `OnnxContentvec.py` | No change — ONNX path still tried first, falls back to HF loader |
| `Whisper.py` | No change |
| `Pipeline.py` / `PipelineGenerator.py` | No change — `extractFeatures(feats, embOutputLayer, useFinalProj)` API unchanged |
| `VoiceChangerParams.py` | No structural change — `hubert_base` field now holds a **dir path** |
| All pitch extractors | No change |
| Frontend / UI | No change |

---

## Implementation Order

1. **`FairseqHubert.py`** — core fix (full rewrite)
2. **`WeightDownloader.py`** — download HF-format weights into `pretrain/contentvec/`
3. **`Okada.py`** — update default `--hubert_base` and `--content_vec_500` to `pretrain/contentvec`
4. **`requirements.txt`** — add `transformers`, audit `torchaudio`

---

## Testing Checklist

- [ ] Server starts without import errors
- [ ] `pretrain/contentvec/pytorch_model.bin` and `config.json` downloaded on first run
- [ ] Model loads: no exception in embedder loading
- [ ] Pipeline initializes: no `Pipeline is not initialized` loop
- [ ] Voice conversion produces audio output (RVC v1 → 256-dim, RVC v2 → 768-dim)
