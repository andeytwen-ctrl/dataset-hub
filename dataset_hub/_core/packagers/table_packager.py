from typing import Dict

from dataset_hub._core.loaders.buffer import Buffer

from .buffer_packager import BufferPackager


class TableBufferPack:

    def __init__(self, buffers: Dict[str, Buffer]):
        self.data = buffers


class TableBufferPackager(BufferPackager[TableBufferPack]):

    def package(self, buffers: Dict[str, Buffer]) -> None:
        pass
