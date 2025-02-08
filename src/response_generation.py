import random
from typing import Dict, List, Set, Any
from dere_types import get_current_dere

def generate_response(response_templates: Dict[tuple[str, str], List[str]], keyword: str, substitutions: Dict[str, Any], used_responses: Set[str], waifu_memory: Any, current_dere: str, dere_response: Any, debug: bool) -> str:
    """Generates a response based on the keyword, substitutions, and current dere type.

    Args:
        response_templates: A dictionary of response templates, keyed by (keyword, dere_type).
        keyword: The keyword to generate a response for.
        substitutions: A dictionary of substitutions to make in the response template.
        used_responses: A set of responses that have already been used.
        waifu_memory: The waifu's memory object.
        current_dere: The current dere type of the waifu.
        dere_response: A function to generate a dere-specific response.
        debug: A boolean indicating whether to print debug messages.

    Returns:
        A string containing the generated response.
    """
    if debug:
        print(f"Type of used_responses in generate_response: {type(used_responses)}")
    dere_type = get_current_dere(waifu_memory.affection)
    template_group = None

    for (k, d), templates in response_templates.items():
        if k == keyword and d == dere_type:
            template_group = templates
            break

    if template_group:
        unused_templates = [t for t in template_group if t not in used_responses]

        if not unused_templates:
            used_responses.clear()  # Clear the set in place instead of reassigning
            unused_templates = template_group

        template = random.choice(unused_templates)
        used_responses.add(template)

        for placeholder, value in substitutions.items():
            if isinstance(value, list):
                value = ' '.join(value)

            template = template.replace("*", value, 1)

        return template

    return dere_response(waifu_memory, current_dere,
        "I don't know what to say.", "Is that so?", "Hmph.", "O-okay..."
    )