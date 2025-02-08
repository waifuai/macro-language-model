from typing import Dict, List, Tuple, Callable, Any, Optional, Set

from utils import matches
from dere_types import DereContext

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

def _handle_generate_response(context: DereContext, part: tuple, substitutions: Dict[str, List[str]], response_templates: Dict[tuple[str, str], List[str]], dere_response: Callable[..., str], debug: bool) -> str:
    """Handles the 'generate' response type."""
    keyword = part[1]
    sub_dict = {}
    for sub_key, sub_value in part[2]:
        # Get substitutions for all wildcards in the tuple
        all_values = []
        for k, v in substitutions.items():
            all_values.extend(v)
        sub_dict[sub_key] = all_values
    return generate_response(response_templates, keyword, sub_dict, context.used_responses, context.waifu_memory, context.current_dere, dere_response, debug)

def _handle_waifu_memory_response(waifu_memory: Any, part: tuple) -> str:
    """Handles the 'waifu-memory' response type."""
    return str(getattr(waifu_memory, part[1]))

def _handle_dere_response(context: DereContext, part: tuple) -> str:
    """Handles the 'dere-response' response type."""
    return dere_response(context, *part[1:])

def _handle_maybe_change_dere(context: DereContext, dere_types: List[str], part: tuple) -> str:
    """Handles the 'maybe-change-dere' response type."""
    return maybe_change_dere(context, dere_types, *part[1:])

def _handle_talk_about(context: DereContext) -> str:
    """Handles the 'talk-about' response type."""
    return talk_about_interest(context.waifu_memory, context.current_dere, context.used_responses, context.debug)

def _handle_introduce_topic(context: DereContext, part: tuple) -> str:
    """Handles the 'introduce-topic' response type."""
    return introduce_topic(part[1], context.waifu_memory, context.current_dere, context.used_responses, context.debug)

def apply_transformations(transformations: Dict[str, Tuple[Any, Optional[str], int]], input_list: List[str], waifu_memory: Any, current_dere: str, talk_about_interest: Callable[..., str], introduce_topic: Callable[..., str], dere_response: Callable[..., str], maybe_change_dere: Callable[..., str], generate_response: Callable[..., str], remember: Callable[..., None], response_templates: Dict[tuple[str, str], List[str]], used_responses: Set[str], dere_types: List[str], debug: bool) -> Optional[str]:
    dere_context = DereContext(waifu_memory, current_dere, used_responses, debug)
    if debug:
        print(f"Type of used_responses in apply_transformations: {type(used_responses)}")
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
                    elif isinstance(part, tuple) and part[0] == "generate":
                        transformed_response.append(_handle_generate_response(dere_context, part, substitutions, response_templates, dere_response, debug))
                    elif isinstance(part, tuple) and part[0] == "waifu-memory":
                        transformed_response.append(_handle_waifu_memory_response(waifu_memory, part))
                    elif isinstance(part, tuple) and part[0] == "dere-response":
                        transformed_response.append(_handle_dere_response(dere_context, part))
                    elif isinstance(part, tuple) and part[0] == "maybe-change-dere":
                        transformed_response.append(_handle_maybe_change_dere(dere_context, dere_types, part))
                    elif isinstance(part, tuple) and part[0] == "talk-about":
                        transformed_response.append(_handle_talk_about(dere_context))
                    elif isinstance(part, tuple) and part[0] == "introduce-topic":
                        transformed_response.append(_handle_introduce_topic(dere_context, part))
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

            return None  # Correct return

    if waifu_memory.current_topic:
        return introduce_topic(waifu_memory.current_topic, waifu_memory,
                             current_dere, used_responses, debug)
    return None
