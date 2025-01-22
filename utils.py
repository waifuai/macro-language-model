import random
import re

def tokenize(input_str):
    """Tokenizes the input string into a list of lowercase words."""
    return [
        word.lower()
        for word in re.split(r"[ .,!?]", input_str)

    ]

def matches(pattern, input_list):
    """Checks if the input list matches the given pattern."""
    if not pattern:
        return not input_list
    if pattern[0] == "*":
        return matches(pattern[1:], input_list) or (
            input_list and matches(pattern, input_list[1:])
        )
    if not input_list:
        return False
    if len(pattern) == 1 and len(input_list) == 1 and pattern[0] == input_list[0]:
        return True
    if pattern[0] == input_list[0]:
        return matches(pattern[1:], input_list[1:])
    return False

def substitute_template(template, substitutions):
    """Replaces placeholders in the template with actual values."""
    for placeholder, value in substitutions.items():
        template = template.replace(placeholder, str(value))
    return template