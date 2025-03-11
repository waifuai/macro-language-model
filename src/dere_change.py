import random
from typing import List, Set, Tuple, NamedTuple, Dict, Any
from dere_context import DereContext
from dere_response_selection import dere_response
from dere_data import dere_types, default_responses

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
        change_probability = 0.4  # Increased chance for extreme affection
    else:
        change_probability = 0.3  # Increased base chance

    # Check for consecutive identical responses
    if len(waifu_chatbot.conversation_context.conversation_history) >= 2:
        last_response = waifu_chatbot.conversation_context.conversation_history[-1][1]
        second_last_response = waifu_chatbot.conversation_context.conversation_history[-2][1]
        if last_response == second_last_response:
            change_probability = 0.7  # Significantly increase if responses are identical

    # Check for turns with the same dere type
    if waifu_chatbot.dere_context.current_dere == context.current_dere:
        waifu_chatbot.turns_in_same_dere += 1
    else:
        waifu_chatbot.turns_in_same_dere = 1 # Reset if dere type changes.
        waifu_chatbot.dere_context = context._replace(current_dere=waifu_chatbot.dere_context.current_dere)

    if waifu_chatbot.turns_in_same_dere > 2: # Reduced turns before increasing probability
        change_probability = 0.6 # Increase probability after 2 turns in the same dere type.

    if random.random() < change_probability:
        new_dere = random.choice(dere_types)
        context = context._replace(current_dere=new_dere)  # Update context directly
        # Update current_dere in waifu_memory
        waifu_chatbot.dere_context = DereContext(waifu_chatbot.waifu_memory, new_dere, set(), context.debug) # Create a NEW DereContext
        waifu_chatbot.turns_in_same_dere = 1  # Reset turns in same dere
        # Pass default responses for the *new* dere type
        response = dere_response(context, waifu_chatbot.response_generator.used_default_responses, *default_responses.get(new_dere, ["..."]))
        if context.debug:
            print(f"{context.waifu_memory.name}: (I feel a little different...)")
            print()
            return response
    # Pass default responses for the *current* dere type
    return dere_response(context, waifu_chatbot.response_generator.used_default_responses, *default_responses.get(context.current_dere, ["..."]))