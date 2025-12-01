from typing import Any, Dict, Generic, Type, TypeVar
from dataclasses import dataclass, field

@dataclass
class Buffer:
    name: str
    data: bytes

BufferT = TypeVar("BufferT", bound=Buffer)

