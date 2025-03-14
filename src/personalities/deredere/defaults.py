from typing import Dict, Any
from .data import deredere_default_responses
import random

def get_default_response(context: Dict[str, Any]) -> str:
    response = random.choice(deredere_default_responses)
    return response.encode('utf-8', 'replace').decode('utf-8')