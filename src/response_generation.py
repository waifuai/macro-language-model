import random
from typing import Dict, List, Set, Any
from dere_types import get_current_dere, DereContext # Import DereContext

def generate_response(response_templates: Dict[tuple[str, str], List[str]], keyword: str, substitutions: Dict[str, Any], used_responses: Set[str], waifu_memory: Any, topic_dere: str, dere_response: Any, debug: bool, used_default_responses: Set[str], previous_input: str = "") -> str: # Added topic_dere and used_default_responses
    """Generates a response based on the keyword, substitutions, and current dere type.
    """
    if debug:
        print(f"Type of used_responses in generate_response: {type(used_responses)}")
    #dere_type = get_current_dere(waifu_memory.affection) # Removed
    dere_type = topic_dere # Use the passed-in dere type
    template_group = None

    if debug:
        print(f"generate_response: keyword: {keyword}, dere_type: {dere_type}") # Debug print
        print(f"generate_response: response_templates keys: {list(response_templates.keys())}") # Debug print

    for (k, d), templates in response_templates.items():
        if k == keyword and d == dere_type:
            template_group = templates
            break
        if debug: # ADDED DEBUG PRINT
            print(f"generate_response: Checking template: {(k, d)}") # ADDED DEBUG PRINT

    if template_group:
        unused_templates = [t for t in template_group if t not in used_responses]

        if not unused_templates:
            used_responses.clear()  # Clear the set in place
            unused_templates = template_group

        template = random.choice(unused_templates)
        used_responses.add(template)

        for placeholder, value in substitutions.items():
            if isinstance(value, list):
                value = ' '.join(value)
            template = template.replace(f"{{{placeholder}}}", str(value), 1)

        return template
    else: # ADDED ELSE BLOCK
        if debug:
            print(f"generate_response: No matching template group found for keyword: {keyword}, dere_type: {dere_type}")

    # Create DereContext here:
    dere_context = DereContext(waifu_memory, topic_dere, used_responses, debug) # Use topic_dere
    return dere_response(dere_context, used_default_responses) # Corrected call to dere_response