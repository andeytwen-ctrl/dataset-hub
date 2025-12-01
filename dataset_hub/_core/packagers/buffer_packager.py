from abc import ABC, abstractmethod
from typing import Dict, Generic, TypeVar

from dataset_hub._core.loaders.buffer import Buffer

BufferPackT = TypeVar("BufferPackT")


class BufferPackager(ABC, Generic[BufferPackT]):

    @abstractmethod
    def package(self, buffers: Dict[str, Buffer]) -> None:
        pass
