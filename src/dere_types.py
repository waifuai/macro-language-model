import random
from typing import List, Set, Tuple, NamedTuple

class DereContext(NamedTuple):
    waifu_memory: any
    current_dere: str
    used_responses: Set[str]
    debug: bool

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

def maybe_change_dere(context: DereContext, dere_types: List[str], *responses: str) -> str:
    """Randomly changes the dere type and returns a dere-specific response.

    Args:
        context: The DereContext containing waifu memory, current dere, used responses, and debug flag.
        dere_types: A list of possible dere types.
        *responses: Variable number of dere-specific responses.

    Returns:
        A string containing the dere-specific response.
    """
    if context.debug:
        print(f"Type of used_responses in maybe_change_dere: {type(context.used_responses)}")
    if random.randint(0, 9) == 0:
        new_dere = random.choice(dere_types)
        context = context._replace(current_dere=new_dere)  # Update context directly
        response = dere_response(context, *responses)
        if context.debug:
            print(f"{context.waifu_memory.name}: (I feel a little different...)")
            print()
        return response
    return dere_response(context, *responses)

def dere_response(context: DereContext, *responses: str) -> str:
    """Returns a random dere-specific response, avoiding repetition.

    Args:
        context: The DereContext containing waifu memory, current dere, used responses, and debug flag.
        *responses: Variable number of dere-specific responses.

    Returns:
        A dere-specific response.
    """

    if not responses:  # Handle the case where no responses are provided
        return "..." # Or some other default

    unused_responses = [resp for resp in responses if resp not in context.used_responses]

    if unused_responses:
        response = random.choice(unused_responses)
        context.used_responses.add(response)
        return response
    else:
        # All responses have been used, so we clear the used_responses
        # and pick a response again.
        context.used_responses.clear()
        response = random.choice(responses)
        context.used_responses.add(response)
        return response