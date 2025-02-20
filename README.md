# Waifu Chatbot

## Overview

This project implements a chatbot that simulates conversation with a customizable "waifu" (a fictional character, typically from anime or manga, that someone has great affection for). The chatbot uses various techniques such as keyword matching, transformations, and a memory system to generate contextually appropriate responses. It also incorporates the concept of "dere" types, which are personality archetypes commonly found in anime and manga, to make the conversation more dynamic and engaging.

## Files

-   **`main.py`**: The main script for running the chatbot. It handles argument parsing for interactive, automatic, and debug modes, and it initializes and runs the chatbot.
-   **`dere_types.py`**: Defines functions related to different "dere" types (personality archetypes) for the chatbot.
    -   `get_current_dere`: Determines the dere type based on affection level.
    -   `maybe_change_dere`: Randomly changes the dere type.
    -   `dere_response`: Returns a response based on the current dere type.
-   **`main_keywords.py`**: Defines a function `register_keywords` that registers keywords and their corresponding responses with the chatbot. It also defines synonyms for certain keywords.
-   **`main_transforms.py`**: Defines a function `register_transforms` that registers transformations with the chatbot. These transformations handle user inputs and map them to specific responses, memory slots, or actions like changing the dere type or introducing a new topic.
-   **`memory.py`**: Defines a function `remember` that stores a value in the chatbot's memory and updates the affection level.
-   **`response_generation.py`**: Defines a function `generate_response` that generates a response based on the keyword, substitutions, current dere type, and used responses.
-   **`response_templates.py`**: Contains a dictionary `response_templates` that maps keywords and dere types to lists of response templates.
-   **`topics.py`**: Defines functions for talking about interests and introducing new topics in a dere-specific manner.
    -   `talk_about_interest`: Generates a response about a random interest.
    -   `introduce_topic`: Introduces a new topic with a relevant phrase based on the current dere type.
-   **`transformations.py`**: Defines functions for creating and applying transformations.
    -   `deftransform`: Defines a transformation pattern and its response.
    -   `apply_transformations`: Applies transformations to the input and returns a transformed response.
-   **`utils.py`**: Defines utility functions for tokenizing input strings, matching patterns, and substituting placeholders in templates.
-   **`waifu_chatbot.py`**: Defines the `WaifuChatbot` class, which is the core of the chatbot. It handles keyword definitions, transformations, memory, dere types, response generation, and topic management.
-   **`waifu_frame.py`**: Defines the `WaifuFrame` class, which represents the chatbot's memory and personality.

## Usage

The chatbot can be run in three modes:

1. **Interactive mode:**  `python main.py --interactive`
    
    This mode allows for a real-time conversation with the chatbot.
    
2. **Automatic mode:**  `python main.py --auto [number_of_turns]`
    
    This mode simulates a conversation with a specified number of turns. If no number is provided, it defaults to 10 turns.
    
3. **Debug mode:**  `python main.py --debug`
    
    This mode enables debug information and runs a self-conversation loop for testing purposes.
    

### Additional Options

-   `--waifu_name`: Sets the waifu's name (default is "Waifu").

## Example

```
$ python main.py --interactive --waifu_name "Alice"
Starting up...
Alice: Senpai, you're back! How was your day?
User: I'm doing well, how are you?
Alice: I'm fine.
User: I'm feeling great
Alice: Oh, you're feeling great.
Alice: I-I'll remember that, okay?
```

## Dependencies

This project uses the following Python libraries:

-   `argparse`: For parsing command-line arguments.
-   `random`: For generating random choices.
-   `re`: For regular expression operations.

These libraries are typically included in standard Python distributions.

## Future Improvements

-   Add more dere types and refine existing ones.
-   Expand the range of topics and responses.
-   Implement a more sophisticated memory system.
-   Incorporate natural language processing (NLP) techniques for better understanding of user input.
-   Add a graphical user interface (GUI).