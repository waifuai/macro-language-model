from typing import Dict, Any
import random

kuudere_default_responses = [
    "...",
    "Whatever.",
    "I don't care.",
    "Do as you wish.",
    "Hmph.",
]

def get_default_response(context: Dict[str, Any]) -> str:
    return random.choice(kuudere_default_responses)