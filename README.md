# Hermes Agent

A fork of [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) — an autonomous agent framework powered by Hermes models with tool-calling capabilities.

> **Personal fork** — I'm using this to experiment with local LLMs via [Ollama](https://ollama.ai) and [LM Studio](https://lmstudio.ai). Main changes from upstream: bumped default temperature down and max iterations up for longer reasoning chains.

## Features

- 🤖 Powered by Hermes-2 and Hermes-3 models
- 🛠️ Extensible tool/function calling system
- 🔄 Multi-step reasoning and planning
- 💬 OpenAI-compatible API interface
- 🐳 Docker support
- 🔧 Highly configurable via environment variables

## Quick Start

### Prerequisites

- Python 3.10+
- An OpenAI-compatible API endpoint (or OpenAI API key)
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

```bash
# Clone the repo
git clone https://github.com/your-org/hermes-agent
cd hermes-agent

# Copy and configure environment
cp .env.example .env
# Edit .env with your API keys and settings

# Install dependencies (using uv)
uv sync

# Or with pip
pip install -r requirements.txt
```

### Running

```bash
# Start the agent
python -m hermes_agent

# Or with Docker
docker compose up
```

## Configuration

All configuration is done via environment variables. See [`.env.example`](.env.example) for the full list of options.

Key settings:

| Variable | Description | Default |
|---|---|---|
| `OPENAI_API_KEY` | Your API key | required |
| `OPENAI_BASE_URL` | API base URL | `https://api.openai.com/v1` |
| `MODEL_NAME` | Model to use | `NousResearch/Hermes-3-Llama-3.1-8B` |
| `MAX_ITERATIONS` | Max agent loop iterations | `20` |
| `TEMPERATURE` | Sampling temperature | `0.3` |
| `TIMEOUT` | Request timeout in seconds | `120` |
| `MAX_TOKENS` | Max tokens per response | `4096` |

> **Note (personal):** When running against LM Studio locally I usually set `TIMEOUT=300` — larger models can be slow to respond on first inference. Also found that setting `MAX_TOKENS=2048` helps avoid runaway responses when testing. For Ollama specifically, also set `OPENAI_BASE_URL=http://localhost:11434/v1` and `OPENAI_API_KEY=ollama` (it doesn't validate the key but the field still needs to be set).
>
> **Ollama model names:** Don't forget that Ollama uses its own model name format — e.g. `MODEL_NAME=llama3.1:8b` or `MODEL_NAME=nous-hermes2:10.7b` rather than the HuggingFace-style names. Tripped me up the first time.
>
> **LM Studio tip:** In LM Studio, make sure "Enable CORS" is checked under the server settings, otherwise you'll get confusing connection errors that don't mention CORS at all.

## Architecture

```
hermes_agent/
├── __main__.py        # Entry point
├── agent.py           # Core agent loop
├── tools/             # Built-in tools
│   ├── __init__.py
│   ├── web_search.py
│   ├── code_exec.py
│   └── file_ops.py
├── models/            # Model interfaces
│   └── openai_compat.py
└── config.py          # Configuration management
```

## Adding Custom Tools

Tools are simple Python functions decorated with `@tool`:

```python
from hermes_agent.tools import tool

@tool
def my_custom_tool
```
