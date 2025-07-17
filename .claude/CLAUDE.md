# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI-powered codebase tutorial generator that analyzes GitHub repositories and creates beginner-friendly tutorials. It uses the PocketFlow framework (100-line LLM framework) to orchestrate a pipeline that identifies core abstractions, analyzes relationships, and generates comprehensive tutorials with cross-references and visualizations.

## Project Structure

```
PocketFlow-Tutorial-Codebase-Knowledge/
├── main.py                    # Entry point - CLI argument parsing and pipeline execution
├── flow.py                    # Flow definition - connects nodes in sequence
├── nodes.py                   # Core pipeline nodes (FetchRepo, IdentifyAbstractions, etc.)
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker containerization
├── README.md                  # Project documentation
├── CLAUDE.md                  # This file - guidance for Claude Code
├── utils/
│   ├── __init__.py
│   ├── call_llm.py           # LLM interface with caching and multiple providers
│   ├── crawl_github_files.py # GitHub repository crawling (API/SSH)
│   └── crawl_local_files.py  # Local directory crawling with .gitignore support
├── logs/                     # Generated - LLM call logs (when created)
├── llm_cache.json           # Generated - LLM response cache (when created)
└── output/                  # Generated - tutorial output directory
    └── [project_name]/
        ├── index.md         # Main tutorial page
        ├── 01_concept.md    # Individual chapter files
        ├── 02_concept.md
        └── ...
```

## Commands

### Running the Application
```bash
# Analyze a GitHub repository
python main.py --repo https://github.com/username/repo --include "*.py" "*.js" --exclude "tests/*" --max-size 50000

# Analyze a local directory
python main.py --dir /path/to/your/codebase --include "*.py" --exclude "*test*"

# Generate tutorial in another language
python main.py --repo https://github.com/username/repo --language "Chinese"

# Control abstraction count and caching
python main.py --repo https://github.com/username/repo --max-abstractions 15 --no-cache
```

### Setup and Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Test LLM connection (verifies API key and model access)
python utils/call_llm.py

# Test file crawling utilities
python utils/crawl_github_files.py
python utils/crawl_local_files.py
```

### Docker
```bash
# Build image
docker build -t pocketflow-app .

# Run with environment variables
docker run -it --rm \
  -e GEMINI_API_KEY="YOUR_API_KEY" \
  -v "$(pwd)/output_tutorials":/app/output \
  pocketflow-app --repo https://github.com/username/repo
