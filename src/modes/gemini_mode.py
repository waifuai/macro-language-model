from .common import setup_gemini_api # Corrected import
from .gemini_init import initialize_chatbot
from .gemini_loop import run_conversation
import google.generativeai as genai # Added import for genai

def run_gemini_mode(waifu_name: str, debug: bool, max_turns: int = 10) -> None:
    genai_instance = setup_gemini_api() # Use the correct function name
    if not genai_instance:
        return
    # Initialize the model here as it's not returned by setup_gemini_api
    model = genai.GenerativeModel("gemini-2.0-flash", generation_config={"temperature": 0.9, "top_p": 0.95})
    waifu = initialize_chatbot(waifu_name, debug)
    run_conversation(waifu, model, max_turns, debug)