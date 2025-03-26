import random
from typing import List, Set
from dere_context import DereContext
from dere_data import default_responses

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

    # Combine provided responses with a pool of generic, neutral/positive defaults
    # Removed negative/unfitting defaults like "Hmph."
    all_responses = list(responses) + [
        "...",
        "I don't know.",
        "Maybe.",
        "What do you think?",
        "I haven't decided yet.",
        "I'm not sure.",
        "It depends.",
        "Ask me later.",
        "I'll think about it.",
        #"That's a secret." # Can sometimes feel dismissive
        "Hmm, interesting point.", # Added more engaging neutral options
        "Okay, I see.",
    ]

    unused_responses = [resp for resp in all_responses if resp not in used_default_responses]

    if context.debug:
        print(f"responses: {responses}")
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
        response = random.choice(all_responses)
        if context.debug:
            print(f"Chosen response after clearing: {response}")
        used_default_responses.add(response)
        if context.debug:
            print(f"used_default_responses after adding: {used_default_responses}")

        return response