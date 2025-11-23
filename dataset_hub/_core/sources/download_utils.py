from pathlib import Path
import requests


def url2file(url: str, save_path: Path) -> None:
    """
    Load file using HTTP/HTTPS URL.

    Args:
    - url: url link to download file from
    - save_path: Path where to save the downloaded file
    """
    resp = requests.get(url)
    resp.raise_for_status()
    save_path.write_bytes(resp.content)
