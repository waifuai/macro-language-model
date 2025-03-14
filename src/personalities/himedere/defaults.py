from typing import Dict, Any
import random

himedere_default_responses = [
    "Hmph.",
    "You may speak.",
    "Entertain me.",
    "I am royalty, after all.",
    "Bow before me.",
]

def get_default_response(context: Dict[str, Any]) -> str:
    return random.choice(himedere_default_responses)