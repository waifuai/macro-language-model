import random
from typing import List, Set, Tuple, NamedTuple, Dict, Any
from dere_context import DereContext

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

        # Combine provided responses with a larger pool of defaults
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
            "That's a secret."
        ]

        unused_responses = [resp for resp in all_responses if resp not in used_default_responses]
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
        response = random.choice(all_responses)
        if context.debug:
            print(f"Chosen response after clearing: {response}")
        used_default_responses.add(response)
        if context.debug:
            print(f"used_default_responses after adding: {used_default_responses}")

        return response

def get_dere_default_response(context: DereContext, used_default_responses: Set[str]) -> str:
    """Returns a more intelligent default response based on the dere type."""
    dere_defaults = {
        "tsundere": [
            "Hmph, whatever.",
            "It's not like I care, b-baka!",
            "Don't get the wrong idea!",
            "Whatever you say...",
            "I'm not interested in that.",
            "Baka! Why would you ask that?",
            "Don't ask stupid questions.",
            "Hmph. As if I'd tell you.",
            "That's none of your concern."
        ],
        "yandere": [
            "...",
            "I only care about you.",
            "Don't leave me.",
            "We'll be together forever.",
            "You're mine.",
            "Where are you going?",
            "Who were you talking to?",
            "You're not thinking about anyone else, are you?",
            "I'll always be watching you.",
            "Stay with me."
        ],
        "kuudere": [
            "...",
            "I see.",
            "That is logical.",
            "Indifferent.",
            "As you wish.",
            "That is irrelevant.",
            "Unnecessary.",
            "Explain.",
            "Continue.",
            "Observation noted."
        ],
        "dandere": [
            "U-um...",
            "I-I'm sorry...",
            "O-okay...",
            "I-I'll try my best...",
            "E-excuse me...",
            "P-please don't be mad...",
            "I-I didn't mean to...",
            "S-sorry...",
            "Y-yes?",
            "I-is that so...?"
        ],
        "himedere": [
            "Fufufu...",
            "Kneel before me!",
            "You should be honored.",
            "Of course.",
            "Remember your place.",
            "I am superior.",
            "Naturally.",
            "You are amusing.",
            "How predictable.",
            "Impress me."
        ],
        "deredere": [
            "Okay!",
            "Sure!",
            "I understand.",
            "No problem!",
            "Got it!",
            "Sounds good!",
            "Alright!",
            "Yeah!",
            "I'm here for you!",
            "Let's do it!"
        ]
    }

    default_list = dere_defaults.get(context.current_dere, ["..."])
    unused_responses = [resp for resp in default_list if resp not in used_default_responses]

    if unused_responses:
        response = random.choice(unused_responses)
        used_default_responses.add(response)
        return response
    else:
        used_default_responses.clear()
        return random.choice(default_list)