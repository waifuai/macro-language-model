from typing import Dict, List, Tuple, Callable, Any, Optional, Set

from utils import matches

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

def apply_transformations(transformations: Dict[str, Tuple[Any, Optional[str], int]], input_list: List[str], waifu_memory: Any, current_dere: str, talk_about_interest: Callable[..., str], introduce_topic: Callable[..., str], dere_response: Callable[..., str], maybe_change_dere: Callable[..., str], generate_response: Callable[..., str], remember: Callable[..., None], response_templates: Dict[tuple[str, str], List[str]], used_responses: Set[str], dere_types: List[str], debug: bool) -> Optional[str]:
    """Applies transformations to the input and returns a transformed response.

    Args:
        transformations: A dictionary of transformations.
        input_list: A list of words from the user input.
        waifu_memory: The waifu's memory object.
        current_dere: The current dere type of the waifu.
        talk_about_interest: A function to talk about the waifu's interests.
        introduce_topic: A function to introduce a new topic.
        dere_response: A function to generate a dere-specific response.
        maybe_change_dere: A function to maybe change the dere type.
        generate_response: A function to generate a response.
        remember: A function to remember something.
        response_templates: A dictionary of response templates.
        used_responses: A set of used responses.
        dere_types: A list of dere types.
        debug: A boolean indicating whether to print debug messages.

    Returns:
        A string containing the transformed response, or None if no transformation was applied.
    """
    if debug:
        print(f"Type of used_responses in apply_transformations: {type(used_responses)}")
    for pattern, (response, memory_slot, affection_change) in transformations.items():
        pattern_list = pattern.split()
        if matches(pattern_list, input_list):
            substitutions = {}
            j = 0
            for i in range(len(pattern_list)):
                if pattern_list[i] == '*':
                    substitutions[pattern_list[i]] = []
                    while j < len(input_list) and (i == len(pattern_list) - 1 or (i + 1 < len(pattern_list) and input_list[j] != pattern_list[i + 1])):
                        substitutions[pattern_list[i]].append(input_list[j])
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
                    if isinstance(part, tuple) and part[0] == "generate":
                        keyword = part[1]
                        sub_dict = {}
                        for sub_key, sub_value in part[2]:
                            sub_dict[sub_key] = substitutions.get(sub_value, [])
                        transformed_response.append(
                            generate_response(response_templates, keyword, sub_dict, used_responses, waifu_memory, current_dere, dere_response, debug)
                        )
                    elif isinstance(part, tuple) and part[0] == "waifu-memory":
                        transformed_response.append(getattr(waifu_memory, part[1]))
                    elif part in substitutions:
                        transformed_response.append(" ".join(substitutions[part]))
                    elif isinstance(part, tuple) and part[0] == "dere-response":
                        transformed_response.append(dere_response(waifu_memory, current_dere, used_responses, debug, *part[1:]))
                    elif isinstance(part, tuple) and part[0] == "maybe-change-dere":
                        transformed_response.append(maybe_change_dere(waifu_memory, current_dere, dere_types, used_responses, debug, *part[1:]))
                    elif isinstance(part, tuple) and part[0] == "talk-about":
                        transformed_response.append(talk_about_interest(waifu_memory, current_dere, used_responses, debug))
                    elif isinstance(part, tuple) and part[0] == "introduce-topic":
                        transformed_response.append(introduce_topic(part[1], waifu_memory, current_dere, used_responses, debug))
                    else:
                        transformed_response.append(part)
                # Correctly substitute placeholders in transformed_response when it's a list
                for i in range(len(transformed_response)):
                    if isinstance(transformed_response[i], str):
                        transformed_response[i] = transformed_response[i].replace("*", " ".join(substitutions.get("*", "")))
            else:
                transformed_response = response

            if memory_slot:
                value = " ".join(substitutions['*'])
                remember(waifu_memory, memory_slot, value, affection_change)

            if isinstance(transformed_response, list):
                return ' '.join(transformed_response)
            else:
                return transformed_response
    if waifu_memory.current_topic:
        return introduce_topic(waifu_memory.current_topic, waifu_memory,
                             current_dere, used_responses, debug)
    return None
