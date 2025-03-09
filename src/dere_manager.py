import random
from typing import List, Set, Tuple, NamedTuple, Dict, Any
from conversation_context import ConversationContext # New import
from dere_data import dere_types, default_responses

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

def maybe_change_dere(context: DereContext, dere_types: List[str], waifu_chatbot: Any) -> str: # Added waifu_chatbot
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

    # Determine the probability of changing dere type
    if context.waifu_memory.affection < 10 or context.waifu_memory.affection > 90:
        change_probability = 0.1  # 10% chance for extreme affection
    else:
        change_probability = 0.05  # 5% chance for normal affection

    if random.random() < change_probability:
        new_dere = random.choice(dere_types)
        context = context._replace(current_dere=new_dere)  # Update context directly
        # Update current_dere in waifu_memory
        waifu_chatbot.dere_context = context # Update the dere_context in waifu chatbot
        # Pass default responses for the *new* dere type
        response = dere_response(context, waifu_chatbot.response_generator.used_default_responses, *default_responses.get(new_dere, ["..."]))
        if context.debug:
            print(f"{context.waifu_memory.name}: (I feel a little different...)")
            print()
            return response
    # Pass default responses for the *current* dere type
    return dere_response(context, waifu_chatbot.response_generator.used_default_responses, *default_responses.get(context.current_dere, ["..."]))

def dere_response(context: DereContext, used_default_responses: Set[str], *responses: str) -> str:
    """Returns a random dere-specific response, avoiding repetition.

    Args:
        context: The DereContext containing waifu memory, current dere, used responses, and debug flag.
        used_default_responses: Set of default responses that have been used.
        *responses: Variable number of dere-specific responses.

    Returns:
        A dere-specific response.
    """
    if context.debug:
        print(f"dere_response called with context: {context}") # Debug print
    if not responses:  # Handle the case where no responses are provided
        if context.debug:
            print("No responses provided to dere_response, returning '...'")
        return "..." # Or some other default

    if context.debug:
        print(f"responses: {responses}")

    unused_responses = [resp for resp in responses if resp not in used_default_responses]
    if context.debug:
        print(f"unused_responses: {unused_responses}")

    if unused_responses:
        response = random.choice(unused_responses)
        if context.debug:
            print(f"Chosen response: {response}")
        used_default_responses.add(response)
        if context.debug:
            print(f"used_default_responses after adding: {used_default_responses}")
        return response
    else:
        # All responses have been used, so we clear the used_responses
        # and pick a response again.
        if context.debug:
            print("All responses used, clearing used_default_responses")
        used_default_responses.clear()
        response = random.choice(responses)
        if context.debug:
            print(f"Chosen response after clearing: {response}")
        used_default_responses.add(response)
        if context.debug:
            print(f"used_default_responses after adding: {used_default_responses}")

        return response