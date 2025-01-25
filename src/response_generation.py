import random

def generate_response(response_templates, keyword, substitutions, used_responses, waifu_memory, current_dere, dere_response, debug):
    """Generates a response based on the keyword, substitutions, and current dere type."""
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