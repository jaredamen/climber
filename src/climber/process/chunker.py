"""Content chunking for LLM consumption."""

from typing import List
from ..ingest.base import ContentItem


class ContentChunker:
    """Chunk content for optimal LLM processing."""
    
    def __init__(self, max_chunk_size: int = 4000, overlap: int = 200):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
    
    def chunk(self, content: ContentItem) -> List[str]:
        """Chunk content into manageable pieces."""
        text = content.text
        
        # If content is small enough, return as single chunk
        if len(text) <= self.max_chunk_size:
            return [text]
        
        chunks = []
        current_pos = 0
        
        while current_pos < len(text):
            # Find the end of the chunk
            chunk_end = current_pos + self.max_chunk_size
            
            if chunk_end >= len(text):
                # Last chunk
                chunks.append(text[current_pos:])
                break
            
            # Try to break at sentence boundary
            sentence_end = text.rfind('.', current_pos, chunk_end)
            if sentence_end == -1:
                # Try paragraph boundary
                sentence_end = text.rfind('\n\n', current_pos, chunk_end)
            
            if sentence_end == -1:
                # Try any whitespace
                sentence_end = text.rfind(' ', current_pos, chunk_end)
            
            if sentence_end == -1 or sentence_end <= current_pos:
                # Force break at max size
                sentence_end = chunk_end
            else:
                sentence_end += 1  # Include the delimiter
            
            chunks.append(text[current_pos:sentence_end])
            current_pos = max(current_pos + 1, sentence_end - self.overlap)
        
        return [chunk.strip() for chunk in chunks if chunk.strip()]