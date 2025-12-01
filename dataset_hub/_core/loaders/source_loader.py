from abc import ABC, abstractmethod

from .buffer import Buffer


class SourceLoader(ABC):
    """Base class for loading data sources into buffers."""

    @abstractmethod
    def load(self) -> Buffer:
        """Load data from source and return as buffer.

        Returns:
            Buffer: The loaded buffer data.
        """
        pass
