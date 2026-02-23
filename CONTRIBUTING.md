# Contributing to Climber

Thank you for your interest in contributing to Climber! This document provides guidelines and information for contributors.

## Development Setup

### Prerequisites

- Python 3.9+
- [uv](https://github.com/astral-sh/uv) package manager
- OpenAI or Anthropic API key for testing

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/YusefAmen/climber.git
   cd climber
   ```

2. **Set up virtual environment**
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   uv pip install -e ".[dev]"
   ```

4. **Set up pre-commit hooks**
   ```bash
   pre-commit install
   ```

5. **Configure API key for testing**
   ```bash
   export CLIMBER_API_KEY=your-test-api-key
   ```

## Project Structure

```
src/climber/
├── __init__.py
├── cli.py                 # Command-line interface
├── config.py             # Configuration management
├── ingest/               # Content ingestion
│   ├── base.py          # Base ingester interface
│   ├── web.py           # Web scraping
│   └── file.py          # Local file processing
├── process/              # LLM processing
│   ├── chunker.py       # Content chunking
│   ├── processor.py     # Main processing logic
│   ├── providers/       # LLM API clients
│   └── prompts/         # Prompt templates
└── output/               # Output formatting
    ├── briefing.py      # Briefing formatter
    ├── flashcards.py    # Flashcard JSON formatter
    └── audio_script.py  # Audio script formatter
```

## Development Guidelines

### Code Style

- **Formatting**: Use `black` for code formatting
- **Linting**: Use `ruff` for linting and import sorting
- **Type hints**: Required for all public functions and methods
- **Docstrings**: Use Google-style docstrings for all modules, classes, and functions

### Testing

- **Test coverage**: All new features must include comprehensive tests
- **Mocking**: Use mocked LLM responses to avoid API calls in tests
- **Test organization**: Mirror the `src/` structure in `tests/`

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=climber --cov-report=html

# Run specific test file
pytest tests/test_ingest/test_web.py -v
```

### Quality Checks

```bash
# Format code
black src/ tests/

# Lint code
ruff src/ tests/

# Type checking
mypy src/climber/
```

## Contributing Workflow

### 1. Create an Issue

Before starting work, create an issue describing:
- The problem or feature request
- Proposed solution approach
- Any breaking changes

### 2. Fork and Branch

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/your-username/climber.git
cd climber
git checkout -b feature/your-feature-name
```

### 3. Implement Changes

- Write clean, well-documented code
- Include comprehensive tests
- Update documentation as needed
- Follow the existing code patterns

### 4. Test Your Changes

```bash
# Run tests
pytest tests/ -v

# Test CLI functionality
climber config show
climber ingest --help
```

### 5. Submit Pull Request

- Write a clear PR description
- Reference related issues
- Include examples of new functionality
- Ensure all checks pass

## Feature Development

### Adding a New Ingester

1. Create a new file in `src/climber/ingest/`
2. Inherit from `BaseIngester`
3. Implement the `ingest()` method
4. Add tests in `tests/test_ingest/`
5. Update the factory function in `ingest/__init__.py`

Example:
```python
class MyIngester(BaseIngester):
    def ingest(self) -> ContentItem:
        # Implementation here
        pass
```

### Adding a New Output Format

1. Create a new file in `src/climber/output/`
2. Inherit from `BaseFormatter`
3. Implement `format()` and `file_extension` property
4. Add tests in `tests/test_output/`
5. Update the factory function in `output/__init__.py`
6. Add CLI option in `cli.py`

### Adding a New LLM Provider

1. Create a new file in `src/climber/process/providers/`
2. Inherit from `BaseLLMProvider`
3. Implement `generate()` and `get_model_name()` methods
4. Add tests with mocked API responses
5. Update the factory function in `providers/__init__.py`
6. Add CLI configuration option

## Documentation

### README Updates

When adding features:
- Update the features list
- Add CLI examples
- Include in the roadmap if partially implemented

### Docstrings

Use Google-style docstrings:

```python
def process_content(content: str, output_type: str) -> dict:
    """Process content with LLM.
    
    Args:
        content: The input content to process.
        output_type: The desired output format.
        
    Returns:
        Dictionary containing processed results.
        
    Raises:
        ValueError: If output_type is not supported.
    """
```

## Release Process

### Version Bumping

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md` with new version
3. Create release PR
4. Tag release after merge

### Changelog Format

Follow [Keep a Changelog](https://keepachangelog.com/):

```markdown
## [1.1.0] - 2024-03-01

### Added
- New feature description

### Changed
- Changed feature description

### Fixed
- Bug fix description
```

## Roadmap Contributions

Priority areas for contribution:

### High Priority
- **Confluence API Integration** - Direct access to Confluence spaces
- **Git Repository Documentation** - Ingest entire `/docs` directories
- **Ollama Support** - Local LLM inference

### Medium Priority
- **Incident Prep Cards** - Specialized runbook format
- **Academic Preset** - Research paper optimization
- **Web UI** - Optional web interface

### Low Priority
- **Plugin System** - External ingester/formatter plugins
- **Caching Layer** - Content and result caching
- **Batch Processing** - Process multiple sources

## Community

- **Discussions**: Use GitHub Discussions for questions and ideas
- **Issues**: Report bugs and request features via GitHub Issues
- **Security**: Report security issues privately to jared.yusef@gmail.com

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and contribute
- Follow the project's technical standards

## Questions?

Feel free to:
- Open a GitHub Discussion
- Create an issue with the "question" label
- Email: jared.yusef@gmail.com

Thank you for contributing to Climber! 🏔️