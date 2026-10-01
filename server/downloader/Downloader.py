import requests  # type: ignore
import os
from tqdm import tqdm

from mods.log_control import VoiceChangaerLogger

logger = VoiceChangaerLogger.get_instance().getLogger()


def download_all(params_list: list, label: str = "Downloading pretrain weights"):
    """Download all files sequentially under a single tqdm progress bar.

    Using parallel tqdm bars (one per file) in a non-TTY environment like
    Google Colab causes every \\r update to flush as a new log line, spamming
    hundreds of lines per download. This function avoids that entirely by
    driving one bar on the main thread while downloading files one-by-one.
    """
    if not params_list:
        return

    # HEAD pass — collect file sizes so the bar shows a meaningful total.
    # If a HEAD fails or returns no Content-Length, that file contributes 0
    # and the bar total will be adjusted live from the GET response.
    total_bytes = 0
    sizes: list[int] = []
    for p in params_list:
        try:
            r = requests.head(p["url"], allow_redirects=True, timeout=10)
            cl = r.headers.get("content-length")
            size = int(cl) if cl else 0
        except Exception:
            size = 0
        sizes.append(size)
        total_bytes += size

    with tqdm(
        total=total_bytes if total_bytes > 0 else None,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
        desc=label,
        dynamic_ncols=True,
    ) as bar:
        for i, p in enumerate(params_list):
            url = p["url"]
            saveTo = p["saveTo"]
            dirname = os.path.dirname(saveTo)
            if dirname:
                os.makedirs(dirname, exist_ok=True)

            filename = os.path.basename(saveTo)
            bar.set_description(f"{label} [{filename}]")

            try:
                req = requests.get(url, stream=True, allow_redirects=True)

                # If HEAD gave us no size, try to grab it from the GET headers
                # and adjust the bar total on the fly.
                if sizes[i] == 0:
                    cl = req.headers.get("content-length")
                    if cl:
                        extra = int(cl)
                        sizes[i] = extra
                        bar.total = (bar.total or 0) + extra
                        bar.refresh()

                with open(saveTo, "wb") as f:
                    for chunk in req.iter_content(chunk_size=65536):
                        if chunk:
                            f.write(chunk)
                            bar.update(len(chunk))

            except Exception as e:
                logger.warning(f"[Voice Changer] Failed to download {url}: {e}")

        bar.set_description(label)


def download_no_tqdm(params):
    """Download a single small file (e.g. JSON catalog) with no progress bar."""
    url = params["url"]
    saveTo = params["saveTo"]
    dirname = os.path.dirname(saveTo)
    if dirname != "":
        os.makedirs(dirname, exist_ok=True)
    try:
        req = requests.get(url, stream=True, allow_redirects=True)
        with open(saveTo, "wb") as f:
            for chunk in req.iter_content(chunk_size=65536):
                if chunk:
                    f.write(chunk)
        logger.info(f"[Voice Changer] download sample catalog. {saveTo}")
    except Exception as e:
        logger.warning(e)

