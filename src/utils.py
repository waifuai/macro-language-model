import random
import re
from typing import List, Dict, Any

def tokenize(input_str: str) -> List[str]:
    """Tokenizes the input string into a list of lowercase words."""
    if not isinstance(input_str, str):
        input_str = str(input_str)
    tokens = [
        word.lower()
        for word in re.split(r"[ .,!?]+", input_str)
        if word
    ]
    # Removed problematic print statements to avoid encoding errors during tokenization logging
    return tokens

def substitute_template(template: str, substitutions: Dict[str, Any]) -> str:
    """Replaces placeholders in the template with actual values."""
    for placeholder, value in substitutions.items():
        template = template.replace(placeholder, str(value))
    return template

def matches(pattern: str, input_str: str) -> bool:
    """Checks if the pattern matches the input string. '*' is a wildcard."""
    pattern = pattern.lower().replace("*", ".*")
    input_str = input_str.lower()
    return bool(re.match(f"^{pattern}$", input_str))