import random
from typing import Set
from dere_context import DereContext
from dere_data import default_responses

def get_dere_default_response(context: DereContext, used_default_responses: Set[str]) -> str:
    """Returns a more intelligent default response based on the dere type."""
    dere_defaults = default_responses

    default_list = dere_defaults.get(context.current_dere, ["..."])
    unused_responses = [resp for resp in default_list if resp not in used_default_responses]

    if unused_responses:
        response = random.choice(unused_responses)
        used_default_responses.add(response)
        return response
    else:
        used_default_responses.clear()
        return random.choice(default_list)