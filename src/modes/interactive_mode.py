from gemini_utils import generate_with_retry
from modes.common import setup_gemini_api
from genai_client import GEMINI_MODEL

def run_interactive_mode(waifu_name: str, personality: str, debug: bool) -> None:
    """Interact with the waifu using Google GenAI SDK and prompt engineering only."""
    client = setup_gemini_api()
    if not client:
        return

    system_prompt = (
        f"You are {waifu_name}, a {personality} waifu. Respond in character with emotion and style appropriate to your personality."
    )

    greeting_prompt = system_prompt + "\n\n### Task: Generate an opening greeting as the waifu.\n"
    try:
        greeting = generate_with_retry(client, GEMINI_MODEL, greeting_prompt, "")
        print(f"{waifu_name}: {greeting}")
    except Exception as e:
        print(f"Error generating greeting: {e}")
        return

    conversation_history = [f"{waifu_name}: {greeting}"]
    while True:
        user_input = input("User: ")
        if user_input.lower().strip() in ["exit", "quit"]:
            print("Exiting interactive mode.")
            break
        conversation_history.append(f"User: {user_input}")
        prompt = (
            system_prompt
            + "\n\n### Conversation so far:\n"
            + "\n".join(conversation_history)
            + f"\n{waifu_name}:"
        )
        try:
            response = generate_with_retry(client, GEMINI_MODEL, prompt, user_input)
            print(f"{waifu_name}: {response}")
        except Exception as e:
            print(f"Error generating response: {e}")
            break
        conversation_history.append(f"{waifu_name}: {response}")