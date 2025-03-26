from typing import Dict, List, Tuple, Callable, Any, Optional, Set
from dere_types import DereContext  # Updated import
# from dere_utils import maybe_change_dere # REMOVED
from dere_response_selection import dere_response
from topics import talk_about_interest, introduce_topic
from dere_data import dere_types
from utils import matches
from memory import remember

def handle_waifu_memory_response(waifu_memory: Any, part: tuple) -> str:
    """Handles the 'waifu-memory' response type."""
    attribute_name = part[1]
    if hasattr(waifu_memory, attribute_name):
        return str(getattr(waifu_memory, attribute_name))
    else:
        return "I don't remember that."

def handle_dere_response(context: DereContext, part: tuple) -> str:
    """Handles the 'dere-response' response type."""
    response = dere_response(context, *part[1:])
    return response.encode('utf-8', 'replace').decode('utf-8')

# REMOVED handle_maybe_change_dere function
# def handle_maybe_change_dere(context: DereContext, dere_types: List[str]) -> str:
#     """Handles the 'maybe-change-dere' response type."""
#     response = maybe_change_dere(context, dere_types)
#     if response:
#         return response.encode('utf-8', 'replace').decode('utf-8')
#     return ""

def handle_talk_about(context: DereContext) -> str:
    """Handles the 'talk-about' response type."""
    response = talk_about_interest(context.waifu_memory, context.current_dere, context.used_responses, context.debug)
    return response.encode('utf-8', 'replace').decode('utf-8')

def handle_introduce_topic(waifu_chatbot: Any, part: tuple) -> str:
    """Handles the 'introduce-topic' response type."""
    topic = part[1]
    response = waifu_chatbot.personality.introduce_topic(topic, {"waifu_memory": waifu_chatbot.waifu_memory, "debug": waifu_chatbot.debug})
    return response.encode('utf-8', 'replace').decode('utf-8')