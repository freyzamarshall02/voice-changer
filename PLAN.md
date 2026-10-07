# Plan: Add "Upload Model via URL" to Voice Changer

## Overview

Add a URL-based model download feature to the voice-changer File Uploader modal. The user pastes a Google Drive, HuggingFace, or Pixeldrain URL and the server downloads the model directly into the correct slot — mirroring Applio's `model_download_pipeline` pattern.

---

## UX Flow

```
ModelSlotManagerDialog (Main)
    → click upload icon on a slot
    ↓
FileUploader modal            ← MODIFIED
    - Remove: VoiceChangerType dropdown (always RVC now)
    - Keep:   Model: [select file]
              Index: [select file]
              [upload] button (existing file-upload path)
    - Add:    [Upload Model via URL] button (new)
    ↓ click "Upload Model via URL"
URLUploader sub-screen (NEW, inside same modal)
    - Info banner: "Supported: Google Drive, HuggingFace, Pixeldrain"
    - Input:  URL text box
    - Buttons: [Upload via URL]   [<< back]
    ↓ click "Upload via URL"
    - Show inline progress: "Downloading... 42%"
    - On success → auto-close → return to ModelSlotConfiguration (Main)
    - On error   → inline error banner: "Failed to upload model. <human-readable reason>"
```

---

## Changes Required

### 1. Backend — New `UrlModelDownloader.py`

**File:** `server/downloader/UrlModelDownloader.py` (NEW)

Mirrors Applio's model_download.py logic, adapted for voice-changer's slot system.

```
download_model_from_url(url, slot, model_dir, progress_callback)
    ├─ detect host:
    │   ├─ drive.google.com  → gdown.download(url)
    │   ├─ huggingface.co
    │   │   ├─ /blob/ or /resolve/ → replace /blob/→/resolve/ → requests.get(stream)
    │   │   └─ /tree/main          → scrape page for .zip → requests.get(stream)
    │   ├─ pixeldrain.com    → pixeldrain.com/u/ID → pixeldrain.com/api/file/ID?download
    │   └─ else              → raise ValueError("Unsupported host.")
    ├─ stream to logs/zips/<filename>, update progress_callback(0-100)
    ├─ if .zip  → zipfile.extractall → model_dir/<slot>/
    │              clean_extracted_files() (flatten subfolder, rename .pth/.index)
    ├─ if .pth/.onnx/.index → move directly to model_dir/<slot>/
    ├─ RVCModelSlotGenerator.loadModel(params)
    └─ modelSlotManager.save_model_slot(slot, slotInfo)
```

**Error handling — human-readable, NO traceback in logs:**

| Condition | Log (logger.error) | Client msg |
|---|---|---|
| HTTP 404 | `[UrlDownloader] File not found: {url}` | "File not found. The link may be broken or deleted." |
| HTTP 403 | `[UrlDownloader] Access denied: {url}` | "Access denied. The file may be private or require login." |
| Unsupported host | `[UrlDownloader] Unsupported host: {host}` | "Unsupported host. Use Google Drive, HuggingFace, or Pixeldrain." |
| No .pth after extract | `[UrlDownloader] No model file in archive` | "No model file (.pth/.onnx) found inside the archive." |
| Timeout | `[UrlDownloader] Timeout: {url}` | "Download timed out. Check your connection and try again." |
| Generic | `[UrlDownloader] {type(e).__name__}: {e}` | "An unexpected error occurred. Check server logs." |

---

### 2. Backend — VoiceChangerManager additions

**File:** `server/voice_changer/VoiceChangerManager.py`

- Add module-level `_url_download_status: dict[int, dict]` for progress tracking:
  ```python
  # { slot: {"progress": 0-100, "status": "idle|downloading|done|error", "msg": ""} }
  ```
- Add method `download_model_from_url(url: str, slot: int)`:
  - Runs `UrlModelDownloader.download_model_from_url(...)` in a background thread
  - Passes a progress callback that writes to `_url_download_status[slot]`
  - Sets status to `"done"` or `"error"` when complete
- Add method `get_url_download_status(slot: int) -> dict`

---

### 3. Backend — REST endpoints

