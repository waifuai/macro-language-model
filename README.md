# Waifu Chatbot

## Overview

This project implements a chatbot designed to simulate conversation with a customizable "waifu" character. It features a modular personality system, allowing the chatbot to adopt different character archetypes (like Deredere, Tsundere, etc.) which dictate its conversational style, responses, and topic handling. The chatbot operates through a command-line interface and supports various interaction modes.

## Key Features

*   **Modular Personality System:** Select different character archetypes at runtime via command-line arguments. Each personality (`deredere`, `tsundere`, `yandere`, `kuudere`, `dandere`, `himedere`) has its own logic module determining behavior.
*   **Gemini-Driven Chat:** All conversation logic uses Google GenAI SDK via `google-genai` and `genai.Client`.
*   **Personality-Driven Responses:** The core response generation is delegated to the currently active personality module, ensuring distinct conversational patterns for each archetype.
*   **Topic Management:** Includes a system (`src/topic_manager.py`) for introducing and managing conversational topics, with personality-specific introductions and reactions.
*   **Multiple Run Modes:**
    *   **Interactive Mode:** Real-time chat via `run_interactive_mode`.
    *   **Auto Mode:** Simulates both user and waifu with Gemini via `run_auto_mode`.
    *   **Gemini Mode:** Prompt-only testing via `run_gemini_mode`.
*   **Configurable:** Basic prompts and small talk stored in `src/chatbot_config.json`.
*   **Testing Suite:** Built with pytest under `tests/`.
*   **Gemini Integration:** Utilizes the Google GenAI SDK (`google-genai`) to power the user simulation in Auto mode. Requires an API key.
*   **Organized Code Structure:** Project code is structured within the `src/` directory, separating concerns like personality logic, run modes, core chatbot mechanics, and utilities.
*   **Configuration:** Basic chatbot attributes like greetings and farewells are defined in `src/chatbot_config.py`.

## Architecture & File Structure

The project uses a simplified, Gemini-only codebase:

```
├── src/
│   ├── main.py            # Entry point
│   ├── cli.py             # Argument parser
│   ├── chatbot_config.json # Small-talk and prompts
│   ├── gemini_utils.py    # Retry wrapper for Gemini API
│   └── modes/
│       ├── common.py      # API setup
│       ├── interactive_mode.py
│       ├── auto_mode.py
│       └── gemini_mode.py
└── tests/
    └── test_gemini_mode.py
```

## Usage

Run via the `src` package:

```powershell
.venv/Scripts/python.exe -m src.main --interactive|--auto [turns]|--gemini [--personality <type>] [--waifu_name <name>] [--debug]
```

## Testing

Ensure dependencies and venv are set up via `uv`:

```powershell
python -m uv venv .venv
.venv/Scripts/python.exe -m ensurepip
.venv/Scripts/python.exe -m pip install uv
.venv/Scripts/python.exe -m uv pip install -r requirements-dev.txt
.venv/Scripts/python.exe -m pytest -q
```

## Dependencies

*   Python 3.x
*   `argparse` (Standard Library)
*   `random` (Standard Library)
*   `re` (Standard Library)
*   `google-genai`: For Gemini API interaction via Client.
*   `tenacity`: For retry logic with the Gemini API.
*   `win_unicode_console`: For better Unicode support on Windows terminals.
*   `pytest`: For testing.

Install external dependencies using pip:

```bash
.venv/Scripts/python.exe -m uv pip install -r requirements.txt
```

## Potential Future Improvements

*   Expand personality modules with more nuanced behaviors.
*   Add more sophisticated topic tracking and transitions.
*   Integrate more advanced Natural Language Processing (NLP) for better input understanding.
*   Develop a graphical user interface (GUI).
*   Refine the transformation system for more complex interactions.
*   Implement a more persistent memory system.
