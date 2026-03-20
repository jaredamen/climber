"""Tests for content chunker."""

from climber.ingest.base import ContentItem
from climber.process.chunker import ContentChunker


class TestContentChunker:

    def test_init(self):
        """Test ContentChunker initialization."""
        chunker = ContentChunker(max_chunk_size=1000, overlap=100)
        assert chunker.max_chunk_size == 1000
        assert chunker.overlap == 100

    def test_init_defaults(self):
        """Test ContentChunker with default values."""
        chunker = ContentChunker()
        assert chunker.max_chunk_size == 4000
        assert chunker.overlap == 200

    def test_chunk_small_content(self):
        """Test chunking content smaller than max size."""
        content = ContentItem(text="Short content that fits in one chunk.")
        chunker = ContentChunker(max_chunk_size=100)

        chunks = chunker.chunk(content)

        assert len(chunks) == 1
        assert chunks[0] == "Short content that fits in one chunk."

    def test_chunk_large_content(self, sample_content):
        """Test chunking large content."""
        # Create content larger than chunk size
        large_text = "This is a sentence. " * 100
        content = ContentItem(text=large_text)
        chunker = ContentChunker(max_chunk_size=100, overlap=20)

        chunks = chunker.chunk(content)

        assert len(chunks) > 1
        assert all(len(chunk) <= 120 for chunk in chunks)  # Allow for overlap
        assert all(chunk.strip() for chunk in chunks)  # No empty chunks

    def test_chunk_sentence_boundaries(self):
        """Test that chunking respects sentence boundaries."""
        text = "First sentence. Second sentence. Third sentence. Fourth sentence."
        content = ContentItem(text=text)
        chunker = ContentChunker(max_chunk_size=30, overlap=5)

        chunks = chunker.chunk(content)

        # Should break at sentence boundaries when possible
        assert len(chunks) >= 2
        for chunk in chunks:
            # Each chunk should end with a complete sentence (or be the last chunk)
            assert chunk.endswith('.') or chunk == chunks[-1]

    def test_chunk_paragraph_boundaries(self):
        """Test chunking with paragraph boundaries."""
        text = "First paragraph.\n\nSecond paragraph with more content.\n\nThird paragraph."
        content = ContentItem(text=text)
        chunker = ContentChunker(max_chunk_size=25, overlap=5)

        chunks = chunker.chunk(content)

        assert len(chunks) >= 2
        assert all(chunk.strip() for chunk in chunks)
