"""Tests for file content ingester."""

from unittest.mock import Mock, mock_open, patch

import pytest

from climber.ingest.base import ContentItem
from climber.ingest.file import FileIngester


class TestFileIngester:

    def test_init(self):
        """Test FileIngester initialization."""
        file_path = "/test/path.txt"
        ingester = FileIngester(file_path)
        assert str(ingester.path) == file_path
        assert ingester.source == file_path

    @patch('pathlib.Path.exists')
    def test_ingest_file_not_found(self, mock_exists):
        """Test handling of non-existent files."""
        mock_exists.return_value = False

        ingester = FileIngester("/nonexistent/file.txt")

        with pytest.raises(FileNotFoundError, match="File not found"):
            ingester.ingest()

    @patch('pathlib.Path.is_file')
    @patch('pathlib.Path.exists')
    def test_ingest_not_a_file(self, mock_exists, mock_is_file):
        """Test handling of directories passed as file path."""
        mock_exists.return_value = True
        mock_is_file.return_value = False

        ingester = FileIngester("/some/directory")

        with pytest.raises(ValueError, match="Path is not a file"):
            ingester.ingest()

    @patch('pathlib.Path.read_text')
    @patch('pathlib.Path.stat')
    @patch('pathlib.Path.is_file')
    @patch('pathlib.Path.exists')
    def test_ingest_text_file(self, mock_exists, mock_is_file, mock_stat, mock_read_text):
        """Test ingesting plain text file."""
        mock_exists.return_value = True
        mock_is_file.return_value = True
        mock_stat.return_value = Mock(st_size=100)
        mock_read_text.return_value = "This is test content\nWith multiple lines"

        ingester = FileIngester("/test/file.txt")
        result = ingester.ingest()

        assert isinstance(result, ContentItem)
        assert result.content_type == "text"
        assert result.title == "file"
        assert "file_size" in result.metadata
        assert "line_count" in result.metadata

    @patch('pathlib.Path.read_text')
    @patch('pathlib.Path.stat')
    @patch('pathlib.Path.is_file')
    @patch('pathlib.Path.exists')
    def test_ingest_markdown_file(self, mock_exists, mock_is_file, mock_stat, mock_read_text):
        """Test ingesting markdown file."""
        mock_exists.return_value = True
        mock_is_file.return_value = True
        mock_stat.return_value = Mock(st_size=200)
        mock_read_text.return_value = "# Main Title\n\nThis is content"

        ingester = FileIngester("/test/file.md")
        result = ingester.ingest()

        assert isinstance(result, ContentItem)
        assert result.content_type == "markdown"
        assert result.title == "Main Title"

    @patch('builtins.open', new_callable=mock_open, read_data=b"fake pdf content")
    @patch('pypdf.PdfReader')
    @patch('pathlib.Path.is_file')
    @patch('pathlib.Path.exists')
    def test_ingest_pdf_file(self, mock_exists, mock_is_file, mock_pdf_reader, mock_file_open):
        """Test ingesting PDF file."""
        mock_exists.return_value = True
        mock_is_file.return_value = True

        # Mock PDF reader
        mock_reader_instance = Mock()
        mock_reader_instance.metadata = {'/Title': 'PDF Title'}
        mock_page = Mock()
        mock_page.extract_text.return_value = "PDF content text"
        mock_reader_instance.pages = [mock_page]
        mock_pdf_reader.return_value = mock_reader_instance

        ingester = FileIngester("/test/file.pdf")
        result = ingester.ingest()

        assert isinstance(result, ContentItem)
        assert result.content_type == "pdf"
        assert result.title == "PDF Title"
