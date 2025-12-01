"""Unit tests for Buffer classes and BufferFactory."""

import pytest

from dataset_hub._core.loaders.buffer import (
    ArchiveBuffer,
    AudioBuffer,
    Buffer,
    BufferFactory,
    ImageBuffer,
)


class TestBufferClasses:
    """Tests for Buffer dataclass and its subclasses."""

    def test_buffer_creation(self) -> None:
        """Buffer creates with name and data."""
        buffer = Buffer(name="file.txt", data=b"content")
        assert buffer.name == "file.txt"
        assert buffer.data == b"content"

    def test_archive_buffer_creation(self) -> None:
        """ArchiveBuffer creates with name and data (inherits from Buffer)."""
        buffer = ArchiveBuffer(name="archive.zip", data=b"zip_content")
        assert buffer.name == "archive.zip"
        assert buffer.data == b"zip_content"
        assert isinstance(buffer, Buffer)
        assert isinstance(buffer, ArchiveBuffer)

    def test_audio_buffer_creation(self) -> None:
        """AudioBuffer creates with all required audio fields."""
        buffer = AudioBuffer(
            name="song.mp3",
            data=b"audio_data",
            sample_rate=44100,
            channels=2,
            duration=180.5,
            format="mp3",
        )
        assert buffer.name == "song.mp3"
        assert buffer.data == b"audio_data"
        assert buffer.sample_rate == 44100
        assert buffer.channels == 2
        assert buffer.duration == 180.5
        assert buffer.format == "mp3"

    def test_image_buffer_creation(self) -> None:
        """ImageBuffer creates with all required image fields."""
        buffer = ImageBuffer(
            name="photo.jpg",
            data=b"image_data",
            width=1920,
            height=1080,
            channels=3,
            format="jpg",
        )
        assert buffer.name == "photo.jpg"
        assert buffer.data == b"image_data"
        assert buffer.width == 1920
        assert buffer.height == 1080
        assert buffer.channels == 3
        assert buffer.format == "jpg"


class TestBufferFactory:
    """Tests for BufferFactory.build() method."""

    def test_build_archive_zip(self) -> None:
        """Factory builds ArchiveBuffer for .zip extension."""
        buffer = BufferFactory.build("data.zip", b"zip_content")
        assert isinstance(buffer, ArchiveBuffer)
        assert buffer.name == "data.zip"
        assert buffer.data == b"zip_content"

    def test_build_archive_tar(self) -> None:
        """Factory builds ArchiveBuffer for .tar extension."""
        buffer = BufferFactory.build("archive.tar", b"tar_content")
        assert isinstance(buffer, ArchiveBuffer)
        assert buffer.name == "archive.tar"

    def test_build_archive_gz(self) -> None:
        """Factory builds ArchiveBuffer for .gz extension."""
        buffer = BufferFactory.build("data.gz", b"gz_content")
        assert isinstance(buffer, ArchiveBuffer)
        assert buffer.name == "data.gz"

    def test_build_archive_tgz(self) -> None:
        """Factory builds ArchiveBuffer for .tgz extension."""
        buffer = BufferFactory.build("archive.tgz", b"tgz_content")
        assert isinstance(buffer, ArchiveBuffer)

    def test_build_archive_7z(self) -> None:
        """Factory builds ArchiveBuffer for .7z extension."""
        buffer = BufferFactory.build("archive.7z", b"7z_content")
        assert isinstance(buffer, ArchiveBuffer)

    def test_build_base_buffer_csv(self) -> None:
        """Factory builds base Buffer for .csv extension."""
        buffer = BufferFactory.build("data.csv", b"col1,col2\n1,2")
        assert isinstance(buffer, Buffer)
        assert type(buffer) is Buffer
        assert buffer.name == "data.csv"
        assert buffer.data == b"col1,col2\n1,2"

    def test_build_base_buffer_unknown_extension(self) -> None:
        """Factory raises KeyError for unknown extension."""
        with pytest.raises(KeyError):
            BufferFactory.build("data.json", b"json_content")

    def test_build_empty_name(self) -> None:
        """Factory raises ValueError for empty name."""
        with pytest.raises(ValueError, match="buffer name must be a non-empty string"):
            BufferFactory.build("", b"content")

    def test_build_none_name(self) -> None:
        """Factory raises ValueError for None name."""
        with pytest.raises(ValueError, match="buffer name must be a non-empty string"):
            BufferFactory.build(None, b"content")  # type: ignore

    def test_build_non_string_name(self) -> None:
        """Factory raises ValueError for non-string name."""
        with pytest.raises(ValueError, match="buffer name must be a non-empty string"):
            BufferFactory.build(123, b"content")  # type: ignore

    def test_build_empty_data(self) -> None:
        """Factory raises ValueError for empty data."""
        with pytest.raises(ValueError, match="buffer data must be non-empty bytes"):
            BufferFactory.build("file.csv", b"")

    def test_build_none_data(self) -> None:
        """Factory raises ValueError for None data."""
        with pytest.raises(ValueError, match="buffer data must be non-empty bytes"):
            BufferFactory.build("file.csv", None)  # type: ignore

    def test_build_non_bytes_data(self) -> None:
        """Factory raises ValueError for non-bytes data."""
        with pytest.raises(ValueError, match="buffer data must be non-empty bytes"):
            BufferFactory.build("file.csv", "string_content")  # type: ignore

    def test_build_bytearray_data(self) -> None:
        """Factory accepts bytearray as data and converts to bytes."""
        buffer = BufferFactory.build("file.csv", bytearray(b"content"))  # type: ignore
        assert buffer.data == b"content"
        assert isinstance(buffer.data, bytes)

    def test_build_case_insensitive_extension(self) -> None:
        """Factory extension matching is case-insensitive."""
        buffer1 = BufferFactory.build("data.ZIP", b"content")
        buffer2 = BufferFactory.build("data.Zip", b"content")
        buffer3 = BufferFactory.build("data.zip", b"content")
        assert isinstance(buffer1, ArchiveBuffer)
        assert isinstance(buffer2, ArchiveBuffer)
        assert isinstance(buffer3, ArchiveBuffer)

    def test_build_no_extension(self) -> None:
        """Factory raises KeyError when no extension found."""
        with pytest.raises(KeyError):
            BufferFactory.build("noextension", b"content")
