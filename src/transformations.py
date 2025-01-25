from utils import matches

def deftransform(transformations, pattern, response, memory_slot=None, affection_change=0):
    """Defines a transformation pattern and its corresponding response."""
    transformations[pattern] = (response, memory_slot, affection_change)

def apply_transformations(transformations, input_list, waifu_memory, current_dere, talk_about_interest, introduce_topic, dere_response, maybe_change_dere, generate_response, remember, response_templates, used_responses, dere_types, debug):
    """Applies transformations to the input and returns a transformed response."""
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
                        transformed_response.append(talk_about_interest(waifu_memory, current_dere))
                    elif isinstance(part, tuple) and part[0] == "introduce-topic":
                        transformed_response.append(introduce_topic(part[1], waifu_memory, current_dere))
                    else:
                        transformed_response.append(part)
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
