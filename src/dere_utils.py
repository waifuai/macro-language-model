from typing import List, Dict, Any, Optional, Set
import random
# Removed: from dere_data import dere_types  # Import dere_types from dere_data
from dere_types import DereContext  # Import DereContext

# Removed class DereContext

def maybe_change_dere(context: DereContext, dere_types: List[str]) -> Optional[str]:
    """Potentially changes the waifu's dere type based on affection and randomness."""
    if context.debug:
        print(f"maybe_change_dere called with context: {context}")
    if context.waifu_memory.affection > 80:
        if random.random() < 0.2:  # 20% chance to switch
            new_dere = random.choice(dere_types)
            if context.debug:
                print(f"Changing dere from {context.current_dere} to {new_dere}")
            context.current_dere = new_dere
            return f"Dere type changed to {new_dere}!"
    elif context.waifu_memory.affection < 20:
        if random.random() < 0.2:  # 20% chance to switch
            new_dere = random.choice(dere_types)
            if context.debug:
                print(f"Changing dere from {context.current_dere} to {new_dere}")
            context.current_dere = new_dere
            return f"Dere type changed to {new_dere}!"
    if context.debug:
        print(f"Dere unchanged. Affection: {context.waifu_memory.affection}")
    return None

def dere_response(context: DereContext, *responses: str) -> str:
    """Returns a random dere-specific response, avoiding repetition.

    Args:
        context: The DereContext containing waifu memory, current dere, used responses, and debug flag.
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

    unused_responses = [resp for resp in all_responses if resp not in context.used_responses]

    if context.debug:
        print(f"responses: {responses}")
        print(f"unused_responses: {unused_responses}")

    if unused_responses:
        response = random.choice(unused_responses)
        if context.debug:
            print(f"Chosen response: {response}")
        context.used_responses.add(response)
        if context.debug:
            print(f"used_responses after adding: {context.used_responses}")
        return response
    else:
        # All responses have been used, so we clear the used_responses
        # and pick a response again.
        if context.debug:
            print("All responses used, clearing used_responses")
        context.used_responses.clear()
        response = random.choice(all_responses)
        if context.debug:
            print(f"Chosen response after clearing: {response}")
        context.used_responses.add(response)
        if context.debug:
            print(f"used_responses after adding: {context.used_responses}")

        return response

def get_dere_default_response(context: DereContext) -> str:
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
            "Let's do it!",
            "Tell me more!", # Added
            "That's interesting!", # Added
            "I'm listening!", # Added
            "Go on!", # Added
            "What then?", # Added
            "Hmm...", # Added
            "I see..." # Added
        ]
    }

    default_list = dere_defaults.get(context.current_dere, ["..."])
    unused_responses = [resp for resp in default_list if resp not in context.used_responses]

    if unused_responses:
        response = random.choice(unused_responses)
        context.used_responses.add(response)
        return response
    else:
        context.used_responses.clear()
        return random.choice(default_list)