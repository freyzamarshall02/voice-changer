import os
import re
import shutil
import zipfile
from typing import Callable

import requests

from mods.log_control import VoiceChangaerLogger
from voice_changer.ModelSlotManager import ModelSlotManager

logger = VoiceChangaerLogger.get_instance().getLogger()

# Directory used to store downloaded zip/model files before extraction
_DOWNLOAD_TMP_DIR = os.path.join("logs", "zips")


def _ensure_download_dir() -> str:
    os.makedirs(_DOWNLOAD_TMP_DIR, exist_ok=True)
    return _DOWNLOAD_TMP_DIR


def _build_download_url(url: str) -> str:
    """Normalise / convert URL to a direct-download endpoint."""
    # HuggingFace: /blob/ → /resolve/
    if "huggingface.co" in url:
        return url.replace("/blob/", "/resolve/")

    # Pixeldrain: /u/FILEID → /api/file/FILEID?download
    pd_match = re.search(r"pixeldrain\.com/u/([A-Za-z0-9]+)", url)
    if pd_match:
        file_id = pd_match.group(1)
        return f"https://pixeldrain.com/api/file/{file_id}?download"

    return url


def _stream_download(url: str, dest_path: str, progress_callback: Callable[[int], None]) -> None:
    """Stream-download *url* to *dest_path*, calling progress_callback(0-99) as bytes arrive."""
    try:
        with requests.get(url, stream=True, timeout=60) as r:
            if r.status_code == 404:
                logger.error(f"[UrlDownloader] File not found: {url}")
                raise ValueError("File not found. The link may be broken or deleted.")
            if r.status_code == 403:
                logger.error(f"[UrlDownloader] Access denied: {url}")
                raise ValueError("Access denied. The file may be private or require login.")
            r.raise_for_status()

            total = int(r.headers.get("content-length", 0))
            downloaded = 0
            with open(dest_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total > 0:
                            pct = int(downloaded / total * 90)  # reserve 10% for extraction
                            progress_callback(pct)
    except requests.exceptions.Timeout:
        logger.error(f"[UrlDownloader] Timeout: {url}")
        raise ValueError("Download timed out. Check your connection and try again.")


def _is_zip_file(path: str) -> bool:
    """Return True if the file at *path* has a ZIP magic header (PK\\x03\\x04)."""
    try:
        with open(path, "rb") as f:
            return f.read(4) == b"PK\x03\x04"
    except OSError:
        return False


def _clean_extracted_files(extract_dir: str) -> None:
    """Recursively flatten all subdirectories: move every file into extract_dir root."""
    changed = True
    while changed:
        changed = False
        for entry in list(os.scandir(extract_dir)):
            if entry.is_dir():
                for sub_entry in os.scandir(entry.path):
                    dest = os.path.join(extract_dir, sub_entry.name)
                    if not os.path.exists(dest):
                        shutil.move(sub_entry.path, dest)
                        changed = True
                try:
                    shutil.rmtree(entry.path, ignore_errors=True)
                except OSError:
                    pass


def download_model_from_url(
    url: str,
    slot: int,
    model_dir: str,
    progress_callback: Callable[[int], None],
) -> None:
    """Download a model from *url* and place it into *model_dir*/<slot>.

    Supported sources:
      • Google Drive  (via gdown)
      • HuggingFace   (direct / /resolve/ links)
      • Pixeldrain     (pixeldrain.com/u/ID)

    Archives (.zip) are extracted and flattened.
    Individual files (.pth / .onnx / .index) are moved directly.

    Raises ValueError with a human-readable message on expected failure.
    """
    from urllib.parse import urlparse

    host = urlparse(url).hostname or ""

    slot_dir = os.path.join(model_dir, str(slot))
    os.makedirs(slot_dir, exist_ok=True)
    tmp_dir = _ensure_download_dir()

    progress_callback(0)

    # ── Google Drive ──────────────────────────────────────────────────────────
    if "drive.google.com" in host:
        try:
            import gdown  # type: ignore
        except ImportError:
            raise ValueError("gdown is not installed. Run: pip install gdown")

        # gdown expects the file-ID form; let it handle conversion
        tmp_path = os.path.join(tmp_dir, f"gdrive_slot{slot}")
        try:
            out = gdown.download(url, tmp_path, quiet=True, fuzzy=True)
        except Exception as e:
            logger.error(f"[UrlDownloader] {type(e).__name__}: {e}")
            raise ValueError("An unexpected error occurred. Check server logs.")
        if out is None:
            logger.error(f"[UrlDownloader] gdown returned None for: {url}")
            # gdown may have created a partial file; clean it up
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            raise ValueError("Access denied. The file may be private or require login.")
        downloaded_path = out
        progress_callback(90)

    # ── HuggingFace / Pixeldrain / generic HTTP ───────────────────────────────
    elif any(s in host for s in ("huggingface.co", "pixeldrain.com")):
        dl_url = _build_download_url(url)
        filename = os.path.basename(dl_url.split("?")[0]) or f"model_slot{slot}.bin"
        downloaded_path = os.path.join(tmp_dir, filename)
        _stream_download(dl_url, downloaded_path, progress_callback)
        progress_callback(90)

    else:
        logger.error(f"[UrlDownloader] Unsupported host: {host}")
        raise ValueError("Unsupported host. Use Google Drive, HuggingFace, or Pixeldrain.")

    # ── Determine what was downloaded and place it ────────────────────────────
    ext = os.path.splitext(downloaded_path)[1].lower()

    # Use magic bytes to detect zips — gdown gives files with no extension
    if ext == ".zip" or _is_zip_file(downloaded_path):
        # Extract to a temp sub-dir, then clean & move files
        extract_tmp = os.path.join(tmp_dir, f"extract_slot{slot}")
        os.makedirs(extract_tmp, exist_ok=True)
        with zipfile.ZipFile(downloaded_path, "r") as zf:
            zf.extractall(extract_tmp)
        os.remove(downloaded_path)
        _clean_extracted_files(extract_tmp)

        # Verify at least one model file is present
        model_files = [
            f for f in os.listdir(extract_tmp) if f.endswith((".pth", ".onnx"))
        ]
        if not model_files:
            logger.error("[UrlDownloader] No model file in archive")
            shutil.rmtree(extract_tmp, ignore_errors=True)
            raise ValueError("No model file (.pth/.onnx) found inside the archive.")

        # Move all extracted files into slot_dir
        for fname in os.listdir(extract_tmp):
            src = os.path.join(extract_tmp, fname)
            dst = os.path.join(slot_dir, fname)
            if os.path.exists(dst):
                os.remove(dst)
            shutil.move(src, dst)
        shutil.rmtree(extract_tmp, ignore_errors=True)

    elif ext in (".pth", ".onnx", ".index", ".bin"):
        dst = os.path.join(slot_dir, os.path.basename(downloaded_path))
        if os.path.exists(dst):
            os.remove(dst)
        shutil.move(downloaded_path, dst)

    else:
        # Unknown extension — try to move anyway and let slot generator decide
        dst = os.path.join(slot_dir, os.path.basename(downloaded_path))
        if os.path.exists(dst):
            os.remove(dst)
        shutil.move(downloaded_path, dst)

    # ── Generate slot metadata ────────────────────────────────────────────────
    progress_callback(95)

    model_files_in_slot = [f for f in os.listdir(slot_dir) if f.endswith((".pth", ".onnx"))]
    if not model_files_in_slot:
        logger.error("[UrlDownloader] No model file in archive")
        raise ValueError("No model file (.pth/.onnx) found inside the archive.")

    model_filename = model_files_in_slot[0]
    index_files_in_slot = [f for f in os.listdir(slot_dir) if f.endswith((".index", ".bin"))]
    index_filename = index_files_in_slot[0] if index_files_in_slot else ""

    from voice_changer.RVC.RVCModelSlotGenerator import RVCModelSlotGenerator
    from voice_changer.utils.LoadModelParams import LoadModelParamFile, LoadModelParams

    load_params = LoadModelParams(
        voiceChangerType="RVC",
        slot=slot,
        isSampleMode=False,
        sampleId="",
        files=[
            LoadModelParamFile(name=model_filename, kind="rvcModel", dir=""),
            *(
                [LoadModelParamFile(name=index_filename, kind="rvcIndex", dir="")]
                if index_filename
                else []
            ),
        ],
        params={},
    )

    try:
        slot_info = RVCModelSlotGenerator.loadModel(load_params)
    except Exception as e:
        logger.error(f"[UrlDownloader] {type(e).__name__}: {e}")
        raise ValueError("An unexpected error occurred. Check server logs.")

    model_slot_manager = ModelSlotManager.get_instance(model_dir)
    model_slot_manager.save_model_slot(slot, slot_info)

    progress_callback(100)
