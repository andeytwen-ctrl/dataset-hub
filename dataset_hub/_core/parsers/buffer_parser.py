from abc import ABC
from typing import Any, Dict, Generic

from dataset_hub._core.data_bundle import UserDataT
from dataset_hub._core.packagers.buffer_packager import BufferPackT


class BufferParser(ABC, Generic[BufferPackT, UserDataT]):

    def __init__(self, config: Dict[str, Any]) -> None:
        pass

    def parse(self, buffer_pack: BufferPackT) -> None:  # TODO rename this
        return None
