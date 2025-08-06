# Waifu Chatbot

## Overview

This project implements a chatbot designed to simulate conversation with a customizable "waifu" character. It features a modular personality system, allowing the chatbot to adopt different character archetypes like Deredere, Tsundere, etc. The chatbot operates through a command-line interface and supports various interaction modes.

## Key Features

*   Modular Personality System with selectable archetypes
*   Gemini-Driven Chat via Google GenAI SDK
*   Provider-Ready Abstractions: classifier facade to add external providers with minimal coupling
*   Topic Management system with personality-specific prompts
*   Multiple Run Modes: interactive, auto, and gemini mode
*   Configurable small talk in src/chatbot_config.json
*   Testing suite with pytest
*   Organized code structure within src/

## Architecture & File Structure

```
├── src/
│   ├── main.py
│   ├── cli.py
│   ├── chatbot_config.json
│   ├── gemini_utils.py
│   ├── genai_client.py
│   ├── classifier.py              # Provider-agnostic facade
│   ├── provider_openrouter.py     # OpenRouter provider for classification
│   └── modes/
│       ├── common.py
│       ├── interactive_mode.py
│       ├── auto_mode.py
│       └── gemini_mode.py
└── tests/
    ├── test_gemini_mode.py
    └── test_openrouter.py
```

## Environment Setup using uv

Create a minimal virtual environment, ensure pip exists, install uv inside the venv, then install project dependencies. Always run uv via the venv’s Python.

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

Gemini:
* Env: GEMINI_API_KEY or GOOGLE_API_KEY
* File fallback: ~/.api-gemini

OpenRouter:
* Env: OPENROUTER_API_KEY
* File fallback: ~/.api-openrouter

Do not commit secrets to version control.

## Model Selection Overrides

Optionally override the default model names by creating single-line files in your home directory. If the file exists and is non-empty, it takes precedence over built-in defaults.

- Gemini override:
  - Path: ~/.model-gemini
  - Example contents: gemini-2.0-flash-lite
  - Default if absent: gemini-2.5-pro
- OpenRouter override:
  - Path: ~/.model-openrouter
  - Example contents: openrouter/auto
  - Default if absent: openrouter/horizon-beta

## Adding OpenRouter Support

This repo includes a minimal, provider-agnostic integration:
* Provider: [`provider_openrouter.classify_with_openrouter()`](src/provider_openrouter.py:1)
* Facade: [`classifier.classify()`](src/classifier.py:1)

OpenRouter classification behavior:
* Deterministic prompt and low temperature
* Strict output normalization to digits 0 or 1 with conservative fallbacks
* Clear error paths returning None

## Quick Usage Examples

End-to-end classification using the facade:
```
.venv/Scripts/python.exe -c "from classifier import classify; print(classify('This is a test sentence', provider='openrouter'))"
```

Gemini-driven run modes:
```
.venv/Scripts/python.exe -m src.main --interactive
.venv/Scripts/python.exe -m src.main --auto 5
.venv/Scripts/python.exe -m src.main --gemini
```

## Testing

Unit tests cover:
* OpenRouter key resolution paths
* HTTP behaviors including success, non-200, missing fields, and exceptions
* Existing Gemini mode behaviors

Run:
```
.venv/Scripts/python.exe -m pytest -q
```

## Dependencies

Core:
* google-genai
* tenacity
* win_unicode_console
* requests

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
