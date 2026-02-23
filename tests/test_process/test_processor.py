"""Tests for content processor."""

import pytest
from unittest.mock import Mock, patch
from climber.process.processor import ContentProcessor
from climber.ingest.base import ContentItem


class TestContentProcessor:
    
    @patch('climber.process.processor.create_provider')
    @patch('climber.process.processor.get_prompt_template')
    def test_init(self, mock_get_prompt, mock_create_provider, mock_config):
        """Test ContentProcessor initialization."""
        mock_provider = Mock()
        mock_create_provider.return_value = mock_provider
        
        processor = ContentProcessor(mock_config)
        
        assert processor.config == mock_config
        assert processor.provider == mock_provider
        mock_create_provider.assert_called_once_with(mock_config)
    
    @patch('climber.process.processor.create_provider')
    @patch('climber.process.processor.get_prompt_template')
    def test_process_single_chunk(self, mock_get_prompt, mock_create_provider, mock_config, sample_content):
        """Test processing single chunk content."""
        # Mock provider
        mock_provider = Mock()
        mock_provider.generate.return_value = "Generated briefing content"
        mock_create_provider.return_value = mock_provider
        
        # Mock prompt template
        mock_get_prompt.return_value = "Template: {content} {title} {source}"
        
        processor = ContentProcessor(mock_config)
        result = processor.process(sample_content, "briefing", "general")
        
        assert result["output_type"] == "briefing"
        assert result["content"] == "Generated briefing content"
        assert result["source"] == sample_content.source
        assert result["title"] == sample_content.title
        assert result["chunk_count"] == 1
    
    @patch('climber.process.processor.create_provider')
    @patch('climber.process.processor.get_prompt_template')
    def test_process_multiple_chunks(self, mock_get_prompt, mock_create_provider, mock_config):
        """Test processing multiple chunk content."""
        # Create large content that will be chunked
        large_content = ContentItem(
            text="A" * 5000,  # Large enough to trigger chunking
            title="Large Document",
            source="test://large.com"
        )
        
        # Mock provider
        mock_provider = Mock()
        mock_provider.generate.side_effect = ["Chunk 1 result", "Chunk 2 result", "Combined result"]
        mock_create_provider.return_value = mock_provider
        
        # Mock prompt template
        mock_get_prompt.return_value = "Template: {content}"
        
        processor = ContentProcessor(mock_config)
        
        # Mock the chunker to return multiple chunks
        processor.chunker.chunk = Mock(return_value=["chunk1", "chunk2"])
        
        result = processor.process(large_content, "briefing", "general")
        
        assert result["output_type"] == "briefing"
        assert result["chunk_count"] == 2
        assert mock_provider.generate.call_count == 3  # 2 chunks + 1 combine
    
    @patch('climber.process.processor.create_provider')
    @patch('climber.process.processor.get_prompt_template')
    def test_combine_briefings(self, mock_get_prompt, mock_create_provider, mock_config):
        """Test combining multiple briefing results."""
        mock_provider = Mock()
        mock_provider.generate.return_value = "Combined briefing"
        mock_create_provider.return_value = mock_provider
        
        processor = ContentProcessor(mock_config)
        
        briefings = ["Brief 1", "Brief 2", "Brief 3"]
        result = processor._combine_briefings(briefings)
        
        assert result == "Combined briefing"
        mock_provider.generate.assert_called_once()
        
        # Check that the prompt contains all briefings
        call_args = mock_provider.generate.call_args[0][0]
        assert "Brief 1" in call_args
        assert "Brief 2" in call_args
        assert "Brief 3" in call_args
    
    @patch('climber.process.processor.create_provider')
    def test_combine_flashcards(self, mock_create_provider, mock_config):
        """Test combining flashcard sets."""
        mock_provider = Mock()
        mock_create_provider.return_value = mock_provider
        
        processor = ContentProcessor(mock_config)
        
        flashcard_sets = ['{"cards": [1]}', '{"cards": [2]}', '{"cards": [3]}']
        result = processor._combine_flashcards(flashcard_sets)
        
        expected = '{"cards": [1]}\n{"cards": [2]}\n{"cards": [3]}'
        assert result == expected