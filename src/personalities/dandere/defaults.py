from typing import Dict, Any
import random

dandere_default_responses = [
    "...",
    "Um...",
    "I-I don't know...",
    "*nods*",
    "*looks away*",
]

def get_default_response(context: Dict[str, Any]) -> str:
    return random.choice(dandere_default_responses)