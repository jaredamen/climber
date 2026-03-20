"""Tests for output formatters."""

import json

from climber.output.audio_script import AudioScriptFormatter
from climber.output.briefing import BriefingFormatter
from climber.output.flashcards import FlashcardsFormatter


class TestBriefingFormatter:

    def test_file_extension(self):
        """Test briefing formatter file extension."""
        formatter = BriefingFormatter()
        assert formatter.file_extension == "md"

    def test_format_basic(self):
        """Test basic briefing formatting."""
        formatter = BriefingFormatter()
        result = {
            "content": "This is the briefing content.",
            "title": "Test Title",
            "source": "https://example.com"
        }

        output = formatter.format(result)

        assert "# Test Title" in output
        assert "**Source:** https://example.com" in output
        assert "## Executive Summary" in output
        assert "This is the briefing content." in output

    def test_format_with_chunk_count(self):
        """Test briefing formatting with multiple chunks."""
        formatter = BriefingFormatter()
        result = {
            "content": "Multi-chunk briefing content.",
            "title": "Test Title",
            "source": "test source",
            "chunk_count": 3
        }

        output = formatter.format(result)

        assert "Generated from 3 content sections" in output


class TestFlashcardsFormatter:

    def test_file_extension(self):
        """Test flashcards formatter file extension."""
        formatter = FlashcardsFormatter()
        assert formatter.file_extension == "json"

    def test_format_with_json_content(self):
        """Test formatting flashcards with JSON content."""
        formatter = FlashcardsFormatter()

        json_content = json.dumps({
            "flashcards": [
                {"question": "What is X?", "answer": "X is Y"},
                {"question": "How does Z work?", "answer": "Z works by..."}
            ]
        })

        result = {
            "content": json_content,
            "title": "Test Cards",
            "source": "test source",
            "chunk_count": 1
        }

        output = formatter.format(result)
        parsed_output = json.loads(output)

        assert parsed_output["title"] == "Test Cards"
        assert parsed_output["source"] == "test source"
        assert len(parsed_output["flashcards"]) == 2
        assert parsed_output["metadata"]["total_cards"] == 2
        assert parsed_output["metadata"]["chunk_count"] == 1

    def test_format_with_text_content(self):
        """Test formatting flashcards with text content."""
        formatter = FlashcardsFormatter()

        text_content = """
        Q: What is Python?
        A: Python is a programming language.
        
        Q: What is Django?
        A: Django is a web framework.
        """

        result = {
            "content": text_content,
            "title": "Test Cards",
            "source": "test source"
        }

        output = formatter.format(result)
        parsed_output = json.loads(output)

        assert len(parsed_output["flashcards"]) >= 1
        assert all("question" in card and "answer" in card for card in parsed_output["flashcards"])

    def test_extract_flashcards_from_json(self):
        """Test extracting flashcards from JSON format."""
        formatter = FlashcardsFormatter()

        json_content = '{"flashcards": [{"question": "Test?", "answer": "Answer"}]}'
        flashcards = formatter._extract_flashcards(json_content)

        assert len(flashcards) == 1
        assert flashcards[0]["question"] == "Test?"
        assert flashcards[0]["answer"] == "Answer"

    def test_parse_text_flashcards(self):
        """Test parsing flashcards from text format."""
        formatter = FlashcardsFormatter()

        text_content = """
        Q: First question?
        A: First answer.
        
        Question: Second question?
        Answer: Second answer.
        """

        flashcards = formatter._parse_text_flashcards(text_content)

        assert len(flashcards) >= 2
        assert flashcards[0]["question"] == "First question?"
        assert flashcards[0]["answer"].strip() == "First answer."


class TestAudioScriptFormatter:

    def test_file_extension(self):
        """Test audio script formatter file extension."""
        formatter = AudioScriptFormatter()
        assert formatter.file_extension == "txt"

    def test_format_basic(self):
        """Test basic audio script formatting."""
        formatter = AudioScriptFormatter()
        result = {
            "content": "Welcome to this audio script about testing.",
            "title": "Test Script",
            "source": "test source"
        }

        output = formatter.format(result)

        assert "AUDIO SCRIPT: Test Script" in output
        assert "Source: test source" in output
        assert "Estimated Duration: 5-10 minutes" in output
        assert "SCRIPT:" in output
        assert "Welcome to this audio script about testing." in output
        assert "END OF SCRIPT" in output

    def test_format_with_chunk_count(self):
        """Test audio script formatting with multiple chunks."""
        formatter = AudioScriptFormatter()
        result = {
            "content": "Multi-chunk script content.",
            "title": "Test Script",
            "source": "test source",
            "chunk_count": 2
        }

        output = formatter.format(result)

        assert "Generated from 2 content sections" in output
