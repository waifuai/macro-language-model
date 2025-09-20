"""
Interactive conversation mode for the Waifu Chatbot application.

This module implements the real-time interactive conversation mode where users can
engage in back-and-forth dialogue with an AI-powered waifu character. The module
handles conversation flow, maintains conversation history, and manages user input
processing with graceful exit handling.

Key features:
- Real-time conversation loop with user input handling
- Conversation history management for context preservation
- Support for multiple AI providers (Gemini, OpenRouter)
- Configurable personality traits and waifu names
- Debug mode for conversation monitoring
- Graceful error handling and recovery
- UTF-8 encoding support for international characters

The module generates an initial greeting and then maintains a continuous conversation
loop until the user chooses to exit, providing a natural chat experience with
the AI character.
"""
from chat_provider import generate_chat_response, get_default_provider

def run_interactive_mode(waifu_name: str, personality: str, debug: bool, provider: str = None) -> None:
    """Interact with the waifu using the selected provider (Gemini or OpenRouter)."""
    if provider is None:
        provider = get_default_provider()

    system_message = {
        "role": "system",
        "content": (
            f"You are {waifu_name}, a {personality} waifu. "
            "Respond in character with emotion and style appropriate to your personality."
        )
    }

    # Generate initial greeting
    greeting_messages = [
        system_message,
        {"role": "user", "content": "### Task: Generate an opening greeting as the waifu."}
    ]

    try:
        greeting = generate_chat_response(
            messages=greeting_messages,
            provider=provider,
            temperature=0.7
        )
        if greeting:
            print(f"{waifu_name}: {greeting}")
        else:
            print("Error: Could not generate greeting.")
            return
    except Exception as e:
        print(f"Error generating greeting: {e}")
        return

    conversation_history = [system_message, {"role": "assistant", "content": greeting}]

    while True:
        user_input = input("User: ")
        if debug:
            print(f"[DEBUG] User input: {user_input}")
        if user_input.lower().strip() in ["exit", "quit"]:
            print("Exiting interactive mode.")
            break

        # Add user message to history
        conversation_history.append({"role": "user", "content": user_input})

        try:
            response = generate_chat_response(
                messages=conversation_history,
                provider=provider,
                temperature=0.7,
                previous_waifu_response=user_input
            )
            if response:
                print(f"{waifu_name}: {response}")
                conversation_history.append({"role": "assistant", "content": response})
            else:
                print("Error: Could not generate response.")
                break
        except Exception as e:
            print(f"Error generating response: {e}")
            break