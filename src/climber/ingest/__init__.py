"""Content ingestion modules."""

from .base import BaseIngester, ContentItem
from .web import WebIngester
from .file import FileIngester

def create_ingester(source: str) -> BaseIngester:
    """Create appropriate ingester based on source type."""
    if source.startswith(("http://", "https://")):
        return WebIngester(source)
    else:
        return FileIngester(source)

__all__ = ["BaseIngester", "ContentItem", "WebIngester", "FileIngester", "create_ingester"]