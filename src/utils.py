import random
import re
from typing import List, Dict, Any

def tokenize(input_str: str) -> List[str]:
    """Tokenizes the input string into a list of lowercase words."""
    if not isinstance(input_str, str):
        input_str = str(input_str)
    return [
        word.lower()
        for word in re.split(r"[ .,!?]+", input_str)
        if word
    ]

def matches(pattern: List[str], input_list: List[str]) -> bool:
    """Checks if the input list matches the given pattern."""
    if not pattern:
        return not input_list
    if not input_list:
        return False
    if pattern[0] == "*":
        return matches(pattern[1:], input_list) or matches(pattern, input_list[1:])
    if pattern[0] == input_list[0]:
        return matches(pattern[1:], input_list[1:])
    return False

def substitute_template(template: str, substitutions: Dict[str, Any]) -> str:
    """Replaces placeholders in the template with actual values."""
    for placeholder, value in substitutions.items():
        template = template.replace(placeholder, str(value))
    return template