"""Audio script output formatter."""

from typing import Dict, Any
from .base import BaseFormatter


class AudioScriptFormatter(BaseFormatter):
    """Format audio script output."""
    
    @property
    def file_extension(self) -> str:
        """Get the file extension for audio scripts."""
        return "txt"
    
    def format(self, result: Dict[str, Any]) -> str:
        """Format audio script result as structured text."""
        content = result.get("content", "")
        title = result.get("title", "Audio Script")
        source = result.get("source", "Unknown")
        
        output = f"AUDIO SCRIPT: {title}\n"
        output += "=" * len(f"AUDIO SCRIPT: {title}") + "\n\n"
        
        if source and source != "Unknown":
            output += f"Source: {source}\n"
        
        output += f"Estimated Duration: 5-10 minutes\n"
        output += f"Format: Educational/Conversational\n\n"
        
        output += "SCRIPT:\n"
        output += "-------\n\n"
        output += content
        
        if result.get("chunk_count", 1) > 1:
            output += f"\n\n[Generated from {result['chunk_count']} content sections]"
        
        output += "\n\n" + "END OF SCRIPT"
        
        return output