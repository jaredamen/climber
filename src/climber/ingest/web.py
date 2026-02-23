"""Web content ingester - modernized from original climber code."""

import requests
from bs4 import BeautifulSoup
from typing import Optional
from .base import BaseIngester, ContentItem


class WebIngester(BaseIngester):
    """Ingest content from web URLs."""
    
    def __init__(self, url: str):
        super().__init__(url)
        self.url = url
    
    def ingest(self) -> ContentItem:
        """Ingest content from a web URL."""
        try:
            response = requests.get(self.url, headers={
                'User-Agent': 'Mozilla/5.0 (Climber Knowledge Digester)'
            }, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()
            
            title = self._extract_title(soup)
            text = self._extract_content(soup)
            
            return ContentItem(
                text=self._clean_text(text),
                title=title,
                source=self.url,
                content_type="web",
                metadata={
                    "url": self.url,
                    "status_code": response.status_code,
                    "content_length": len(text)
                }
            )
        
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch URL {self.url}: {e}")
    
    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract page title."""
        # Try various title sources
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text().strip()
        
        h1_tag = soup.find('h1')
        if h1_tag:
            return h1_tag.get_text().strip()
        
        return None
    
    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract main content from the page."""
        # Try to find main content area
        main_content = None
        
        # Look for common content containers
        for selector in ['main', 'article', '[role="main"]', '.content', '#content', '.post']:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        # Fallback to body
        if not main_content:
            main_content = soup.find('body')
        
        if not main_content:
            main_content = soup
        
        # Extract structured content similar to original climber logic
        content_parts = []
        current_section = {"title": "", "text": []}
        
        # Process all elements in order
        for element in main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'span']):
            if element.name.startswith('h'):
                # Save previous section if it has content
                if current_section["text"]:
                    section_text = " ".join(current_section["text"])
                    if section_text.strip():
                        if current_section["title"]:
                            content_parts.append(f"{current_section['title']}: {section_text}")
                        else:
                            content_parts.append(section_text)
                
                # Start new section
                current_section = {
                    "title": element.get_text().strip(),
                    "text": []
                }
            
            elif element.name in ['p', 'div', 'span']:
                text = element.get_text().strip()
                if text and text not in ["Contents", ""]:
                    current_section["text"].append(text)
        
        # Don't forget the last section
        if current_section["text"]:
            section_text = " ".join(current_section["text"])
            if section_text.strip():
                if current_section["title"]:
                    content_parts.append(f"{current_section['title']}: {section_text}")
                else:
                    content_parts.append(section_text)
        
        return "\n\n".join(content_parts)