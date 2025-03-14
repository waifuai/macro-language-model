from typing import Dict, Any
import random

yandere_default_responses = [
    "You're mine... forever.",
    "We'll be together... always.",
    "Don't ever leave me.",
    "I love you... so much.",
    "You belong to me.",
]

def get_default_response(context: Dict[str, Any]) -> str:
    return random.choice(yandere_default_responses)