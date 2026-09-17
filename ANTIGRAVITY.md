# RVC-Only Refactor Plan

> Scope: Strip this voice changer down to **RVC only**, removing all other VC model backends while keeping all RVC-specific features intact (ONNX support, model merging, ONNX export, pitch extractors, etc.).

---

## What We're Keeping

Everything inside `server/voice_changer/RVC/` stays **untouched**:

| Folder / File | Purpose |
|---|---|
| `RVC/inferencer/` | PyTorch + ONNX RVC inferencers (including `OnnxRVCInferencer.py`) |
| `RVC/onnxExporter/` | Convert PyTorch `.pth` RVC models → ONNX |
| `RVC/modelMerger/` | RVC model merging feature |
| `RVC/pitchExtractor/` | CREPE, RMVPE (including ONNX variants) |
| `RVC/embedder/` | ContentVec, Whisper, ONNX ContentVec |
| `RVC/pipeline/` | Full RVC inference pipeline |
| `RVC/deviceManager/` | GPU/device management |
| `server/voice_changer/VoiceChangerV2.py` | Generic V2 engine used by RVC |
| `server/voice_changer/common/` | Shared utilities |
| `server/voice_changer/utils/` | Shared interfaces & base classes |
| `server/voice_changer/Local/` | Server device audio I/O |
| `server/voice_changer/ModelSlotManager.py` | Generic slot manager |

### ONNX Support — Fully Preserved
RVC ONNX support is self-contained inside the `RVC/` folder. The following workflows are all kept:
- Upload and run a `.onnx` RVC model directly
- Convert a PyTorch `.pth` RVC model to ONNX (export button in UI)
- ONNX-based pitch extraction (CREPE, RMVPE)
- AMD/Intel GPU acceleration via DirectML with ONNX models

---

## What We're Removing

### Backend — Delete These Folders Entirely
| Folder | Model |
|---|---|
| `server/voice_changer/MMVCv13/` | MMVC v1.3 |
| `server/voice_changer/MMVCv15/` | MMVC v1.5 |
| `server/voice_changer/SoVitsSvc40/` | so-vits-svc 4.0 |
| `server/voice_changer/DDSP_SVC/` | DDSP-SVC |
| `server/voice_changer/DiffusionSVC/` | Diffusion-SVC |
| `server/voice_changer/Beatrice/` | Beatrice v1/v2 |
| `server/voice_changer/LLVC/` | LLVC |
| `server/voice_changer/EasyVC/` | EasyVC |

---

## Code Changes Required

### 1. `server/voice_changer/VoiceChangerManager.py`
- In `loadModel()`: remove all `elif` branches except `voiceChangerType == "RVC"`
- In `generateVoiceChanger()`: remove all `elif` branches except `voiceChangerType == "RVC"`
- Add a server-side guard: if `voiceChangerType != "RVC"`, return `{"status": "ERROR", "msg": "Only RVC models are supported"}` — no crash, no console spam

### 2. `server/data/ModelSlot.py`
- Remove dataclasses: `MMVCv13ModelSlot`, `MMVCv15ModelSlot`, `SoVitsSvc40ModelSlot`, `DDSPSVCModelSlot`, `DiffusionSVCModelSlot`, `BeatriceModelSlot`, `LLVCModelSlot`, `EasyVCModelSlot`
- Trim `ModelSlots` type alias — keep only `ModelSlot` and `RVCModelSlot`
- Trim `loadSlotInfo()` — keep only the `"RVC"` branch
- In `loadAllSlotInfo()` — **remove lines 214-215** (the hardcoded `Beatrice-JVS` static slot load). This is easy to miss if only looking at folder structure.

### 3. `server/const.py`
- Trim `VoiceChangerType` enum — keep only `"RVC"`

### 4. `client/lib/src/const.ts` (Frontend TypeScript)
- Trim `VoiceChangerType` enum — keep only `RVC`
- Remove non-RVC model slot types: `MMVCv13ModelSlot`, `MMVCv15ModelSlot`, `SoVitsSvc40ModelSlot`, `DDSPSVCModelSlot`, `DiffusionSVCModelSlot`, `BeatriceModelSlot`, `LLVCModelSlot`
- Trim `ModelSlotUnion` — keep only `RVCModelSlot`
- Remove DDSP-SVC specific fields from the shared `ModelSlot` interface (lines 191-199)
- Remove `DiffusionSVCSampleModel` type

### 5. `client/demo/src/` (Frontend UI Components)
- Remove non-RVC model options from upload forms and model type dropdowns
- Trim any `if/switch` on `voiceChangerType` in TSX components (e.g. `904_ModelSlotManagerDialog.tsx`, `904-3_FileUploader.tsx`)

---

## UX Strategy for Non-RVC Uploads

Use a layered approach:

1. **Proactive (frontend):** Remove non-RVC model options from the UI entirely — users can't even select MMVC/Beatrice/etc.
2. **Reactive (server):** If a non-RVC request somehow reaches the server (e.g. direct API call), return a clean JSON error: `{"status": "ERROR", "msg": "Only RVC models are supported"}`
3. **Frontend fallback:** Display the server error as a toast/banner in the WebUI — no console errors, no crashes.

---

## Summary of Touch Points

| Layer | Files to Edit | Files/Folders to Delete |
|---|---|---|
| Backend Python | `VoiceChangerManager.py`, `ModelSlot.py`, `const.py` | 8 model folders |
| Frontend TypeScript | `client/lib/src/const.ts` | — |
| Frontend UI (TSX) | `904_ModelSlotManagerDialog.tsx`, `904-3_FileUploader.tsx`, and other components with model-type branching | — |

---

## Notes
- `merge_models()` and `export2onnx()` in `VoiceChangerManager.py` are **already RVC-only** — no changes needed there.
- The `VoiceChanger.py` (V1 engine) can eventually be removed too since RVC uses `VoiceChangerV2.py`, but this is optional/low priority.
- The `Beatrice-JVS` hardcoded static slot in `loadAllSlotInfo()` is a special case — it must be removed from code, not just by deleting the folder.
