from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any, Dict, Generic, Type

class SourceLoader(ABC):

    def __init__(self, config: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def load(self) -> bytes:
        pass

