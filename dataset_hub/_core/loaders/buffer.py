from dataclasses import dataclass
from typing import Dict, Type, TypeVar


@dataclass
class Buffer:
    name: str
    data: bytes


BufferT = TypeVar("BufferT", bound=Buffer)


@dataclass
class AudioBuffer(Buffer):
    sample_rate: int
    channels: int
    duration: float
    format: str


@dataclass
class ImageBuffer(Buffer):
    width: int
    height: int
    channels: int
    format: str


@dataclass
class ArchiveBuffer(Buffer):
    """Buffer for archive-like data (zip, tar, etc.).

    Currently no additional fields are required, but class exists
    to distinguish archive buffers from generic buffers.
    """

    pass


class BufferFactory:
    """Factory that picks a Buffer subclass based on file extension.

    The build API is intentionally minimal: callers buffers `name`
    (filename) and `data` (bytes). Both must be non-empty. The factory
    chooses a concrete Buffer class from a small extension-based
    registry and returns an instance of it.
    """

    _REGISTRY: Dict[str, Type[Buffer]] = {
        "zip": ArchiveBuffer,
        "tar": ArchiveBuffer,
        "gz": ArchiveBuffer,
        "tgz": ArchiveBuffer,
        "7z": ArchiveBuffer,
        "csv": Buffer,
    }

    @classmethod
    def build(cls, name: str, data: bytes) -> Buffer:
        """Create a Buffer (or subclass) for the given filename and bytes.

        Args:
            name: Filename including extension (must be non-empty).
            data: Raw bytes (must be non-empty).

        Returns:
            Buffer: Instance of a Buffer subclass selected by extension.

        Raises:
            ValueError: If `name` or `data` are empty.
        """
        if not name or not isinstance(name, str):
            raise ValueError("buffer name must be a non-empty string")
        if not data or not isinstance(data, (bytes, bytearray)):
            raise ValueError("buffer data must be non-empty bytes")

        # Quick extension detection (use last suffix)
        ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""

        buffer = cls._REGISTRY[ext]

        return buffer(name=name, data=bytes(data))
