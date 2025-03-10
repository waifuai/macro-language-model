from typing import Dict, List, Tuple, Callable, Any, Optional, Set

from utils import matches
from dere_manager import DereContext, dere_types
from transformation_handlers import (
    handle_generate_response,
    handle_waifu_memory_response,
    handle_dere_response,
    handle_maybe_change_dere,
    handle_talk_about,
    handle_introduce_topic
)
from topic_manager import TopicManager # New import

def deftransform(transformations: Dict[str, Tuple[Any, Optional[str], int]], pattern: str, response: Any, memory_slot: Optional[str] = None, affection_change: int = 0) -> None:
    """Defines a transformation pattern and its corresponding response.

    Args:
        transformations: A dictionary to store the transformations.
        pattern: The pattern to match against the input.
        response: The response to return if the pattern matches.
        memory_slot: The memory slot to store the matched value in.
        affection_change: The amount to change the waifu's affection by.
    """
    transformations[pattern] = (response, memory_slot, affection_change)

def apply_transformations(transformations: Dict[str, Tuple[Any, Optional[str], int]], input_list: List[str], waifu_memory: Any, current_dere: str, talk_about_interest: Callable[..., str], introduce_topic: Callable[..., str], dere_response: Callable[..., str], maybe_change_dere: Callable[..., str], generate_response: Callable[..., str], remember: Callable[..., None], response_templates: Dict[tuple[str, str], List[str]], used_responses: Set[str], dere_types: List[str], debug: bool, waifu_chatbot: Any) -> Optional[str]:
    """Applies transformations to the input and returns a transformed response."""
    if waifu_chatbot.debug:
        print(f"transformations.apply_transformations: Entering with input: {input_list}")
    # Dictionary to map response types to handler functions
    response_handlers: Dict[str, Callable] = {
        "generate": handle_generate_response,
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
                            if part[0] == "generate":
                                # Access dere_context from waifu_chatbot instance
                                transformed_response.append(handler(waifu_chatbot, part, substitutions, response_templates, dere_response,  waifu_chatbot.debug))
                            elif part[0] in ("waifu-memory", "dere-response"):
                                transformed_response.append(handler(waifu_memory, part))
                            elif part[0] == "maybe-change-dere":
                                # Access dere_context from waifu_chatbot instance
                                transformed_response.append(handler(waifu_chatbot.dere_context, dere_types, part))
                            elif part[0] == "talk-about":
                                # Access dere_context from waifu_chatbot instance
                                transformed_response.append(handler(waifu_chatbot.waifu_memory, waifu_chatbot.dere_context.current_dere, list(waifu_chatbot.dere_context.used_responses), waifu_chatbot.debug))
                            elif part[0] == "introduce-topic":
                                transformed_response.append(handler(part[1], waifu_chatbot.waifu_memory, waifu_chatbot.dere_context.current_dere, list(waifu_chatbot.dere_context.used_responses), waifu_chatbot.debug))
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

    # Access TopicManager from the WaifuChatbot instance
    if waifu_chatbot.topic_manager.current_topic:
        return introduce_topic(waifu_chatbot.topic_manager.current_topic, waifu_memory,
                             # Access dere_context from waifu_chatbot instance
                             current_dere, list(used_responses),  waifu_chatbot.debug)
    return None
