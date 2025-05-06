from .common import setup_gemini_api
from gemini_utils import generate_with_retry
import google.generativeai as genai

def run_gemini_mode(waifu_name: str, personality: str, debug: bool) -> None:
    """Interactive Gemini-driven Waifu chat using personality prompt."""
    genai_instance = setup_gemini_api()
    if not genai_instance:
        return
    model = genai_instance.GenerativeModel(
        "gemini-2.5-pro-preview-05-06",
        generation_config={"temperature": 0.9, "top_p": 0.95}
    )
    # Construct personality-based system prompt
    system_prompt = (
        f"You are {waifu_name}, a {personality} waifu. "
        "Respond in character with emotion and style appropriate to your personality."
    )
    # Generate initial greeting
    greeting_prompt = system_prompt + "\n\n### Task: Generate an opening greeting as the waifu.\n"
    try:
        greeting = generate_with_retry(model, greeting_prompt, "")
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
            response = generate_with_retry(model, prompt, "")
            print(f"{waifu_name}: {response}")
        except Exception as e:
            print(f"Error generating response: {e}")