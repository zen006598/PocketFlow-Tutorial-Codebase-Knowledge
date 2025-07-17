# Codebase to Tutorial Generator

> An AI agent that analyzes GitHub repositories and creates beginner-friendly tutorials explaining how the code works.

## Overview

This tool crawls GitHub repositories and builds a knowledge base from the code. It analyzes entire codebases to identify core abstractions and how they interact, transforming complex code into beginner-friendly tutorials.

## 🚀 Getting Started

1. Clone this repository
   ```bash
   git clone https://github.com/The-Pocket/PocketFlow-Tutorial-Codebase-Knowledge
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Set up your environment variables in `.env`:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   GEMINI_PROJECT_ID=your_project_id
   GITHUB_TOKEN=your_github_token
   ```

4. Verify LLM setup:
   ```bash
   uv run python utils/call_llm.py
   ```

5. Generate a tutorial:
   ```bash
   # Analyze a GitHub repository
   uv run python main.py --repo https://github.com/username/repo --include "*.py" "*.js"

   # Analyze a local directory
   uv run python main.py --dir /path/to/your/codebase --include "*.py"

   # Generate tutorial in Chinese
   uv run python main.py --repo https://github.com/username/repo --language "Chinese"
   ```

## Command Line Options

- `--repo` or `--dir` - GitHub repo URL or local directory path (required)
- `-n, --name` - Project name (optional, derived from URL/directory if omitted)
- `-t, --token` - GitHub token (or set GITHUB_TOKEN environment variable)
- `-o, --output` - Output directory (default: ./output)
- `-i, --include` - Files to include (e.g., "`*.py`" "`*.js`")
- `-e, --exclude` - Files to exclude (e.g., "`tests/*`" "`docs/*`")
- `-s, --max-size` - Maximum file size in bytes (default: 100KB)
- `--language` - Language for the generated tutorial (default: "english")
- `--max-abstractions` - Maximum number of abstractions to identify (default: 10)
- `--no-cache` - Disable LLM response caching (default: caching enabled)

## Docker Support

1. Build the Docker image:
   ```bash
   docker build -t pocketflow-app .
   ```

2. Run with environment variables:
   ```bash
   docker run -it --rm \
     -e GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE" \
     -v "$(pwd)/output_tutorials":/app/output \
     pocketflow-app --repo https://github.com/username/repo
   ```

## Configuration

The application uses a centralized configuration system in `config.py`. All API keys and settings are loaded from environment variables for security.

### Environment Variables

Set these in your `.env` file or environment:

- `GEMINI_API_KEY` - Your Google Gemini API key (required)
- `GEMINI_MODEL` - Gemini model to use (default: "gemini-2.5-pro-exp-03-25")
- `GEMINI_PROJECT_ID` - Google Cloud project ID (for Vertex AI)
- `GEMINI_LOCATION` - Google Cloud location (default: "us-central1")
- `GITHUB_TOKEN` - GitHub personal access token (for private repos)
- `LOG_DIR` - Directory for log files (default: "logs")
- `CACHE_FILE` - LLM response cache file (default: "llm_cache.json")

### Alternative LLM Providers

The `utils/call_llm.py` file includes commented implementations for:
- OpenAI GPT-4/o1 with reasoning effort
- Anthropic Claude 3.7 Sonnet with extended thinking
- Azure OpenAI with custom deployments
