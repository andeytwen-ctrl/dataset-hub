"""Unit tests for data loaders (SourceLoader and UrlLoader)."""

from unittest.mock import Mock, patch

import pytest
import requests

from dataset_hub._core.loaders.buffer import Buffer
from dataset_hub._core.loaders.url_loader import UrlLoader


class TestUrlLoader:
    """Tests for UrlLoader implementation."""

    def test_url_loader_init_valid_url(self) -> None:
        """UrlLoader initializes with valid URL."""
        loader = UrlLoader("https://example.com/data.csv")
        assert loader.url == "https://example.com/data.csv"

    def test_url_loader_init_empty_url(self) -> None:
        """UrlLoader raises ValueError with empty URL."""
        with pytest.raises(ValueError, match="URL must be a non-empty string"):
            UrlLoader("")

    def test_url_loader_init_none_url(self) -> None:
        """UrlLoader raises ValueError with None URL."""
        with pytest.raises(ValueError, match="URL must be a non-empty string"):
            UrlLoader(None)

    def test_url_loader_init_non_string_url(self) -> None:
        """UrlLoader raises ValueError with non-string URL."""
        with pytest.raises(ValueError, match="URL must be a non-empty string"):
            UrlLoader(123)

    @patch("dataset_hub._core.loaders.url_loader.requests.get")
    def test_url_loader_load_success(self, mock_get: Mock) -> None:
        """UrlLoader successfully loads data from URL."""
        test_data = b"test_content"
        mock_response = Mock()
        mock_response.content = test_data
        mock_get.return_value = mock_response

        loader = UrlLoader("https://example.com/data.csv")
        buffer = loader.load()

        # CSV files map to base Buffer type
        assert type(buffer) is Buffer
        assert buffer.data == test_data
        assert buffer.name == "data.csv"
        mock_get.assert_called_once_with("https://example.com/data.csv", timeout=30)

    @patch("dataset_hub._core.loaders.url_loader.requests.get")
    def test_url_loader_load_extracts_filename(self, mock_get: Mock) -> None:
        """UrlLoader extracts filename from URL correctly."""
        from dataset_hub._core.loaders.buffer import ArchiveBuffer

        test_data = b"content"
        mock_response = Mock()
        mock_response.content = test_data
        mock_get.return_value = mock_response

        loader = UrlLoader("https://example.com/path/to/myfile.zip")
        buffer = loader.load()

        assert buffer.name == "myfile.zip"
        assert isinstance(buffer, ArchiveBuffer)

    @patch("dataset_hub._core.loaders.url_loader.requests.get")
    def test_url_loader_load_empty_response(self, mock_get: Mock) -> None:
        """UrlLoader raises ValueError on empty response."""
        mock_response = Mock()
        mock_response.content = b""
        mock_get.return_value = mock_response

        loader = UrlLoader("https://example.com/data.csv")
        with pytest.raises(ValueError, match="Empty response"):
            loader.load()

    @patch("dataset_hub._core.loaders.url_loader.requests.get")
    def test_url_loader_load_http_error(self, mock_get: Mock) -> None:
        """UrlLoader handles HTTP errors properly."""
        mock_get.side_effect = requests.RequestException("Connection failed")

        loader = UrlLoader("https://example.com/data.csv")
        with pytest.raises(requests.RequestException, match="Failed to download"):
            loader.load()

    @patch("dataset_hub._core.loaders.url_loader.requests.get")
    def test_url_loader_load_timeout(self, mock_get: Mock) -> None:
        """UrlLoader respects timeout setting."""
        mock_get.side_effect = requests.Timeout("Request timed out")

        loader = UrlLoader("https://example.com/data.csv")
        with pytest.raises(requests.RequestException, match="Failed to download"):
            loader.load()

    @patch("dataset_hub._core.loaders.url_loader.requests.get")
    def test_url_loader_load_no_filename(self, mock_get: Mock) -> None:
        """UrlLoader raises ValueError when URL has no filename."""
        test_data = b"content"
        mock_response = Mock()
        mock_response.content = test_data
        mock_get.return_value = mock_response

        loader = UrlLoader("https://example.com/")
        with pytest.raises(ValueError, match="URL must contain a filename"):
            loader.load()

    @patch("dataset_hub._core.loaders.url_loader.requests.get")
    def test_url_loader_load_unsupported_extension(self, mock_get: Mock) -> None:
        """UrlLoader raises KeyError for unsupported file extension."""
        test_data = b"json_content"
        mock_response = Mock()
        mock_response.content = test_data
        mock_get.return_value = mock_response

        loader = UrlLoader("https://example.com/data.json")
        with pytest.raises(KeyError):
            loader.load()

    @patch("dataset_hub._core.loaders.url_loader.requests.get")
    def test_url_loader_load_archive_buffer(self, mock_get: Mock) -> None:
        """UrlLoader returns ArchiveBuffer for .zip files."""
        from dataset_hub._core.loaders.buffer import ArchiveBuffer

        test_data = b"zip_content"
        mock_response = Mock()
        mock_response.content = test_data
        mock_get.return_value = mock_response

        loader = UrlLoader("https://example.com/archive.zip")
        buffer = loader.load()

        assert isinstance(buffer, ArchiveBuffer)
        assert buffer.name == "archive.zip"
        assert buffer.data == test_data

    def test_extract_filename_with_extension(self) -> None:
        """Extract filename correctly from URL with file extension."""
        filename = UrlLoader._extract_filename("https://example.com/data/file.csv")
        assert filename == "file.csv"

    def test_extract_filename_multiple_directories(self) -> None:
        """Extract filename from deeply nested URL."""
        filename = UrlLoader._extract_filename("https://example.com/a/b/c/dataset.json")
        assert filename == "dataset.json"

    def test_extract_filename_with_query_params(self) -> None:
        """Extract filename ignoring query parameters."""
        filename = UrlLoader._extract_filename(
            "https://example.com/file.zip?token=abc123"
        )
        assert filename == "file.zip"

    def test_extract_filename_no_path(self) -> None:
        """Fallback to default name when no filename in path."""
        filename = UrlLoader._extract_filename("https://example.com/")
        assert filename == ""

    def test_extract_filename_no_extension(self) -> None:
        """Extract filename without extension."""
        filename = UrlLoader._extract_filename("https://example.com/data/myfile")
        assert filename == "myfile"

    def test_buffer_structure(self) -> None:
        """Buffer has correct structure with name and data fields."""
        buffer = Buffer(name="test.csv", data=b"content")
        assert buffer.name == "test.csv"
        assert buffer.data == b"content"
        assert isinstance(buffer.data, bytes)
