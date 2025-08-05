from modes.common import setup_gemini_api
from genai_client import GEMINI_MODEL

def setup_gemini(waifu_name: str, debug: bool):
    client = setup_gemini_api()
    if not client:
        return None, None
    system_instruction = (
        f"You are a human user interacting with {waifu_name}, "
        f"a virtual character with a specific personality. "
        f"Your goal is to have a conversation with {waifu_name} and explore their responses. "
        f"Remember that {waifu_name} is a chatbot and does not have real feelings or consciousness. "
        f"Keep the conversation light and engaging, and try to ask questions that are relevant "
        f"to {waifu_name}'s personality and interests. "
        f"Avoid asking overly personal or sensitive questions."
    )
    if debug:
        print("Entering run_gemini_mode")
    # Return client and model name for callers using generate_with_retry
    return client, GEMINI_MODEL