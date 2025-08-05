from .common import setup_gemini_api
from gemini_utils import generate_with_retry
from genai_client import GEMINI_MODEL

def run_gemini_mode(waifu_name: str, personality: str, debug: bool) -> None:
    """Interactive GenAI-driven Waifu chat using personality prompt."""
    client = setup_gemini_api()
    if not client:
        return

    system_prompt = (
        f"You are {waifu_name}, a {personality} waifu. "
        "Respond in character with emotion and style appropriate to your personality."
    )
    # Generate initial greeting
    greeting_prompt = system_prompt + "\n\n### Task: Generate an opening greeting as the waifu.\n"
    try:
        greeting = generate_with_retry(client, GEMINI_MODEL, greeting_prompt, "")
        print(f"{waifu_name}: {greeting}")
    except Exception as e:
        print(f"Error generating greeting: {e}")
    # Conversation loop
    while True:
        user_input = input("User: ")
        if debug:
            print(f"[DEBUG] User input: {user_input}")
        if user_input.lower().strip() in ["exit", "quit"]:
            print("Exiting Gemini mode.")
            break
        # Build prompt for next waifu response
        prompt = (
            system_prompt
            + "\n\n### Conversation so far:\n"
            + f"User: {user_input}\n"
            + f"{waifu_name}:"
        )
        if debug:
            print(f"[DEBUG] Prompt to Gemini: {prompt}")
        try:
            response = generate_with_retry(client, GEMINI_MODEL, prompt, "")
            print(f"{waifu_name}: {response}")
        except Exception as e:
            print(f"Error generating response: {e}")