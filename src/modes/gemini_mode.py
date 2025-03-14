from .gemini_setup import setup_gemini
from .gemini_init import initialize_chatbot
from .gemini_loop import run_conversation

def run_gemini_mode(waifu_name: str, debug: bool, max_turns: int = 10) -> None:
    genai_instance, model = setup_gemini(waifu_name, debug)
    if not genai_instance:
        return
    waifu = initialize_chatbot(waifu_name, debug)
    run_conversation(waifu, model, max_turns, debug)