# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-02-23

### Added

#### Core Features
- **Knowledge digestion engine** with LLM-powered content processing
- **Multiple input sources**: URLs (web scraping), local files (Markdown, PDF, plain text)
- **Three output formats**: Briefings (executive summaries), Flashcards (JSON), Audio Scripts (TTS-ready)
- **Content presets**: General, Runbook, Changelog optimizations
- **BYOK (Bring Your Own Key)**: OpenAI and Anthropic API support
- **Command-line interface** with rich progress indicators

#### Architecture
- Modern Python 3.9+ codebase with type hints
- Modular architecture with pluggable ingesters, processors, and formatters
- Comprehensive test suite (42 tests) with mocked LLM responses
- Configuration management with file and environment variable support

#### CLI Commands
- `climber ingest <source>` - Main content processing command
- `climber config set/show` - Configuration management
- Support for `--output`, `--preset`, `--save` options

#### Output Formats
- **Briefing**: 2-minute executive summaries in Markdown
- **Flashcards**: JSON format compatible with basecamp companion app
- **Audio Script**: Conversational teaching scripts for TTS

#### Content Processing
- Intelligent content chunking for large documents
- Multi-chunk processing with result synthesis
- Content cleaning and normalization
- Hierarchical text extraction from web pages

#### Developer Experience
- Modern `pyproject.toml` packaging
- Development dependencies with `uv` support
- Pre-commit hooks ready configuration
- Comprehensive documentation

### Technical Details

#### Dependencies
- `click>=8.0.0` - CLI framework
- `requests>=2.28.0` - HTTP client
- `beautifulsoup4>=4.11.0` - HTML parsing
- `openai>=1.0.0` - OpenAI API client
- `anthropic>=0.3.0` - Anthropic API client
- `pydantic>=2.0.0` - Data validation
- `rich>=13.0.0` - Terminal formatting
- `pypdf>=3.0.0` - PDF processing
- `python-dotenv>=1.0.0` - Environment variables

#### Project Migration
- Complete rewrite from Django-based v0.1.4 to standalone CLI tool
- Migrated from Python 2.7 to Python 3.9+
- Replaced NLTK summarization with LLM-powered processing
- Modernized packaging from `setup.py` to `pyproject.toml`

### Security
- BYOK model ensures no API keys are stored or transmitted by the application
- Local configuration file with restricted permissions
- No hardcoded credentials or API endpoints

### Documentation
- Professional README with examples and use cases
- Comprehensive CLI reference
- Flashcard JSON format specification
- Development setup instructions
- Roadmap for future features