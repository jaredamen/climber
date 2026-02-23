"""Prompt templates for different output types and presets."""

from .briefing import get_briefing_prompt
from .flashcards import get_flashcards_prompt
from .audio_script import get_audio_script_prompt


def get_prompt_template(output_type: str, preset: str) -> str:
    """Get prompt template for the specified output type and preset."""
    if output_type == "briefing":
        return get_briefing_prompt(preset)
    elif output_type == "flashcards":
        return get_flashcards_prompt(preset)
    elif output_type == "audio-script":
        return get_audio_script_prompt(preset)
    else:
        raise ValueError(f"Unsupported output type: {output_type}")


__all__ = ["get_prompt_template"]