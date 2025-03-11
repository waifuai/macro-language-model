from typing import Dict, List, Tuple, Callable, Any, Optional, Set
from dere_manager import DereContext, dere_response, maybe_change_dere
from topics import talk_about_interest, introduce_topic
from dere_data import default_responses
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

def apply_transformations(transformations: Dict[str, Tuple[Any, Optional[str], int]], input_list: List[str], waifu_memory: Any, current_dere: str, talk_about_interest: Callable[..., str], introduce_topic: Callable[..., str], dere_response: Callable[..., str], response_templates: Dict[tuple[str, str], List[str]], used_responses: Set[str], dere_types: List[str], debug: bool, waifu_chatbot: Any) -> Optional[str]:
    """Applies transformations to the input and returns a transformed response."""
    if waifu_chatbot.debug:
        print(f"transformations.apply_transformations: Entering with input: {input_list}")
    # Dictionary to map response types to handler functions
    response_handlers: Dict[str, Callable] = {
        "waifu-memory": handle_waifu_memory_response,
        "dere-response": handle_dere_response,
        "maybe-change-dere": handle_maybe_change_dere,
        "talk-about": handle_talk_about,
        "introduce-topic": handle_introduce_topic,
    }

    for pattern, (response, memory_slot, affection_change) in transformations.items():
        pattern_list = pattern.split()
        if matches(pattern_list, input_list):
            substitutions: Dict[str, List[str]] = {}
            j = 0
            for i in range(len(pattern_list)):
                if pattern_list[i] == '*':
                    key = f'*_{i}'
                    substitutions[key] = []
                    while j < len(input_list) and (i == len(pattern_list) - 1 or (i + 1 < len(pattern_list) and input_list[j] != pattern_list[i + 1])):
                        substitutions[key].append(input_list[j])
                        j += 1
                elif j < len(input_list) and i < len(pattern_list) and input_list[j] == pattern_list[i]:
                    j += 1

            if callable(response):
                if "*" in substitutions:
                    transformed_response = response(" ".join(substitutions["*"]))
                else:
                    transformed_response = response()
            elif isinstance(response, list):
                transformed_response = []
                for part in response:
                    if isinstance(part, str):
                        # Replace all wildcards in the string
                        temp_part = part
                        for k, v in substitutions.items():
                            temp_part = temp_part.replace(k, " ".join(v))
                        transformed_response.append(temp_part)
                    elif isinstance(part, tuple):
                        handler = response_handlers.get(part[0])
                        if handler:
                            if part[0] in ("waifu-memory", "dere-response"):
                                transformed_response.append(handler(waifu_memory, part))
                            elif part[0] == "maybe-change-dere":
                                # Access dere_context from waifu_chatbot instance
                                transformed_response.append(handler(waifu_chatbot.dere_context, dere_types, waifu_chatbot))
                            elif part[0] == "talk-about":
                                # Access dere_context from waifu_chatbot instance
                                transformed_response.append(handler(waifu_chatbot.dere_context, part))
                            elif part[0] == "introduce-topic":
                                transformed_response.append(handler(waifu_chatbot.dere_context, part))
                        else:
                            transformed_response.append(str(part))  # Fallback for unknown tuples
                    else:
                        transformed_response.append(str(part))
                transformed_response = " ".join(transformed_response)

            else:
                transformed_response = str(response) # Ensure string conversion

            if memory_slot:
                # Concatenate all substitutions for memory slot
                memory_value = ""
                for k, v in substitutions.items():
                    memory_value += " ".join(v) + " "
                remember(waifu_memory, memory_slot, memory_value.strip(), affection_change)
            if waifu_chatbot.debug:
                print(f"transformations.apply_transformations: Returning transformed response: {transformed_response}")
            return transformed_response

    if waifu_chatbot.topic_manager.current_topic:
        return waifu_chatbot.topic_manager.maybe_introduce_topic(waifu_chatbot.previous_input, waifu_chatbot.turn_count)

    return None