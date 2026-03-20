"""Tests for web content ingester."""

from unittest.mock import Mock, patch

import pytest
import requests

from climber.ingest.base import ContentItem
from climber.ingest.web import WebIngester


class TestWebIngester:

    def test_init(self):
        """Test WebIngester initialization."""
        url = "https://example.com"
        ingester = WebIngester(url)
        assert ingester.url == url
        assert ingester.source == url

    @patch('climber.ingest.web.requests.get')
    @patch('climber.ingest.web.BeautifulSoup')
    def test_ingest_success(self, mock_soup, mock_get):
        """Test successful web content ingestion."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><title>Test Page</title><body><p>Test content</p></body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Mock BeautifulSoup
        mock_soup_instance = Mock()
        mock_soup_instance.find.return_value = Mock(get_text=Mock(return_value="Test Page"))
        mock_soup_instance.find_all.return_value = [Mock(get_text=Mock(return_value="Test content"))]
        # Make soup callable to handle soup(["script", "style"])
        mock_soup_instance.return_value = []
        mock_soup.return_value = mock_soup_instance

        ingester = WebIngester("https://example.com")

        # Mock the private methods
        ingester._extract_title = Mock(return_value="Test Page")
        ingester._extract_content = Mock(return_value="Test content")

        result = ingester.ingest()

        assert isinstance(result, ContentItem)
        assert result.title == "Test Page"
        assert result.content_type == "web"
        assert result.source == "https://example.com"
        assert "url" in result.metadata

    @patch('climber.ingest.web.requests.get')
    def test_ingest_request_failure(self, mock_get):
        """Test handling of request failures."""
        mock_get.side_effect = requests.RequestException("Connection failed")

        ingester = WebIngester("https://example.com")

        with pytest.raises(RuntimeError, match="Failed to fetch URL"):
            ingester.ingest()

    def test_extract_title_from_title_tag(self):
        """Test title extraction from title tag."""
        from bs4 import BeautifulSoup

        html = "<html><title>Page Title</title></html>"
        soup = BeautifulSoup(html, 'html.parser')

        ingester = WebIngester("https://example.com")
        title = ingester._extract_title(soup)

        assert title == "Page Title"

    def test_extract_title_from_h1(self):
        """Test title extraction from h1 tag when no title."""
        from bs4 import BeautifulSoup

        html = "<html><body><h1>Main Heading</h1></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        ingester = WebIngester("https://example.com")
        title = ingester._extract_title(soup)

        assert title == "Main Heading"
