# Waifu Chatbot

## Overview

This project implements a chatbot designed to simulate conversation with a customizable "waifu" character. It features a modular personality system, allowing the chatbot to adopt different character archetypes (like Deredere, Tsundere, etc.) which dictate its conversational style, responses, and topic handling. The chatbot operates through a command-line interface and supports various interaction modes.

## Key Features

*   **Modular Personality System:** Select different character archetypes at runtime via command-line arguments. Each personality (`deredere`, `tsundere`, `yandere`, `kuudere`, `dandere`, `himedere`) has its own logic module determining behavior.
*   **Personality-Driven Responses:** The core response generation is delegated to the currently active personality module, ensuring distinct conversational patterns for each archetype.
*   **Topic Management:** Includes a system (`src/topic_manager.py`) for introducing and managing conversational topics, with personality-specific introductions and reactions.
*   **Multiple Run Modes:**
    *   **Interactive:** Engage in a real-time conversation with the chatbot via terminal input.
    *   **Auto (Gemini User Simulation):** Simulates a conversation where Google's Gemini API generates the *user's* responses, useful for testing the chatbot's interaction flow.
    *   **Debug:** Enables verbose logging for development and troubleshooting.
*   **Gemini Integration:** Utilizes the Google Gemini API (`google-generativeai`) to power the user simulation in Auto mode. Requires an API key.
*   **Organized Code Structure:** Project code is structured within the `src/` directory, separating concerns like personality logic, run modes, core chatbot mechanics, and utilities.
*   **Configuration:** Basic chatbot attributes like greetings and farewells are defined in `src/chatbot_config.py`.

## Architecture & File Structure (`src/`)

The project is organized within the `src/` directory:

*   **`main.py`**: Entry point. Parses arguments and launches the appropriate run mode. Uses `win_unicode_console` for Windows compatibility.
*   **`cli.py`**: Defines and parses command-line arguments using `argparse`.
*   **`modes/`**: Contains modules for different execution modes:
    *   `interactive_mode.py`: Handles the loop for direct user interaction.
    *   `auto_mode.py`: Runs a conversation simulation using Gemini for user input.
    *   `gemini_mode.py`: Appears related to the auto/Gemini simulation setup.
    *   `common.py`: Utility for configuring the Gemini API key.
    *   `gemini_init.py`, `gemini_loop.py`: Helper modules potentially used by `gemini_mode.py`.
*   **`waifu_chatbot.py`**: Defines the main `WaifuChatbot` class, holding state and orchestrating components.
*   **`waifu_chatbot_init.py`**: Initializes the chosen personality logic and registers core components like the `ResponseGenerator`.
*   **`waifu_chatbot_response.py`**: Contains the `respond` method logic, handling input processing and delegating response generation to the personality module.
*   **`waifu_frame.py`**: Class representing the chatbot's memory and state (e.g., name, interests, favorite food).
*   **`conversation_context.py`**: Manages the conversation history and tracks used responses to avoid repetition.
*   **`response_generator.py`**: Coordinates response generation, primarily by calling the active personality's methods. Loads response templates.
*   **`personalities/`**: Central hub for personality logic:
    *   `personality_interface.py`: Abstract base class defining the required methods for any personality module.
    *   `deredere/`, `tsundere/`, `yandere/`, `kuudere/`, `dandere/`, `himedere/`: Subdirectories for each archetype, containing:
        *   `logic.py`: The main class implementing the personality's behavior.
        *   `response_generator.py`: Response generation logic specific to the archetype.
        *   `topic_handler.py`: Topic introduction/reaction logic.
        *   `defaults.py`: Default/fallback responses.
        *   `data.py` (Optional): Personality-specific data.
*   **`response_templates/`**: Python files defining structured response templates keyed by topic/keyword and personality type.
*   **`response_template_loader.py`**: Loads and organizes the response templates from `response_templates/`.
*   **`topic_manager.py`**: Manages the introduction and flow of conversational topics.
*   **`topics.py`**: Contains logic for talking about interests (like manga, anime) in a personality-specific way.
*   **`dere_data/` & `dere_context.py`**: Contain data structures and context definitions related to personality types. (Note: 'Dere' terminology is used internally).
*   **`memory.py`**: Simple function for storing information in the `WaifuFrame`.
*   **`transformations.py`, `transformation_handlers.py`, `transforms/`**: Define and handle basic input pattern transformations, primarily for memory recall and simple actions. *Note: Keyword matching seems less central now.*
*   **`utils.py`**: Utility functions for tokenization and pattern matching.
*   **`core/registry.py`**: A registry class, primarily holding transformation definitions.
*   **`chatbot_config.py`**: Stores lists of greetings and farewells.

## Usage

Run the chatbot from the command line using `python src/main.py`.

**Modes:**

1.  **Interactive:**
    ```bash
    python src/main.py --interactive --personality <type> [--waifu_name <name>] [--debug]
    ```
    Chat directly with the bot in your terminal.

2.  **Auto (Gemini User Simulation):**
    ```bash
    python src/main.py --auto [number_of_turns] --personality <type> [--waifu_name <name>] [--debug]
    ```
    Simulates a conversation for `number_of_turns` (defaults to 10). Requires Gemini API setup.

3.  **Gemini Mode** (pure prompt test):
    ```bash
    python src/main.py --gemini --personality <type> [--waifu_name <name>] [--debug]
    ```
    Use your prompt engineering to test waifu responses directly via Gemini.

4.  **Debug**:
    Add `--debug` to any mode to enable verbose logging.

**Options:**

*   `--waifu_name <name>`: Sets the chatbot's name (default: "Waifu").
*   `--personality <type>`: Sets the chatbot's personality archetype.
    *   Choices: `deredere`, `dandere`, `himedere`, `kuudere`, `tsundere`, `yandere` (default: `deredere`).
*   `--gemini`: Explicitly enables Gemini mode (seems related to `--auto`).

**Gemini API Setup (for Auto mode):**

*   Place your Google Gemini API key in a file named `api.txt` in the directory *above* the project's root directory (i.e., `../api.txt` relative to `src/`).

## Dependencies

*   Python 3.x
*   `argparse` (Standard Library)
*   `random` (Standard Library)
*   `re` (Standard Library)
*   `google-generativeai`: For Gemini API interaction.
*   `tenacity`: For retry logic with the Gemini API.
*   `win_unicode_console`: For better Unicode support on Windows terminals.

Install external dependencies using pip:

```bash
pip install google-generativeai tenacity win_unicode_console --user
```

## Potential Future Improvements

*   Expand personality modules with more nuanced behaviors.
*   Add more sophisticated topic tracking and transitions.
*   Integrate more advanced Natural Language Processing (NLP) for better input understanding.
*   Develop a graphical user interface (GUI).
*   Refine the transformation system for more complex interactions.
*   Implement a more persistent memory system.
