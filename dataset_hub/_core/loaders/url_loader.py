from urllib.parse import urlparse

import requests

from .buffer import Buffer, BufferFactory
from .source_loader import SourceLoader


class UrlLoader(SourceLoader):
    """Loader for downloading data from HTTP/HTTPS URLs."""

    def __init__(self, url: str) -> None:
        """Initialize URL loader.

        Args:
            url: The URL to download from.

        Raises:
            ValueError: If URL is empty or invalid.
        """
        if not url or not isinstance(url, str):
            raise ValueError("URL must be a non-empty string")
        self.url = url

    def load(self) -> Buffer:
        """Download data from URL and return as a Buffer subclass.

        Returns:
            Buffer: The downloaded data wrapped by a Buffer subclass.
        """
        try:
            response = requests.get(self.url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            raise requests.RequestException(
                f"Failed to download from {self.url}: {e}"
            ) from e

        if not response.content:
            raise ValueError(f"Empty response from {self.url}")

        # Extract filename from URL (we assume caller-provided URLs include a filename)
        name = self._extract_filename(self.url)
        if not name:
            raise ValueError("URL must contain a filename")

        buffer = BufferFactory.build(name, response.content)
        return buffer

    @staticmethod
    def _extract_filename(url: str) -> str:
        """Extract filename from URL path.

        Args:
            url: The URL to extract filename from.

        Returns:
            str: Extracted filename or 'downloaded_file' if not found.
        """
        path = urlparse(url).path
        if path:
            return path.split("/")[-1]
        return ""
