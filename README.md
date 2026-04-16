# Climber

[![CI Status](https://github.com/jaredamen/climber/workflows/CI/badge.svg)](https://github.com/jaredamen/climber/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A knowledge digester that ingests technical content and produces study-ready output formats.**

Climber transforms technical documentation, web articles, and PDFs into digestible learning materials optimized for platform engineers and technical teams.

## Features

- **Multiple Input Sources**: URLs, local files (Markdown, PDF, plain text)
- **Smart Content Processing**: LLM-powered chunking and analysis
- **Multiple Output Formats**: Briefings, flashcards, audio scripts
- **Bring Your Own Key (BYOK)**: Use your own OpenAI or Anthropic API keys
- **Content Presets**: Optimized prompts for runbooks, changelogs, and general content
- **Command Line Interface**: Simple, powerful CLI for automation

## Quick Start

### Installation

```bash
pip install climber
```

### Configuration

Set your API key (required):

```bash
climber config set --api-key your-api-key-here
climber config set --provider openai  # or anthropic
```

Alternatively, set the environment variable:

```bash
export CLIMBER_API_KEY=your-api-key-here
```

**Security Note**: Configuration files are automatically secured with `600` permissions (owner read/write only) to protect your API keys.

### Basic Usage

Generate a 2-minute briefing from a URL:

```bash
climber ingest https://kubernetes.io/docs/concepts/overview/
```

Create flashcards from a runbook:

```bash
climber ingest runbook.md --output flashcards --preset runbook
```

Generate all formats and save to directory:

```bash
climber ingest changelog.pdf --output all --save ./study-materials/
```

## Example Outputs

### Briefing Format

```markdown
# Kubernetes Overview

**Source:** https://kubernetes.io/docs/concepts/overview/

## Executive Summary

• Kubernetes is a container orchestration platform that automates deployment, scaling, and management
• Key components include the control plane (API server, etcd, scheduler) and worker nodes (kubelet, kube-proxy)
• Provides declarative configuration through YAML manifests and APIs
• Handles service discovery, load balancing, and storage orchestration automatically
• Essential for modern cloud-native applications requiring high availability and scalability
```

### Flashcards Format (JSON)

```json
{
  "title": "Kubernetes Overview",
  "source": "https://kubernetes.io/docs/concepts/overview/",
  "flashcards": [
    {
      "question": "What is Kubernetes and what problem does it solve?",
      "answer": "Kubernetes is a container orchestration platform that automates the deployment, scaling, and management of containerized applications..."
    },
    {
      "question": "What are the main components of the Kubernetes control plane?",
      "answer": "The control plane consists of the API server (handles requests), etcd (distributed key-value store), scheduler (assigns pods to nodes)..."
    }
  ],
  "metadata": {
    "total_cards": 8,
    "format_version": "1.0"
  }
}
```

### Audio Script Format

```text
AUDIO SCRIPT: Kubernetes Overview
=====================================

Source: https://kubernetes.io/docs/concepts/overview/
Estimated Duration: 7 minutes
Format: Educational/Conversational

SCRIPT:
-------

Hey there! Let's talk about Kubernetes - one of the most important tools in modern platform engineering.

So, what exactly is Kubernetes? Think of it as the ultimate traffic controller for your containers...
```

## Use Cases

### 1. Kubernetes Runbook → Incident Response Cards

Transform your operational runbooks into study-ready flashcards:

```bash
climber ingest k8s-troubleshooting.md --preset runbook --output flashcards
```

Perfect for on-call engineers who need quick access to troubleshooting procedures during incidents.

### 2. Prometheus Changelog → Impact Analysis

Convert release notes into focused briefings:

```bash
climber ingest https://github.com/prometheus/prometheus/releases/tag/v2.45.0 --preset changelog --output briefing
```

Get straight to what matters: breaking changes, new features, and migration requirements.

### 3. Distributed Systems Paper → Study Materials

Turn academic papers into digestible learning content:

```bash
climber ingest raft-consensus.pdf --output all --save ./study-session/
```

Generate briefings for quick review, flashcards for memorization, and audio scripts for commute learning.

## CLI Reference

### Global Commands

- `climber --version` - Show version information
- `climber --help` - Show help information

### Configuration Commands

```bash
climber config set --api-key <key>        # Set API key
climber config set --provider <provider>  # Set provider (openai/anthropic)
climber config show                        # Show current configuration
```

### Ingest Command

```bash
climber ingest <source> [options]
```

**Arguments:**
- `<source>` - URL or file path to process

**Options:**
- `--output <format>` - Output format: `briefing`, `flashcards`, `audio-script`, `all` (default: `briefing`)
- `--preset <preset>` - Content preset: `general`, `runbook`, `changelog` (default: `general`)
- `--save <directory>` - Save output to directory instead of displaying

**Examples:**

```bash
# Basic briefing from URL
climber ingest https://example.com/docs

# Flashcards from local file with runbook preset
climber ingest ./incident-playbook.md --output flashcards --preset runbook

# All formats saved to directory
climber ingest changelog.pdf --output all --save ./outputs/

# Audio script optimized for changelog content
climber ingest release-notes.md --output audio-script --preset changelog
```

## Content Presets

### General (Default)
Balanced approach suitable for most technical content. Focuses on key concepts, definitions, and practical applications.

### Runbook
Optimized for operational documentation:
- Emphasizes procedures and decision points
- Highlights prerequisites and dependencies
- Includes troubleshooting scenarios
- Focuses on actionable information

### Changelog
Tuned for release notes and change documentation:
- Categorizes changes by impact level
- Highlights breaking changes and migrations
- Focuses on user-facing impacts
- Includes version and timeline information

## Flashcard JSON Format

The flashcards output is compatible with the [basecamp companion app](https://basecamp.app) for mobile study sessions. The JSON structure is:

```json
{
  "title": "Content Title",
  "source": "Original Source URL/Path",
  "generated_at": "ISO timestamp",
  "format_version": "1.0",
  "flashcards": [
    {
      "question": "Question text",
      "answer": "Detailed answer"
    }
  ],
  "metadata": {
    "total_cards": 10,
    "chunk_count": 1
  }
}
```

## Roadmap

### Coming Soon
- **Confluence API Integration** - Direct access to Confluence spaces
- **Git Repository Documentation** - Ingest entire `/docs` directories
- **Ollama Support** - Local LLM inference without API costs
- **Incident Prep Cards** - Specialized format for runbooks with decision trees
- **Changelog Digest** - Smart release note summarization
- **Academic Preset** - Optimized for research papers and technical documentation
- **RFC Preset** - Tailored for technical specifications and proposals

## Development

### Requirements
- Python 3.9+
- OpenAI API key OR Anthropic API key

### Local Development

```bash
git clone https://github.com/jaredamen/climber.git
cd climber
uv venv
source .venv/bin/activate
uv pip install -e .
```

### Running Tests

```bash
uv pip install pytest pytest-mock
pytest tests/ -v
```

### Task Management

This project uses `uv` for dependency management and includes a comprehensive test suite with 42 passing tests covering all core functionality.

## Author

**Built by Jared (Yusef) Amen**

Platform engineer passionate about making technical knowledge more accessible. Available for consulting on developer tooling, platform engineering, and knowledge management systems.

- **Consulting**: [jared.yusef@gmail.com](mailto:jared.yusef@gmail.com)
- **Support this project**: [Buy Me a Coffee](https://buymeacoffee.com/YusefAmen)

## Companion App

Want to study on the go? Check out **[basecamp](https://basecamp.app)** — the companion PWA for reviewing Climber flashcard output from your phone. Import your JSON files and study anywhere.

## License

MIT License. See [LICENSE](LICENSE) for details.

---

*Climb Mt. Knowledge, one digest at a time.* 🏔️