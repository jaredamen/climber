"""Flashcards output formatter."""

import json
from typing import Dict, Any
from .base import BaseFormatter


class FlashcardsFormatter(BaseFormatter):
    """Format flashcards output as JSON."""
    
    @property
    def file_extension(self) -> str:
        """Get the file extension for flashcards."""
        return "json"
    
    def format(self, result: Dict[str, Any]) -> str:
        """Format flashcards result as structured JSON."""
        content = result.get("content", "")
        title = result.get("title", "Flashcards")
        source = result.get("source", "Unknown")
        
        # Try to parse existing JSON from LLM response
        flashcards_data = self._extract_flashcards(content)
        
        # Create the final structure
        output_data = {
            "title": title,
            "source": source,
            "generated_at": "",  # Could add timestamp
            "format_version": "1.0",
            "flashcards": flashcards_data,
            "metadata": {
                "total_cards": len(flashcards_data),
                "chunk_count": result.get("chunk_count", 1)
            }
        }
        
        return json.dumps(output_data, indent=2)
    
    def _extract_flashcards(self, content: str) -> list:
        """Extract flashcards from LLM response."""
        try:
            # Try to parse JSON directly
            data = json.loads(content)
            if "flashcards" in data:
                return data["flashcards"]
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            # Parse from text format if JSON parsing fails
            return self._parse_text_flashcards(content)
    
    def _parse_text_flashcards(self, content: str) -> list:
        """Parse flashcards from text format as fallback."""
        flashcards = []
        lines = content.split('\n')
        
        current_card = {}
        in_question = False
        in_answer = False
        
        for line in lines:
            line = line.strip()
            
            if line.startswith("Q:") or line.startswith("Question:"):
                if current_card and "question" in current_card and "answer" in current_card:
                    flashcards.append(current_card)
                current_card = {"question": line.split(":", 1)[1].strip()}
                in_question = True
                in_answer = False
            elif line.startswith("A:") or line.startswith("Answer:"):
                if "question" in current_card:
                    current_card["answer"] = line.split(":", 1)[1].strip()
                    in_answer = True
                    in_question = False
            elif in_question and "question" in current_card:
                current_card["question"] += " " + line
            elif in_answer and "answer" in current_card:
                current_card["answer"] += " " + line
        
        # Don't forget the last card
        if current_card and "question" in current_card and "answer" in current_card:
            flashcards.append(current_card)
        
        # Fallback: create basic flashcards from content
        if not flashcards:
            flashcards = [
                {
                    "question": "What are the key points from this content?",
                    "answer": content[:500] + "..." if len(content) > 500 else content
                }
            ]
        
        return flashcards