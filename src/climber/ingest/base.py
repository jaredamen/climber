"""Base ingester interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class ContentItem:
    """A piece of content with metadata."""

    text: str
    title: Optional[str] = None
    source: Optional[str] = None
    content_type: str = "text"
    metadata: dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BaseIngester(ABC):
    """Base class for content ingesters."""

    def __init__(self, source: str):
        self.source = source

    @abstractmethod
    def ingest(self) -> ContentItem:
        """Ingest content from the source."""
        pass

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        # Remove excessive whitespace
        text = " ".join(text.split())

        # Remove citation markers [1], [2], etc.
        import re

        text = re.sub(r"\[\d+\]", "", text)

        # Remove extra punctuation patterns
        text = re.sub(r"\.{2,}", "...", text)
        text = re.sub(r"\s+", " ", text)

        return text.strip()
