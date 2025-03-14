from typing import Dict, Any
import random

tsundere_default_responses = [
    "B-Baka!",
    "It's not like I like you or anything!",
    "Hmph!",
    "Don't get the wrong idea!",
    "Whatever.",
]

def get_default_response(context: Dict[str, Any]) -> str:
    return random.choice(tsundere_default_responses)