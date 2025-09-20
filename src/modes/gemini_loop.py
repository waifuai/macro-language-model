"""
Gemini conversation loop implementation for the Waifu Chatbot application.

This module implements the core conversation loop for Gemini-based interactions,
managing the flow between user input, AI response generation, and conversation
history. It provides a complete conversation management system with features for
UTF-8 encoding, debug logging, and graceful error handling.

Key features:
- Complete conversation loop management for Gemini interactions
- UTF-8 encoding support for international characters
- Debug mode for conversation monitoring and troubleshooting
- Conversation history preservation for context awareness
- Integration with waifu response generation
- Graceful error handling and recovery
- Farewell detection for conversation termination

Note: This module appears to reference waifu objects and methods that may not be
fully implemented in the current codebase, suggesting it may be part of an incomplete
or planned feature implementation.
"""
from gemini_utils import generate_with_retry
import sys
import traceback
from modes.common import setup_gemini_api
from genai_client import GEMINI_MODEL

def run_conversation(waifu, client, max_turns: int, debug: bool):
    # Attempt to force UTF-8 output for stdout
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception as e:
        print(f"Warning: Could not reconfigure stdout to UTF-8: {e}", file=sys.stderr)

    greeting = waifu.greetings[0]
    print(f"{waifu.waifu_memory.name}: {greeting}")
    conversation_history = [f"{waifu.waifu_memory.name}: {greeting}"]

    # System instruction for Gemini
    system_instruction = (
        f"You are a human user interacting with a chatbot named {waifu.waifu_memory.name}. "
        f"Generate engaging, natural, **very short** responses (max 20 words) that continue the conversation in a realistic way. " # Added length constraint
        f"Be friendly, curious, and show personality. Avoid repeating what {waifu.waifu_memory.name} says."
    )
    for turn in range(max_turns):
        if turn == 0:
            # Generate first user response to greeting
            prompt = (
                f"{system_instruction}\\n\\n"
                f"### Conversation History:\\n"
                f"{conversation_history[0]}\\n"
                f"### Your Task:\\n"
                f"Respond as the user to this greeting in a natural way.\\n"
                f"User: "
            )
        else:
            # Prepare prompt with full history
            history_text = "\\n".join(conversation_history)
            prompt = (
                f"{system_instruction}\\n\\n"
                f"### Conversation History:\\n"
                f"{history_text}\\n"
                f"### Your Task:\\n"
                f"Respond as the user to {waifu.waifu_memory.name}'s last message in a natural way.\\n"
                f"User: "
            )
        try:
            response = generate_with_retry(client, GEMINI_MODEL, prompt, greeting if turn == 0 else waifu_response)
            if response: # 'response' here is the raw text from Gemini
                user_input = response
                # Ensure user_input is treated as a string and print safely
                try:
                    # Print user input directly (stdout reconfigured)
                    if debug: # Use the debug flag passed into the function
                        print(f"DEBUG: Original user_input type: {type(user_input)}")
                        print(f"DEBUG: Original user_input repr: {repr(user_input)}")
                    print(f"User: {str(user_input)}")
                except Exception as e:
                    # Fallback if printing fails
                    print(f"User: [Error displaying response: {e}]")
                conversation_history.append(f"User: {user_input}") # Append original user_input to history

                # Pass the potentially raw user_input string to the chatbot
                waifu_response = waifu.respond(user_input)
                # Print waifu_response directly (stdout reconfigured)
                try:
                    print(f"{waifu.waifu_memory.name}: {str(waifu_response)}")
                except Exception as e:
                    # Fallback if printing fails
                    print(f"{waifu.waifu_memory.name}: [Error displaying response: {e}]")
                conversation_history.append(f"{waifu.waifu_memory.name}: {waifu_response}")
                if waifu_response in waifu.farewells:
                    break
            else:
                print("Waifu: I'm sorry, I'm having trouble understanding. Can you try again?")
                break

        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
            break