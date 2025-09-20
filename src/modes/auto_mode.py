"""
Automatic conversation simulation mode for the Waifu Chatbot application.

This module implements the automatic conversation mode where the AI simulates both
sides of a conversation between a human user and the waifu character. This mode
demonstrates the chatbot's ability to generate natural, context-aware dialogue
through AI vs AI interaction over a configurable number of conversation turns.

Key features:
- AI vs AI conversation simulation for demonstration purposes
- Configurable number of conversation turns (default: 10)
- Dual AI role-playing: one AI as the waifu, another as the human user
- Conversation history management for context preservation
- Support for multiple AI providers (Gemini, OpenRouter)
- Configurable personality traits and waifu characteristics
- Debug mode for conversation monitoring
- Graceful error handling and recovery

The module generates an initial waifu greeting, then alternates between generating
user responses and waifu responses to create a natural conversation flow that
showcases the AI's conversational capabilities.
"""
from chat_provider import generate_chat_response, get_default_provider

def run_auto_mode(waifu_name: str, personality: str, debug: bool, max_turns: int = 10, provider: str = None) -> None:
    """Simulates a conversation for `max_turns` turns with the selected provider as both waifu and user."""
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
        waifu_response = generate_chat_response(
            messages=greeting_messages,
            provider=provider,
            temperature=0.7
        )
        if waifu_response:
            print(f"{waifu_name}: {waifu_response}")
        else:
            print("Error: Could not generate greeting.")
            return
    except Exception as e:
        print(f"Error generating greeting: {e}")
        return

    conversation_history = [system_message, {"role": "assistant", "content": waifu_response}]
    user_input = ""

    for turn in range(max_turns):
        # User (AI) turn
        user_system_message = {
            "role": "system",
            "content": f"You are a human user talking to a waifu named {waifu_name}."
        }

        user_messages = [
            user_system_message,
            {"role": "user", "content": f"### Task: Respond as the user, naturally and briefly. The waifu said: {waifu_response}"}
        ]

        try:
            user_input = generate_chat_response(
                messages=user_messages,
                provider=provider,
                temperature=0.7
            )
            if user_input:
                print(f"User: {user_input}")
                conversation_history.append({"role": "user", "content": user_input})
            else:
                print("Error: Could not generate user input.")
                break
        except Exception as e:
            print(f"Error generating user input: {e}")
            break

        # Waifu (AI) turn
        try:
            waifu_response = generate_chat_response(
                messages=conversation_history,
                provider=provider,
                temperature=0.7,
                previous_waifu_response=user_input
            )
            if waifu_response:
                print(f"{waifu_name}: {waifu_response}")
                conversation_history.append({"role": "assistant", "content": waifu_response})
            else:
                print("Error: Could not generate waifu response.")
                break
        except Exception as e:
            print(f"Error generating waifu response: {e}")
            break
        # Optionally, break if a farewell is detected (not implemented)