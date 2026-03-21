"""Base output formatter interface."""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseFormatter(ABC):
    """Base class for output formatters."""
    
    @property
    @abstractmethod
    def file_extension(self) -> str:
        """Get the file extension for this format."""
        pass
    
    @abstractmethod
    def format(self, result: Dict[str, Any]) -> str:
        """Format the processing result for output."""
        pass