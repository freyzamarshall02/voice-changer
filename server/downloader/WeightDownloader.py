import os
import urllib.request

from downloader.Downloader import download_all
from mods.log_control import VoiceChangaerLogger
from voice_changer.utils.VoiceChangerParams import VoiceChangerParams
from Exceptions import WeightDownladException

logger = VoiceChangaerLogger.get_instance().getLogger()

# URLs for the HuggingFace-format contentvec embedder (Applio's load_embedding() sources)
_CONTENTVEC_BIN_URL = (
    "https://huggingface.co/IAHispano/Applio/resolve/main/Resources/embedders/contentvec/pytorch_model.bin"
)
_CONTENTVEC_CFG_URL = (
    "https://huggingface.co/IAHispano/Applio/resolve/main/Resources/embedders/contentvec/config.json"
)


def _download_file(url: str, dest: str):
    """Download a single file from url to dest using urllib."""
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    logger.info(f"Downloading {url} -> {dest}")
    urllib.request.urlretrieve(url, dest)


def _ensure_contentvec(model_dir: str):
    """
    Ensure the HuggingFace-format contentvec model directory exists.
    Downloads pytorch_model.bin and config.json from Applio's HuggingFace
    repo if either is missing.

    Args:
        model_dir: Path to the model directory (e.g. 'pretrain/contentvec').
    """
    bin_path = os.path.join(model_dir, "pytorch_model.bin")
    cfg_path = os.path.join(model_dir, "config.json")

    if not os.path.exists(bin_path):
        _download_file(_CONTENTVEC_BIN_URL, bin_path)
    if not os.path.exists(cfg_path):
        _download_file(_CONTENTVEC_CFG_URL, cfg_path)


def downloadWeight(voiceChangerParams: VoiceChangerParams):
    content_vec_500_onnx = voiceChangerParams.content_vec_500_onnx
    hubert_base = voiceChangerParams.hubert_base          # now a directory path
    hubert_base_jp = voiceChangerParams.hubert_base_jp
    crepe_onnx_full = voiceChangerParams.crepe_onnx_full
    crepe_onnx_tiny = voiceChangerParams.crepe_onnx_tiny
    rmvpe = voiceChangerParams.rmvpe
    rmvpe_onnx = voiceChangerParams.rmvpe_onnx
    whisper_tiny = voiceChangerParams.whisper_tiny

    # ── HuggingFace-format contentvec (hubert_base + content_vec_500 share same dir) ──
    # hubert_base is now a directory path (e.g. pretrain/contentvec).
    # Both --hubert_base and --content_vec_500 default to the same dir.
    try:
        _ensure_contentvec(hubert_base)
    except Exception as e:
        logger.error(f"[WeightDownloader] Failed to download contentvec model: {e}")
        raise WeightDownladException()

    # ── Other single-file weights ──
    downloadParams = []

    # JP model: download HuggingFace-format files into the dir pointed to by hubert_base_jp
    jp_bin = os.path.join(hubert_base_jp, "pytorch_model.bin")
    jp_cfg = os.path.join(hubert_base_jp, "config.json")
    if not os.path.exists(jp_bin):
        try:
            _download_file(
                "https://huggingface.co/IAHispano/Applio/resolve/main/Resources/embedders/japanese_hubert_base/pytorch_model.bin",
                jp_bin,
            )
        except Exception as e:
            logger.warning(f"[WeightDownloader] Failed to download JP HuBERT bin: {e}")
    if not os.path.exists(jp_cfg):
        try:
            _download_file(
                "https://huggingface.co/IAHispano/Applio/resolve/main/Resources/embedders/japanese_hubert_base/config.json",
                jp_cfg,
            )
        except Exception as e:
            logger.warning(f"[WeightDownloader] Failed to download JP HuBERT config: {e}")

    if os.path.exists(crepe_onnx_full) is False:
        downloadParams.append(
            {
                "url": "https://huggingface.co/wok000/weights/resolve/main/crepe/onnx/full.onnx",
                "saveTo": crepe_onnx_full,
                "position": 5,
            }
        )
    if os.path.exists(crepe_onnx_tiny) is False:
        downloadParams.append(
            {
                "url": "https://huggingface.co/wok000/weights/resolve/main/crepe/onnx/tiny.onnx",
                "saveTo": crepe_onnx_tiny,
                "position": 6,
            }
        )

    if os.path.exists(content_vec_500_onnx) is False:
        downloadParams.append(
            {
                "url": "https://huggingface.co/wok000/weights_gpl/resolve/main/content-vec/contentvec-f.onnx",
                "saveTo": content_vec_500_onnx,
                "position": 7,
            }
        )
    if os.path.exists(rmvpe) is False:
        downloadParams.append(
            {
                "url": "https://huggingface.co/wok000/weights/resolve/main/rmvpe/rmvpe_20231006.pt",
                "saveTo": rmvpe,
                "position": 8,
            }
        )
    if os.path.exists(rmvpe_onnx) is False:
        downloadParams.append(
            {
                "url": "https://huggingface.co/wok000/weights_gpl/resolve/main/rmvpe/rmvpe_20231006.onnx",
                "saveTo": rmvpe_onnx,
                "position": 9,
            }
        )

    if os.path.exists(whisper_tiny) is False:
        downloadParams.append(
            {
                "url": "https://openaipublic.azureedge.net/main/whisper/models/65147644a518d12f04e32d6f3b26facc3f8dd46e5390956a9424a650c0ce22b9/tiny.pt",
                "saveTo": whisper_tiny,
                "position": 10,
            }
        )

    download_all(downloadParams, label="Downloading pretrain weights")

    # Validate contentvec dir is present (both files required)
    bin_path = os.path.join(hubert_base, "pytorch_model.bin")
    cfg_path = os.path.join(hubert_base, "config.json")
    if not os.path.exists(bin_path) or not os.path.exists(cfg_path):
        logger.error(f"[WeightDownloader] contentvec model incomplete in '{hubert_base}'")
        raise WeightDownladException()

    # Log contentvec dir file sizes
    for f in (bin_path, cfg_path):
        logger.debug(f"weight file [{f}]: {os.path.getsize(f)}")

    # Soft-warn if JP model is missing (optional embedder, not a hard fail)
    jp_bin_check = os.path.join(hubert_base_jp, "pytorch_model.bin")
    if not os.path.exists(jp_bin_check):
        logger.warning(f"[WeightDownloader] JP HuBERT model missing at '{hubert_base_jp}' — Japanese voice conversion will be unavailable.")

    # ファイルサイズをログに書き込む。（デバッグ用）
    single_file_weights = [
        content_vec_500_onnx,
        crepe_onnx_full,
        crepe_onnx_tiny,
        rmvpe,
        whisper_tiny,
    ]
    for weight in single_file_weights:
        if os.path.exists(weight):
            file_size = os.path.getsize(weight)
            logger.debug(f"weight file [{weight}]: {file_size}")
        else:
            logger.warning(f"weight file is missing. {weight}")
            raise WeightDownladException()

