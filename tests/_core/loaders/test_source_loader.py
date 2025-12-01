"""Unit tests for SourceLoader base class."""

import pytest

from dataset_hub._core.loaders.buffer import Buffer
from dataset_hub._core.loaders.source_loader import SourceLoader


class TestSourceLoader:
    """Tests for abstract SourceLoader base class."""

    def test_source_loader_is_abstract(self) -> None:
        """SourceLoader cannot be instantiated directly."""
        with pytest.raises(TypeError):
            SourceLoader()  # type: ignore

    def test_source_loader_requires_load_method(self) -> None:
        """Subclass must implement load() method."""
        with pytest.raises(TypeError):

            class IncompleteLoader(SourceLoader):  # type: ignore
                pass

            IncompleteLoader()  # type: ignore

    def test_source_loader_concrete_implementation(self) -> None:
        """Concrete subclass with load() method instantiates properly."""

        class ConcreteLoader(SourceLoader[Buffer]):
            def load(self) -> Buffer:
                return Buffer(name="test", data=b"test_data")

        loader = ConcreteLoader()
        buffer = loader.load()
        assert buffer.name == "test"
        assert buffer.data == b"test_data"
        assert isinstance(buffer, Buffer)
