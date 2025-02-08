import random
from typing import List, Set, Tuple

def get_current_dere(affection: int) -> str:
    """
    Determines the current dere type based on the affection level.

    Args:
        affection: The affection level of the waifu.

    Returns:
        The current dere type (e.g., "tsundere", "yandere").
    """
    if affection < -5:
        return "tsundere"
    elif -5 <= affection <= 0:
        return "yandere"
    elif 1 <= affection <= 40:
        return "kuudere"
    elif 41 <= affection <= 75:
        return "dandere"
    else:
        return "deredere"

def maybe_change_dere(waifu_memory: any, current_dere: str, dere_types: List[str], used_responses: Set[str], debug: bool, *responses: str) -> str:
    """Randomly changes the dere type and returns a dere-specific response.

    Args:
        waifu_memory: An object containing the waifu's memory and preferences.
        current_dere: The current dere type of the waifu.
        dere_types: A list of possible dere types.
        used_responses: A set of responses that have already been used.
        debug: A boolean indicating whether to print debug messages.
        *responses: Variable number of dere-specific responses.

    Returns:
        A string containing the dere-specific response.
    """
    if debug:
        print(f"Type of used_responses in maybe_change_dere: {type(used_responses)}")
    if random.randint(0, 9) == 0:
        new_dere = random.choice(dere_types)
        response = dere_response(waifu_memory, new_dere, used_responses, debug, *responses)
        if debug:
            print(f"{waifu_memory.name}: (I feel a little different...)")
            print()
        return response
    return dere_response(waifu_memory, current_dere, used_responses, debug, *responses)

def dere_response(waifu_memory: any, current_dere: str, used_responses: Set[str], debug: bool, *responses: str) -> str:
    """Returns a response based on the current dere type.

    Args:
        waifu_memory: An object containing the waifu's memory and preferences.
        current_dere: The current dere type of the waifu.
        used_responses: A set of responses that have already been used.
        debug: A boolean indicating whether to print debug messages.
        *responses: Variable number of dere-specific responses.

    Returns:
        A string containing the dere-specific response.
    """
    if debug:
        print(f"Type of used_responses in dere_response: {type(used_responses)}")
    if not responses:
        if current_dere == "tsundere":
            responses = ("B-baka! It's not like I care what you say!", "Hmph! Whatever.")
        elif current_dere == "yandere":
            responses = ("You're mine forever, you know that?", "Don't even think about leaving me.", "I will never let you go.", "You belong to me, and me alone.")
        elif current_dere == "kuudere":
            responses = ("Hmph.", "...", "Is that so.", "I see.", "Understood.")
        elif current_dere == "dandere":
            responses = ("U-um...", "O-okay...", "I-I understand...", "If you say so...", "S-sure...")
        elif current_dere == "himedere":
            responses = ("Bow down to me, you peasant!", "You are lucky to be in my presence.", "Hmph, how amusing.", "Do as I command!", "You should be honored.")

    unused_responses = [r for r in responses if r not in used_responses]

 # Ensure responses is always a tuple
    if not unused_responses:
        # Keep 50% of used responses to avoid immediate repetition
        keep_count = len(used_responses) // 2
        used_responses_list = list(used_responses)
        used_responses.clear()
        if keep_count > 0:
            used_responses.update(used_responses_list[-keep_count:])
        unused_responses = list(responses)

    chosen_response = random.choice(unused_responses)
    if isinstance(used_responses, list):
        used_responses = set(used_responses)
    used_responses.add(chosen_response)
    return chosen_response