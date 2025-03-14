import random
import re
from typing import List, Dict, Any

def tokenize(input_str: str) -> List[str]:
    """Tokenizes the input string into a list of lowercase words."""
    print(f"utils.tokenize: Entering with input: {input_str}")  # Debug print
    if not isinstance(input_str, str):
        input_str = str(input_str)
    tokens = [
        word.lower()
        for word in re.split(r"[ .,!?]+", input_str)
        if word
    ]
    print(f"utils.tokenize: Returning tokens: {tokens}")  # Debug print
    return tokens

def matches(pattern: List[str], input_list: List[str]) -> bool:
    """Checks if the input list matches the given pattern."""
    print(f"utils.matches: Entering with pattern: {pattern}, input_list: {input_list}")  # Debug print
    if not pattern:
        return not input_list  # Empty pattern matches only empty input
    if not input_list:
        return pattern[0] == '*' and matches(pattern[1:], input_list) # Empty input can match *
    if pattern[0] == "*":
        return matches(pattern[1:], input_list) or matches(pattern, input_list[1:])
    elif pattern[0] == input_list[0]:
        return matches(pattern[1:], input_list[1:])
    else:
        return False

def substitute_template(template: str, substitutions: Dict[str, Any]) -> str:
    """Replaces placeholders in the template with actual values."""
    for placeholder, value in substitutions.items():
        template = template.replace(placeholder, str(value))
    return template