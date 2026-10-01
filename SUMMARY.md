# Session Summary — 2026-10-01

## Problem

Selecting any model (custom or default) caused the voice changer pipeline to fail
immediately with **"Pipeline is not initialized"** and no audio output.

### Root Cause

`pretrain/hubert_base.pt` is a fairseq-format checkpoint. When Python's `torch.load`
tries to deserialize it, pickle needs to reconstruct fairseq/omegaconf classes
(e.g. `fairseq.dataclass.configs.FairseqConfig`) that are baked into the file.
Because `fairseq` is not installed, this crashed with:

```
ModuleNotFoundError: No module named 'fairseq'
```

And later after a first fix attempt, crashed with:

```
TypeError: 'type' object is not iterable
```
(Python's import path machinery tried to iterate our fake stub module as a file path.)

---

## Fix — `server/voice_changer/RVC/embedder/FairseqHubert.py`

### Attempts

| # | Approach | Outcome |
|---|---|---|
| 1 | Inject fake stub modules into `sys.modules` before `torch.load` | ❌ `TypeError: 'type' object is not iterable` — Python's `FileFinder` tried to iterate the stub module as a path |
| 2 | Custom `pickle.Unpickler` subclass + manual zip parsing | ❌ Too fragile — `torch.FloatStorage()` removed in PyTorch 2.x, tensor rebuild broken |
| 3 | Temporarily swap `torch.serialization.pickle` with a proxy module | ✅ Works — torch handles all zip/storage/device logic natively, we only intercept `find_class` |

### Final Solution (Attempt 3)

Two new top-level classes added before `FairseqHubert`:

**`_Stub`** — Generic stand-in for any fairseq/omegaconf class:
- `__init__(*args, **kwargs)` — stores kwargs in `self._data`
- `__getattr__` — returns a new `_Stub()` for chained access
- `.get(key, default)` — reads from `self._data` like a dict
- `__iter__`, `__bool__` — safe no-op implementations

**`_FairseqPickleModule`** — Drop-in proxy for the `pickle` module:
- `__getattr__` — proxies all real `pickle` attributes transparently
- Inner `Unpickler(pickle.Unpickler)` — overrides `find_class`:
  - If `module` starts with `"fairseq."` or `"omegaconf."` → return `_Stub`
  - Otherwise → `super().find_class()` (normal resolution)

**`_load_fairseq_checkpoint_without_fairseq(file)`** — The loader:
```python
import torch.serialization as _ts
_real_pickle = _ts.pickle
_ts.pickle = _FairseqPickleModule()
try:
    return torch.load(file, map_location="cpu", weights_only=False)
finally:
    _ts.pickle = _real_pickle
```

This lets `torch.load` do all the real work (zip extraction, storage
reconstruction, device mapping) while our proxy intercepts only the
`find_class` step for missing fairseq/omegaconf modules — never touching
the import system at all.

---

## Files Changed

| File | Change |
|---|---|
| `server/voice_changer/RVC/embedder/FairseqHubert.py` | Added `_Stub`, `_FairseqPickleModule`, `_load_fairseq_checkpoint_without_fairseq()`; replaced `torch.load()` call in `loadModel()` with the new loader |

## Files NOT Changed

- `EmbedderManager.py` — no changes needed
- `OnnxContentvec.py` — still a `NotImplementedError` stub (expected, ONNX path not used)
- `requirements.txt` — `fairseq` already removed in a prior session

---

## Other Findings (No Action Taken)

- `pretrain/` directory is auto-downloaded on first run — all 8 weight files confirmed present ✅
- `gin`, `einops`, `local_attention` — listed in Phase 2 plan but not actually imported anywhere in the codebase, ignored for now
- ONNX Runtime CUDA warning — expected in this environment (`libcublasLt.so.13` mismatch), non-fatal

---

## Next Steps

- Test the fix on Colab (run server, select model, start voice changing)
- If working: proceed to **Phase 1** (RVC-only refactor per `ANTIGRAVITY.md`)
- Then: **Phase 2** remaining tasks (pyworld, librosa, faiss unpinning per `ANTIGRAVITYPHASE2.md`)
