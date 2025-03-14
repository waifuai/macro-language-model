from waifu_chatbot import WaifuChatbot
from typing import Dict, List, Tuple
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
from gemini_utils import is_echoed_response, generate_with_retry
from modes.common import setup_gemini_api


def run_auto_mode(waifu_name: str, debug: bool, max_turns: int = 10) -> None:
    """Runs the chatbot in auto mode with Gemini generating the user responses."""
    print("Entering run_auto_mode with Gemini")

    # Setup Gemini API
    genai_instance = setup_gemini_api()
    if genai_instance is None:
        return

    # Initialize the WaifuChatbot
    waifu = WaifuChatbot(waifu_name, debug=debug)
    #register_transforms(waifu)

    # System instruction for Gemini
    system_instruction = (
        f"You are a human user interacting with a chatbot named {waifu_name}. "
        f"Generate engaging, natural responses that continue the conversation in a realistic way. "
        f"Be friendly, curious, and show personality. Avoid repeating what {waifu_name} says."
    )

    model = genai.GenerativeModel("gemini-2.0-flash", generation_config={"temperature": 0.9, "top_p": 0.95})

    # Initialize conversation
    conversation_history = []
    greeting = waifu.greetings[0]
    print(f"{waifu_name}: {greeting}")
    conversation_history.append(f"{waifu_name}: {greeting}")

    # Generate first user response to greeting
    prompt = (
        f"{system_instruction}\n\n"
        f"### Conversation History:\n"
        f"{conversation_history[0]}\n"
        f"### Your Task:\n"
        f"Respond as the user to this greeting in a natural way.\n"
        f"User: "
    )

    try:
        response = generate_with_retry(model, prompt, greeting)
        user_input = response.text
    except Exception as e:
        print(f"Error generating initial response: {e}")
        return
    #user_input = \"Placeholder response\" # Placeholder

    # Apply encoding fix here
    user_input = user_input.encode('utf-8', 'replace').decode('utf-8')
    print(f"User: {user_input}")
    conversation_history.append(f"User: {user_input}")

    # Main conversation loop
    for turn in range(max_turns):
        # Get waifu response
        waifu_response = waifu.respond(user_input)
        print(f"{waifu_name}: {waifu_response}")
        conversation_history.append(f"{waifu_name}: {waifu_response}")

        # Check if conversation should end
        if waifu_response in waifu.farewells:
            break

        # Prepare prompt with full history
        history_text = "\n".join(conversation_history)
        prompt = (
            f"{system_instruction}\n\n"
            f"### Conversation History:\n"
            f"{history_text}\n"
            f"### Your Task:\n"
            f"Respond as the user to {waifu_name}'s last message in a natural way.\n"
            f"User: "
        )

        # Generate user response with Gemini
        try:
            response = generate_with_retry(model, prompt, waifu_response)
            user_input = response.text
            # Apply encoding fix here
            user_input = user_input.encode('utf-8', 'replace').decode('utf-8')
            print(f"User: {user_input}")
            conversation_history.append(f"User: {user_input}")
        except Exception as e:
            print(f"Error in turn {turn + 1}: {e}")
            break
        #user_input = \"Placeholder response\" # Placeholder