**File:** `server/restapi/MMVC_Rest_Fileuploader.py`

- `POST /download_model_url`
  - Body: `url: str (Form)`, `slot: int (Form)`
  - Kicks off background download, returns `{"status": "OK", "msg": "Download started"}`
- `GET /download_model_url_status`
  - Query param: `slot: int`
  - Returns: `{"progress": N, "status": "...", "msg": "..."}`

---

### 4. Frontend — New client methods

**File:** `client/lib/src/client/ServerRestClient.ts`

```ts
downloadModelFromUrl = async (url: string, slot: number) => {
    const formData = new FormData();
    formData.append("url", url);
    formData.append("slot", String(slot));
    const res = await fetch(this.serverUrl + "/download_model_url", { method: "POST", body: formData });
    return await res.json();
};

getUrlDownloadStatus = async (slot: number) => {
    const res = await fetch(`${this.serverUrl}/download_model_url_status?slot=${slot}`);
    return await res.json();
};
```

**File:** `client/lib/src/hooks/useServerSetting.ts`

- Expose both new methods in `ServerSettingState`.

---

### 5. Frontend — FileUploader modal changes

**File:** `client/demo/src/components/demo/904-3_FileUploader.tsx`

**Changes:**
- Remove `VoiceChangerType` dropdown (always RVC, no need to surface it)
- Add `[Upload Model via URL]` button next to existing `[upload]` button
- Add local state: `subScreen: "FileUploader" | "URLUploader"`
- When `subScreen === "URLUploader"`, render:

```
┌──────────────────────────────────────────┐
│  File Uploader                           │
├──────────────────────────────────────────┤
│  Upload Model via URL       [<< back]   │
│                                          │
│  ℹ Supported sources:                   │
│    • Google Drive                        │
│    • HuggingFace                         │
│    • Pixeldrain                          │
│                                          │
│  URL: [______________________________]   │
│                                          │
│  [  Upload via URL  ]                    │
│                                          │
│  ████████░░░░░░░  42%    (while active) │
│                                          │
│  ❌ Failed: <reason>   (on error)        │
└──────────────────────────────────────────┘
```

**URL upload logic (polling):**
```tsx
const handleUrlUpload = async () => {
    setUrlUploadStatus("downloading");
    setUrlProgress(0);
    setUrlError("");
    await voiceChangerClient.downloadModelFromUrl(url, props.targetIndex);
    const poll = setInterval(async () => {
        const data = await voiceChangerClient.getUrlDownloadStatus(props.targetIndex);
        setUrlProgress(data.progress);
        if (data.status === "done") {
            clearInterval(poll);
            setUrlUploadStatus("idle");
            props.backToSlotManager();
        } else if (data.status === "error") {
            clearInterval(poll);
            setUrlUploadStatus("idle");
            setUrlError(data.msg);
        }
    }, 500);
};
```

---

## Pixeldrain URL Conversion

```
https://pixeldrain.com/u/FILEID
    →  https://pixeldrain.com/api/file/FILEID?download
```
Parse with: `re.search(r'pixeldrain\.com/u/([A-Za-z0-9]+)', url)`

---

## File Change Summary

| File | Type | Change |
|---|---|---|
| `server/downloader/UrlModelDownloader.py` | **NEW** | URL download + extract + slot placement |
| `server/voice_changer/VoiceChangerManager.py` | Modify | `download_model_from_url()` + progress dict |
| `server/restapi/MMVC_Rest_Fileuploader.py` | Modify | 2 new routes: POST + GET |
| `client/lib/src/client/ServerRestClient.ts` | Modify | 2 new HTTP methods |
| `client/lib/src/hooks/useServerSetting.ts` | Modify | Expose new methods |
| `client/demo/src/components/demo/904-3_FileUploader.tsx` | Modify | Remove dropdown; URL sub-screen + progress UI |

---

## Implementation Order

1. `UrlModelDownloader.py`
2. `VoiceChangerManager.py`
3. `MMVC_Rest_Fileuploader.py`
4. `ServerRestClient.ts`
5. `useServerSetting.ts`
6. `904-3_FileUploader.tsx`

## Rule

Don't use subagent for saving antigravity tokens