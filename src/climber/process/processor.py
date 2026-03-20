"""Main content processor using LLM providers."""

from typing import Any

from ..config import Config
from ..ingest.base import ContentItem
from .chunker import ContentChunker
from .prompts import get_prompt_template
from .providers import create_provider


class ContentProcessor:
    """Process content using LLM providers."""

    def __init__(self, config: Config):
        self.config = config
        self.chunker = ContentChunker()
        self.provider = create_provider(config)

    def process(self, content: ContentItem, output_type: str, preset: str) -> dict[str, Any]:
        """Process content and generate output."""
        # Chunk content for processing
        chunks = self.chunker.chunk(content)

        # Get prompt template for output type and preset
        prompt_template = get_prompt_template(output_type, preset)

        if len(chunks) == 1:
            # Single chunk processing
            return self._process_single_chunk(chunks[0], content, prompt_template, output_type)
        else:
            # Multi-chunk processing - summarize each chunk then combine
            return self._process_multiple_chunks(chunks, content, prompt_template, output_type)

    def _process_single_chunk(self, chunk: str, content: ContentItem,
                            prompt_template: str, output_type: str) -> dict[str, Any]:
        """Process a single content chunk."""
        # Format the prompt with content and metadata
        prompt = prompt_template.format(
            content=chunk,
            title=content.title or "Document",
            source=content.source or "Unknown"
        )

        # Get response from LLM provider
        response = self.provider.generate(prompt)

        return {
            "output_type": output_type,
            "content": response,
            "source": content.source,
            "title": content.title,
            "chunk_count": 1
        }

    def _process_multiple_chunks(self, chunks: list, content: ContentItem,
                               prompt_template: str, output_type: str) -> dict[str, Any]:
        """Process multiple content chunks and combine results."""
        chunk_results = []

        for i, chunk in enumerate(chunks):
            prompt = prompt_template.format(
                content=chunk,
                title=content.title or "Document",
                source=content.source or "Unknown",
                chunk_info=f" (Part {i+1} of {len(chunks)})"
            )

            response = self.provider.generate(prompt)
            chunk_results.append(response)

        # Combine chunk results
        if output_type == "briefing":
            combined_content = self._combine_briefings(chunk_results)
        elif output_type == "flashcards":
            combined_content = self._combine_flashcards(chunk_results)
        elif output_type == "audio-script":
            combined_content = self._combine_audio_scripts(chunk_results)
        else:
            combined_content = "\n\n".join(chunk_results)

        return {
            "output_type": output_type,
            "content": combined_content,
            "source": content.source,
            "title": content.title,
            "chunk_count": len(chunks)
        }

    def _combine_briefings(self, briefings: list) -> str:
        """Combine multiple briefing chunks into one."""
        # Use LLM to synthesize multiple briefings
        combine_prompt = f"""
Combine these briefing sections into a single, coherent 2-minute executive summary:

{chr(10).join(f"Section {i+1}: {briefing}" for i, briefing in enumerate(briefings))}

Create a unified briefing that covers all key points without redundancy.
"""
        return self.provider.generate(combine_prompt)

    def _combine_flashcards(self, flashcard_sets: list) -> str:
        """Combine multiple flashcard sets."""
        # Simply concatenate flashcard sets
        return "\n".join(flashcard_sets)

    def _combine_audio_scripts(self, scripts: list) -> str:
        """Combine multiple audio script sections."""
        combine_prompt = f"""
Combine these audio script sections into a single, coherent teaching script:

{chr(10).join(f"Section {i+1}: {script}" for i, script in enumerate(scripts))}

Create a unified script that flows naturally from one section to the next.
"""
        return self.provider.generate(combine_prompt)
