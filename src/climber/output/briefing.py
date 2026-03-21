"""Briefing output formatter."""

from typing import Any

from .base import BaseFormatter


class BriefingFormatter(BaseFormatter):
    """Format briefing output."""

    @property
    def file_extension(self) -> str:
        """Get the file extension for briefings."""
        return "md"

    def format(self, result: dict[str, Any]) -> str:
        """Format briefing result as Markdown."""
        content = result.get("content", "")
        title = result.get("title", "Briefing")
        source = result.get("source", "Unknown")

        output = f"# {title}\n\n"

        if source and source != "Unknown":
            output += f"**Source:** {source}\n\n"

        output += "## Executive Summary\n\n"
        output += content

        if result.get("chunk_count", 1) > 1:
            output += (
                f"\n\n---\n*Generated from {result['chunk_count']} content sections*"
            )

        return output