```

## Architecture

### PocketFlow Pipeline Architecture
The application follows a linear 6-stage pipeline using PocketFlow's Node/Flow abstraction:

1. **FetchRepo** (Node) - Crawls GitHub repos or local directories using API/SSH/filesystem
2. **IdentifyAbstractions** (Node) - Uses LLM to identify 5-10 core abstractions from codebase
3. **AnalyzeRelationships** (Node) - Determines how abstractions interact and creates project summary
4. **OrderChapters** (Node) - Determines optimal pedagogical order for explaining abstractions
5. **WriteChapters** (BatchNode) - Generates individual tutorial chapters in parallel
6. **CombineTutorial** (Node) - Combines chapters into final tutorial with index and navigation

### Key Components

**Entry Point & Flow Control:**
- `main.py` - CLI argument parsing, shared state initialization
- `flow.py` - Creates pipeline by connecting nodes with >> operator

**Core Processing:**
- `nodes.py` - All 6 node implementations inheriting from Node/BatchNode
- Each node has prep/exec/post methods following PocketFlow pattern

**Utilities:**
- `utils/call_llm.py` - LLM interface with caching, logging, and multiple provider support
- `utils/crawl_github_files.py` - GitHub API crawling with SSH/HTTPS support, rate limiting, error handling
- `utils/crawl_local_files.py` - Local filesystem crawling with .gitignore support and progress tracking

### Shared State Flow
The pipeline uses a shared dictionary that accumulates data:
```python
shared = {
    # Input configuration
    "repo_url": str,               # GitHub repository URL
    "local_dir": str,              # Local directory path
    "project_name": str,           # Derived project name
    "github_token": str,           # GitHub API token
    "include_patterns": set,       # File patterns to include
    "exclude_patterns": set,       # File patterns to exclude
    "max_file_size": int,          # File size limit in bytes
    "language": str,               # Tutorial language
    "use_cache": bool,             # Enable/disable LLM caching
    "max_abstraction_num": int,    # Max abstractions to identify
    
    # Pipeline data (populated by nodes)
    "files": [(path, content)],    # List of file tuples
    "abstractions": [{}],          # Core concepts with files mapping
    "relationships": {},           # Project summary and abstraction relationships
    "chapter_order": [int],        # Ordered abstraction indices
    "chapters": [str],             # Generated markdown content
    "final_output_dir": str        # Output directory path
}
```

## LLM Configuration

### Default Setup (Google Gemini 2.5 Pro)
```bash
export GEMINI_API_KEY="your-api-key"
# Optional: customize model
export GEMINI_MODEL="gemini-2.5-pro-exp-03-25"
```

### Alternative Providers
The `utils/call_llm.py` file contains commented implementations for:
- OpenAI GPT-4/o1 with reasoning effort
- Anthropic Claude 3.7 Sonnet with extended thinking
- Azure OpenAI with custom deployments
- OpenRouter API for various models

### Caching and Logging
- Responses cached in `llm_cache.json` (can be disabled with `--no-cache`)
- Logs saved to `logs/llm_calls_YYYYMMDD.log` with prompts and responses
- Cache is skipped during retries to avoid infinite loops

## File Processing

### Crawling Capabilities
**GitHub Support:**
- HTTPS and SSH repository URLs
- Specific branch/commit/path targeting
- Rate limit handling and automatic retries
- Private repository access with tokens
- File size limits and pattern filtering

**Local Directory Support:**
- .gitignore integration for automatic exclusion
- Progress tracking with colored output
- Pattern-based inclusion/exclusion
- UTF-8-sig encoding support (handles BOM)

### Default File Patterns
**Include:** `*.py`, `*.js`, `*.jsx`, `*.ts`, `*.tsx`, `*.go`, `*.java`, `*.c`, `*.cpp`, `*.h`, `*.md`, `*.rst`, `*Dockerfile`, `*Makefile`, `*.yaml`, `*.yml`

**Exclude:** `assets/*`, `data/*`, `*test*`, `*build/*`, `*dist/*`, `*node_modules/*`, `.git/*`, `.github/*`, `*venv/*`

## Error Handling and Reliability

### Node Retry Logic
- All LLM-dependent nodes configured with `max_retries=5` and `wait=20` seconds
- Automatic retry on rate limits, timeouts, and temporary failures
- Graceful fallback mechanisms for validation failures

### Response Validation
- YAML parsing with structured validation
- Assertion checks for required fields and data types
- Index validation against available abstractions/files
- File size limits (default 100KB) prevent memory issues

## Multi-language Support

### Language Configuration
- `--language` parameter for non-English tutorials
- Language instructions injected into LLM prompts
- Translated abstraction names, descriptions, and chapter content
- Fixed UI elements (like attribution) remain in English

### Prompt Engineering
- Conditional language instructions based on target language
- Context notes about potentially translated input data
- Separate handling for different content types (names, descriptions, explanations)

## Output Structure

### Generated Files
- `index.md` - Main tutorial with project summary, Mermaid diagram, and chapter links
- `01_concept_name.md` - Individual chapter files for each abstraction
- Chapter navigation with proper markdown links
- Attribution footer on all generated files

### Tutorial Features
- Mermaid diagrams showing abstraction relationships
- Cross-references between chapters with proper links
- Beginner-friendly explanations with analogies
- Code examples with step-by-step breakdowns
- Sequence diagrams for complex interactions

## Agentic Coding Principles

This project implements the "Agentic Coding" methodology from `.cursorrules`:
1. **Requirements** - Human defines tutorial goals
2. **Flow Design** - High-level pipeline structure
3. **Utilities** - LLM calls and file crawling
4. **Node Design** - Individual processing stages
5. **Implementation** - PocketFlow-based execution
6. **Optimization** - Prompt engineering and error handling

### Development Workflow
- Start with simple solutions and iterate
- Design at high level before implementation
- Frequently ask for feedback and clarification
- Use shared store for data separation from compute logic
- Fail fast without extensive try/catch logic to identify weak points