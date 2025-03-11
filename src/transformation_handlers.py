from typing import Dict, List, Tuple, Callable, Any, Optional, Set
from dere_manager import DereContext, dere_response, maybe_change_dere
from topics import talk_about_interest, introduce_topic
from dere_data import default_responses

def handle_waifu_memory_response(waifu_memory: Any, part: tuple) -> str:
    """Handles the 'waifu-memory' response type."""
    attribute_name = part[1]
    if hasattr(waifu_memory, attribute_name):
        return str(getattr(waifu_memory, attribute_name))
    else:
        return "I don't remember that."

def handle_dere_response(context: DereContext, part: tuple) -> str:
    """Handles the 'dere-response' response type."""
    return dere_response(context, *part[1:])

def handle_maybe_change_dere(context: DereContext, dere_types: List[str], waifu_chatbot: Any) -> str:
    """Handles the 'maybe-change-dere' response type."""
    return maybe_change_dere(context, dere_types, waifu_chatbot)

def handle_talk_about(context: DereContext) -> str:
    """Handles the 'talk-about' response type."""
    return talk_about_interest(context.waifu_memory, context.current_dere, context.used_responses, context.debug)

def handle_introduce_topic(context: DereContext, part: tuple) -> str:
    """Handles the 'introduce-topic' response type."""
    return introduce_topic(part[1], context.waifu_memory, context.current_dere, list(context.used_responses), context.debug)