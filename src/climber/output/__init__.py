"""Output formatting modules."""

from .base import BaseFormatter
from .briefing import BriefingFormatter
from .flashcards import FlashcardsFormatter
from .audio_script import AudioScriptFormatter


def create_output_formatter(output_type: str) -> BaseFormatter:
    """Create output formatter based on type."""
    if output_type == "briefing":
        return BriefingFormatter()
    elif output_type == "flashcards":
        return FlashcardsFormatter()
    elif output_type == "audio-script":
        return AudioScriptFormatter()
    else:
        raise ValueError(f"Unsupported output type: {output_type}")


__all__ = ["BaseFormatter", "BriefingFormatter", "FlashcardsFormatter", "AudioScriptFormatter", "create_output_formatter"]