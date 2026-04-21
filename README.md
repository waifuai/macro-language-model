# Waifu Chatbot

## Overview

This project implements a chatbot designed to simulate conversation with a customizable "waifu" character. It features a modular personality system, allowing the chatbot to adopt different character archetypes like Deredere, Tsundere, etc. The chatbot operates through a command-line interface and supports various interaction modes.

## Key Features

*   Modular Personality System with selectable archetypes
*   AI-Powered Chat via OpenRouter for chat generation
*   Provider-Ready Abstractions: unified facade for chat and classification
*   Topic Management system with personality-specific prompts
*   Multiple Run Modes: interactive and auto mode
*   Configurable small talk in src/chatbot_config.json
*   Testing suite with pytest
*   Organized code structure within src/

## Architecture & File Structure

```
├── src/
│   ├── main.py
│   ├── cli.py
│   ├── chatbot_config.json
│   ├── config.py                  # Centralized configuration management
│   ├── classifier.py              # Facade for classification
│   ├── chat_provider.py           # Facade for chat generation
│   ├── provider_openrouter.py     # OpenRouter provider for classification
│   ├── provider_openrouter_chat.py # OpenRouter provider for chat generation
│   └── modes/
│       ├── common.py
│       ├── interactive_mode.py
│       └── auto_mode.py
└── tests/
    └── test_openrouter.py
```

## Environment Setup using uv

Create a minimal virtual environment, ensure pip exists, install uv inside the venv, then install project dependencies. Always run uv via the venv's Python.

Windows:
```
.venv/Scripts/python.exe -m uv venv .venv
.venv/Scripts/python.exe -m ensurepip
.venv/Scripts/python.exe -m pip install uv
.venv/Scripts/python.exe -m uv pip install -r requirements-dev.txt
```

Linux or macOS:
```
.venv/bin/python -m uv venv .venv
.venv/bin/python -m ensurepip
.venv/bin/python -m pip install uv
.venv/bin/python -m uv pip install -r requirements-dev.txt
```

Run tests:
```
.venv/Scripts/python.exe -m pytest -q
```

## Credentials

OpenRouter:
* Env: OPENROUTER_API_KEY
* File fallback: ~/.api-openrouter

Do not commit secrets to version control.

## Model Selection Overrides

Optionally override the default model names by creating single-line files in your home directory. If the file exists and is non-empty, it takes precedence over built-in defaults.

- OpenRouter classification override:
  - Path: ~/.model-openrouter
  - Example contents: openrouter/free
  - Default if absent: openrouter/free
- OpenRouter chat override:
  - Path: ~/.model-openrouter-chat
  - Example contents: meta-llama/llama-3.1-8b-instruct
  - Default if absent: openrouter/free

## OpenRouter Integration

This repo uses OpenRouter for both classification and chat generation:

### Classification
* Provider: [`provider_openrouter.classify_with_openrouter()`](src/provider_openrouter.py:1)
* Facade: [`classifier.classify()`](src/classifier.py:1)

OpenRouter classification behavior:
* Deterministic prompt and low temperature
* Strict output normalization to digits 0 or 1 with conservative fallbacks
* Clear error paths returning None

### Chat Generation
* Provider: [`provider_openrouter_chat.generate_with_retry()`](src/provider_openrouter_chat.py:1)
* Facade: [`chat_provider.generate_chat_response()`](src/chat_provider.py:1)

OpenRouter chat behavior:
* Message-based conversation format
* Configurable temperature and token limits
* Retry logic with exponential backoff
* Echo detection to prevent repetitive responses
* Comprehensive error handling

## Quick Usage Examples

End-to-end classification using the facade:
```
.venv/Scripts/python.exe -c "from classifier import classify; print(classify('This is a test sentence', provider='openrouter'))"
```

Chat generation:
```
# Run from src directory
cd src

# Interactive mode with OpenRouter (default)
python main.py --interactive --personality tsundere

# Auto mode
python main.py --auto 5 --debug
```

## Testing

Unit tests cover:
* OpenRouter key resolution paths for both classification and chat
* HTTP behaviors including success, non-200, missing fields, and exceptions
* Chat generation with OpenRouter
* Mode-specific behaviors (interactive, auto)
* Error handling and fallback mechanisms

Run:
```
.venv/Scripts/python.exe -m pytest -q
```

## Dependencies

Core:
* requests - HTTP client for OpenRouter API
* tenacity - Retry logic for API calls
* win_unicode_console - Windows console encoding support

Dev:
* pytest and pinned tooling in requirements-dev.txt

Install:
```
.venv/Scripts/python.exe -m uv pip install -r requirements.txt
```

## Operational Guidance

* Timeouts: sensible HTTP timeout used in OpenRouter calls
* Determinism: keep temperature low, prompt concise, and normalize outputs strictly
* Security: prefer env vars in CI and restrict permissions for local key files
* Rate-limiting: consider delaying or adding retries if your workload is bursty
* Logging: log non-200 responses, truncated to avoid leaking PII or secrets

## License

MIT-0 License
