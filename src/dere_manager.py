import random
from typing import List, Set, Tuple, NamedTuple, Dict, Any
from conversation_context import ConversationContext # New import

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
    if random.randint(0, 9) == 0:  # Increased probability to 10%
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

dere_types: List[str] = ["tsundere", "yandere", "kuudere", "dandere", "himedere"]

default_responses: Dict[str, List[str]] = {
    "tsundere": [
        "Hmph, what do *you* want?",
        "It's not like I care what you say, b-baka!",
        "Whatever.",
        "Don't get the wrong idea!",
        "I'm not doing this for *you* or anything.",
        "B-baka!",
        "What are you looking at?",
        "It's not like I like you or anything...",
        "Don't misunderstand, okay?",
        "I'm only talking to you because I have nothing better to do."
    ],
    "yandere": [
        "Oh, you're back! I was waiting for you.",
        "Where have you been? I was so worried...",
        "You're the only one I care about.",
        "Don't leave me again, okay?",
        "We'll be together forever, right?",
        "I can't live without you.",
        "You're mine, and mine alone.",
        "I'll do anything for you.",
        "No one else matters but you.",
        "I'm watching you, always."
    ],
    "kuudere": [
        "...",
        "I see.",
        "That is logical.",
        "Hmph.",
        "Understood.",
        "Affirmative.",
        "Negative.",
        "Indifferent.",
        "As you wish.",
        "It is irrelevant."
    ],
    "dandere": [
        "U-um...",
        "I-I'm sorry...",
        "P-please don't be mad...",
        "O-okay...",
        "I-I'll try my best...",
        "D-do you need something?",
        "I-is everything alright?",
        "M-maybe we could...",
        "E-excuse me...",
        "I-I didn't mean to bother you..."
    ],
    "himedere": [
        "Fufufu, you're finally back.",
        "Kneel before me!",
        "You should be honored to be in my presence.",
        "Of course, I'm always right.",
        "Remember your place.",
        "I am superior in every way.",
        "You are beneath me.",
        "Bow down, peasant!",
        "My word is law.",
        "I deserve all the praise."
    ]
}