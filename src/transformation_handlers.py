from typing import Dict, List, Tuple, Callable, Any, Optional, Set
from dere_manager import DereContext, dere_response, maybe_change_dere
from topics import talk_about_interest, introduce_topic
from response_generation import generate_response
from dere_data import default_responses

def handle_generate_response(waifu_chatbot: Any, part: tuple, substitutions: Dict[str, List[str]], response_templates: Dict[tuple[str, str], List[str]], dere_response: Callable[..., str], debug: bool) -> str:
    """Handles the 'generate' response type."""
    keyword = part[1]
    sub_dict = {}
    for sub_key, sub_value in part[2]:
        # Get substitutions for all wildcards in the tuple
        all_values: List[str] = []
        for k, v in substitutions.items():
            all_values.extend(v)
        sub_dict[sub_key] = all_values
    return generate_response(
        response_templates, # Pass response_templates
        keyword,  # Use current_topic as keyword
        sub_dict,  # Pass substitutions
        waifu_chatbot.dere_context.used_responses,
        waifu_chatbot.waifu_memory,
        waifu_chatbot.dere_context.current_dere, # Use the stored dere type
        dere_response,
        waifu_chatbot.debug,
        waifu_chatbot.response_generator.used_default_responses, # Pass used_default_responses
        "" # Pass previous input
    )


def handle_waifu_memory_response(waifu_memory: Any, part: tuple) -> str:
    """Handles the 'waifu-memory' response type."""
    return str(getattr(waifu_memory, part[1]))

def handle_dere_response(context: DereContext, part: tuple) -> str:
    """Handles the 'dere-response' response type."""
    return dere_response(context, *part[1:])

def handle_maybe_change_dere(context: DereContext, dere_types: List[str], part: tuple) -> str:
    """Handles the 'maybe-change-dere' response type."""
    return maybe_change_dere(context, dere_types, *part[1:])

def handle_talk_about(context: DereContext) -> str:
    """Handles the 'talk-about' response type."""
    return talk_about_interest(context.waifu_memory, context.current_dere, context.used_responses, context.debug)

def handle_introduce_topic(context: DereContext, part: tuple) -> str:
    """Handles the 'introduce-topic' response type."""
    return introduce_topic(part[1], context.waifu_memory, context.current_dere, list(context.used_responses), context.debug)