# Phase 2 — Python 3.12 / Google Colab Compatibility Rework

> Optional use: You can use graphify to analyzing the code structure
> Prerequisite: Phase 1 (RVC-Only Refactor) must be fully completed before starting this phase.
> Goal: Make the project run cleanly on the latest Google Colab environment (Python 3.12, CUDA 12.x).
> Don't use subagent for saving agent usage

---

## Target Environment

| | Target |
|---|---|
| Python | 3.12 |
| CUDA | 12.x |
| PyTorch | Latest (pre-installed on Colab) |
| OS | Linux (Colab = Ubuntu) |

---

## Why This Order Matters

After Phase 1, 8 non-RVC model folders are gone. This means:
- Fairseq usage in MMVC, DDSP-SVC, and others is already deleted
- Only the **RVC embedder** still uses fairseq
- Surface area for fixes is much smaller — less work, less risk of breaking things

---

## Tasks

### 1. Replace `fairseq` — Medium effort ⚠️ (Must Do)

**Current:**
```
git+https://github.com/liyaodev/fairseq.git
```

**Problem:** Original fairseq is unmaintained and broken on Python 3.12 due to `distutils` removal.

**What it's used for in RVC:** Loading HuBERT / ContentVec pretrain model weights for voice feature extraction.

**Fix — Option A (Recommended):** Drop fairseq entirely. Load HuBERT `.pt` weights directly using `torch.hub` or a lightweight standalone HuBERT loader. Other RVC forks (like so-vits-svc) already did this successfully.

**Fix — Option B:** Replace with `fairseq2` (Meta's official rewrite, Python 3.12 ready). Requires small API changes in the embedder code.

**Files to change:**
- `server/voice_changer/RVC/embedder/` — the HuBERT/ContentVec loader logic
- `server/requirements.txt` — remove the fairseq line

---

### 2. Replace `pyworld` — Trivial effort ✅

**Current:**
```
pyworld
```

**Problem:** Relies on C++ extensions that fail to build on Python 3.12 due to `distutils` removal.

**Fix:** Swap to the drop-in prebuilt replacement — zero code changes needed:
```
pyworld-prebuilt
```

> Alternative: If only using RMVPE or CREPE pitch extractors (both already ONNX-based and Python 3.12 safe), pyworld can be removed entirely since harvest/dio are the only pitch extractors that need it.

---

### 3. Upgrade `librosa` — Very low effort ✅

**Current:**
```
librosa==0.9.1
```

**Problem:** Python 3.12 support only arrived in `0.10.x`.

**Fix:**
```
librosa>=0.10.1
```

Check for any API differences between 0.9 and 0.10 in RVC usage (mostly backward compatible, minor function signature changes).

---

### 4. Unpin `faiss-cpu` — Trivial effort ✅

**Current:**
```
faiss-cpu==1.11.0
```

**Problem:** Old version uses `numpy.distutils` which was removed in Python 3.12.

**Fix:**
```
faiss-cpu
```
(Let pip resolve the latest compatible version)

---

### 5. Unpin other packages — Trivial effort ✅

These were pinned at the time of development and don't need to be. Unpin and test:

| Package | Current | Action |
|---|---|---|
| `fastapi==0.95.1` | Old | Unpin → `fastapi` |
| `python-socketio==5.8.0` | Old | Unpin → `python-socketio` |
| `websockets==11.0.2` | Old (also listed twice) | Unpin → `websockets`, remove duplicate |
| `python-multipart==0.0.6` | Old | Unpin → `python-multipart` |
| `pyOpenSSL==23.1.1` | Old | Unpin → `pyOpenSSL` |
| `resampy==0.4.2` | Old | Unpin → `resampy` |
| `dataclasses_json==0.5.7` | Old | Unpin → `dataclasses_json` |
| `matplotlib==3.7.1` | Old | Unpin → `matplotlib` |

---

### 6. Verify CUDA 12 + PyTorch — Low effort ✅

Colab pre-installs PyTorch with CUDA 12 support. Things to verify:
- `onnxruntime-gpu` — confirm it matches CUDA 12 (use `onnxruntime-gpu>=1.17` for CUDA 12 support)
- `torchcrepe==0.0.18` — check latest version for compatibility
- `torchfcpe==0.0.3` — check latest version

---

## Updated `requirements.txt` (Target State)

```txt
wheel
setuptools
requests
uvicorn
pyOpenSSL
numpy
numba
tqdm
# fairseq REMOVED — replaced with direct torch HuBERT loader
resampy
python-socketio
fastapi
python-multipart
onnxruntime-gpu>=1.17
scipy
matplotlib
websockets
faiss-cpu
pyworld-prebuilt
torchcrepe
librosa>=0.10.1
gin
gin_config
einops
local_attention
sounddevice
dataclasses_json
onnxsim
torchfcpe
```

---

## Testing Checklist

- [ ] Install cleanly on Python 3.12 with no build errors
- [ ] HuBERT/ContentVec embedder loads pretrain weights correctly
- [ ] Harvest/Dio pitch extraction works (pyworld-prebuilt)
- [ ] RMVPE/CREPE pitch extraction works (ONNX-based, should be fine)
- [ ] FAISS index file loads correctly for RVC retrieval
- [ ] ONNX RVC model inference works on CUDA 12
- [ ] PyTorch RVC model inference works on CUDA 12
- [ ] WebUI loads and connects via SocketIO
- [ ] Model upload, slot switching works
- [ ] ONNX export works
- [ ] Model merge works

---

## Notes
- The tunnel setup (ngrok, cloudflared, etc.) for Colab is handled separately by the user — not part of this phase.
- `distutils` was fully removed in Python 3.12. Any package that imports `distutils` internally will fail. This is the root cause of most of the issues above.
- After this phase, the project should work on any modern Linux environment with Python 3.12, not just Colab.
