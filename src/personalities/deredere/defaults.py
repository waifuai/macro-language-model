from typing import Dict, Any
from .data import deredere_default_responses
import random

def get_default_response(context: Dict[str, Any]) -> str:
    return random.choice(deredere_default_responses)