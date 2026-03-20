"""File content ingester."""

from pathlib import Path

import pypdf

from .base import BaseIngester, ContentItem


class FileIngester(BaseIngester):
    """Ingest content from local files."""

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.path = Path(file_path)

    def ingest(self) -> ContentItem:
        """Ingest content from a local file."""
        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {self.path}")

        if not self.path.is_file():
            raise ValueError(f"Path is not a file: {self.path}")

        suffix = self.path.suffix.lower()

        if suffix == ".pdf":
            return self._ingest_pdf()
        elif suffix in [".md", ".markdown"]:
            return self._ingest_markdown()
        elif suffix in [".txt", ".text"]:
            return self._ingest_text()
        else:
            # Try to read as text
            return self._ingest_text()

    def _ingest_pdf(self) -> ContentItem:
        """Ingest PDF content."""
        try:
            with open(self.path, "rb") as file:
                pdf_reader = pypdf.PdfReader(file)

                # Extract metadata
                metadata = {}
                if pdf_reader.metadata:
                    metadata = {
                        "title": pdf_reader.metadata.get("/Title"),
                        "author": pdf_reader.metadata.get("/Author"),
                        "pages": len(pdf_reader.pages),
                    }

                # Extract text from all pages
                text_parts = []
                for _page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    if page_text.strip():
                        text_parts.append(page_text)

                text = "\n\n".join(text_parts)
                title = metadata.get("title") or self.path.stem

                return ContentItem(
                    text=self._clean_text(text),
                    title=title,
                    source=str(self.path),
                    content_type="pdf",
                    metadata=metadata,
                )

        except Exception as e:
            raise RuntimeError(f"Failed to read PDF {self.path}: {e}") from e

    def _ingest_markdown(self) -> ContentItem:
        """Ingest Markdown content."""
        try:
            text = self.path.read_text(encoding="utf-8")

            # Extract title from first heading if present
            title = None
            lines = text.split("\n")
            for line in lines:
                if line.startswith("# "):
                    title = line[2:].strip()
                    break

            if not title:
                title = self.path.stem

            return ContentItem(
                text=self._clean_text(text),
                title=title,
                source=str(self.path),
                content_type="markdown",
                metadata={
                    "file_size": self.path.stat().st_size,
                    "line_count": len(lines),
                },
            )

        except Exception as e:
            raise RuntimeError(f"Failed to read Markdown file {self.path}: {e}") from e

    def _ingest_text(self) -> ContentItem:
        """Ingest plain text content."""
        try:
            text = self.path.read_text(encoding="utf-8")

            return ContentItem(
                text=self._clean_text(text),
                title=self.path.stem,
                source=str(self.path),
                content_type="text",
                metadata={
                    "file_size": self.path.stat().st_size,
                    "line_count": len(text.split("\n")),
                },
            )

        except Exception as e:
            raise RuntimeError(f"Failed to read text file {self.path}: {e}") from e
