# Feature Summary: Upload Model via URL

**Date:** 2026-10-07

---

## Overview

Added a URL-based model download feature to the File Uploader modal. Users can now paste a Google Drive, HuggingFace, or Pixeldrain link and have the server download and install the model directly into the target slot — no manual file transfer needed.

---

## UX Flow

```
ModelSlotManagerDialog
    → click upload icon on a slot
    ↓
FileUploader modal
    - Model: [select file]
    - Index: [select file]
    - [upload] button          ← existing file-upload path
    - [Upload Model via URL]   ← NEW button
    ↓ click "Upload Model via URL"
URLUploader sub-screen (inside same modal)
    - Info banner listing supported sources
    - URL text input
    - [Upload via URL] button
    - Inline progress bar (0–100%)
    - On success → auto-close → back to ModelSlotManager
    - On error   → inline red error message
```

The VoiceChangerType dropdown was also removed from the File Uploader — the app is RVC-only and no longer needs to surface this choice.

---

## Files Changed

| File | Type | Description |
|---|---|---|
| `server/downloader/UrlModelDownloader.py` | **New** | Core download pipeline: URL detection, streaming, ZIP extraction, slot placement, metadata generation |
| `server/voice_changer/VoiceChangerManager.py` | Modified | Added `_url_download_status` dict, `download_model_from_url()` (background thread), `get_url_download_status()` |
| `server/restapi/MMVC_Rest_Fileuploader.py` | Modified | Added `POST /download_model_url` and `GET /download_model_url_status` endpoints |
| `server/requirements.txt` | Modified | Added `gdown` for Google Drive support |
| `client/lib/src/client/ServerRestClient.ts` | Modified | Added `downloadModelFromUrl()` and `getUrlDownloadStatus()` HTTP methods |
| `client/lib/src/client/ServerConfigurator.ts` | Modified | Delegated both new methods to `ServerRestClient` |
| `client/lib/src/VoiceChangerClient.ts` | Modified | Pass-through delegation to `ServerConfigurator` |
| `client/lib/src/hooks/useServerSetting.ts` | Modified | Added both methods to `ServerSettingState` type and hook return value |
| `client/demo/src/components/demo/904-3_FileUploader.tsx` | Modified | Removed VoiceChangerType dropdown; added URL sub-screen with progress bar, error banner, unmount-safe polling |

---

## Backend Detail

### `UrlModelDownloader.py`

Entry point: `download_model_from_url(url, slot, model_dir, progress_callback)`

**Host detection:**
- `drive.google.com` → downloads via `gdown` (handles auth/fuzzy links)
- `huggingface.co` → rewrites `/blob/` → `/resolve/` then streams via `requests`
- `pixeldrain.com` → converts `/u/FILEID` → `/api/file/FILEID?download` then streams
- Anything else → raises `ValueError` with a user-friendly message

**After download:**
- `.zip` → extracted to a temp dir, single-level subfolders flattened, all files moved into `model_dir/<slot>/`
- `.pth` / `.onnx` / `.index` → moved directly into `model_dir/<slot>/`
- Validates that at least one `.pth` or `.onnx` is present after extraction

**Metadata generation:**
- Calls `RVCModelSlotGenerator.loadModel()` to read model weights and derive `embChannels`, `samplingRate`, `f0`, etc.
- Saves the completed `RVCModelSlot` via `ModelSlotManager.save_model_slot()`

**Progress reporting (via callback):**
| Stage | Value |
|---|---|
| Download start | 0% |
| Streaming (proportional) | 1–90% |
| Post-download | 90% |
| Metadata generation | 95% |
| Complete | 100% |

**Error handling — human-readable, no tracebacks to client:**

| Condition | Client message |
|---|---|
| HTTP 404 | "File not found. The link may be broken or deleted." |
| HTTP 403 | "Access denied. The file may be private or require login." |
| Unsupported host | "Unsupported host. Use Google Drive, HuggingFace, or Pixeldrain." |
| No `.pth`/`.onnx` in archive | "No model file (.pth/.onnx) found inside the archive." |
| Timeout | "Download timed out. Check your connection and try again." |
| Unexpected | "An unexpected error occurred. Check server logs." |

### `VoiceChangerManager.py`

- Module-level `_url_download_status: dict[int, dict]` tracks per-slot state:
  ```python
  { slot: {"progress": 0–100, "status": "idle|downloading|done|error", "msg": ""} }
  ```
- `download_model_from_url(url, slot)` — starts a daemon thread; writes progress to the dict; catches `ValueError` (user-facing) and bare `Exception` (logged, generic client message) separately
- `get_url_download_status(slot)` — returns the dict entry, defaulting to `idle` if slot has never been used

### REST Endpoints

```
POST /download_model_url
  Body (form): url: str, slot: int
  Returns: {"status": "OK", "msg": "Download started"}   (immediate, download runs in background)

GET /download_model_url_status?slot=<int>
  Returns: {"progress": 0–100, "status": "idle|downloading|done|error", "msg": "..."}
```

---

## Frontend Detail

### Polling strategy

The UI polls `GET /download_model_url_status` every **500 ms** after kicking off the download. When `status === "done"` the modal closes automatically. When `status === "error"` the interval stops and an inline red error banner is shown.

The polling `setInterval` ID is stored in a `useRef` and cleared in a `useEffect` cleanup, preventing state updates after the component unmounts.

### URLUploader sub-screen layout

```
┌──────────────────────────────────────────┐
│  File Uploader                           │
├──────────────────────────────────────────┤
│  Upload Model via URL       [<<back]     │
│                                          │
│  ℹ Supported sources:                   │
│    • Google Drive                        │
│    • HuggingFace                         │
│    • Pixeldrain                          │
│                                          │
│  URL: [________________________________] │
│                                          │
│  [  Upload via URL  ]                    │
│                                          │
│  ████████░░░░  42%      (while active)  │
│  ❌ Failed: <reason>    (on error)       │
└──────────────────────────────────────────┘
```

---

## Bugs Fixed During Review

| Bug | Fix |
|---|---|
| `gdown` partial file left on disk when it returns `None` (private file) | Added `os.remove(tmp_path)` before raising `ValueError` |
| `setInterval` leaked on component unmount mid-download | Added `useRef` + `useEffect` cleanup |
| `gdown` not in `requirements.txt` | Added `gdown` to `server/requirements.txt` |
