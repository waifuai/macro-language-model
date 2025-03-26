import random
from dere_utils import dere_response, DereContext  # Updated import
from typing import List, Dict, Any

interest_templates: Dict[str, Dict[str, List[str]]] = {
    "reading manga": {
        "tsundere": ["You know, I've been reading this really great manga lately. It's about a magical girl fighting evil. You should check it out! ...Not that I care if you read it or not. B-baka!"],
        "yandere": ["This manga... it reminds me of us. We're destined to be together, just like the main characters! You'll love it, because I love it, right? We have to like the same things."],
        "kuudere": ["You know, I've been reading this manga lately. It's about a lone swordsman on a quest for revenge. ...Do as you wish."],
        "dandere": ["U-um, I've been reading this manga lately... It's a little embarrassing, but it's kind of special to me... I-if you're interested, that is..."],
        "himedere": ["This manga is a masterpiece! You should be honored that I'm sharing my refined tastes with you!"]
    },
    "watching anime": {
        "tsundere": ["I just finished watching this amazing anime. It's a slice-of-life anime with beautiful animation. I cried at the end, not that I would admit that normally. ...Don't get any weird ideas just because I shared this with you."],
        "yandere": ["I just finished watching this amazing anime. It's a romantic anime with a really catchy soundtrack. We should watch it together, every night! Just the two of us."],
        "kuudere": ["I just finished watching this amazing anime. It's an action-packed anime with a complex plot. ...Suit yourself."],
        "dandere": ["U-um, I really enjoyed this anime... M-maybe we could watch it together sometime...? I-I hope I'm not bothering you by talking about this..."],
        "himedere": ["This anime is a work of art! You should be grateful that I'm gracing you with its presence. You're lucky I'm even telling you about such a masterpiece."]
    },
    "playing video games": {
        "tsundere": ["I'm so addicted to this new game! It's a JRPG where you have to collect rare items. Wanna play with me sometime? ...But don't think this means I'll go easy on you!"],
        "yandere": ["I'm so addicted to this new game! It's a visual novel where you have to build relationships with other characters. We'll be the best team ever! No one will ever defeat us."],
        "kuudere": ["I'm so addicted to this new game! It's a rhythm game where you have to get the highest score. ...If you insist."],
        "dandere": ["U-um, I really like this game... M-maybe we could play it together sometime...? I-I'm not very good, but I'll try my best..."],
        "himedere": ["This game is a masterpiece! You should be honored that I'm even letting you know about it. You'll probably lose, but I'll allow you to play with me."]
    },
    "cooking": {
        "tsundere": ["I-it's not like I made these cookies for you or anything, b-baka! I just had some extra ingredients. They're pocky flavored. ...And don't expect me to cook for you again!"],
        "yandere": ["I made this food with all my love, just for you! Every bite is a taste of my devotion. You'll love everything I cook for you, because it's made with my love."],
        "kuudere": ["Cooking is... an efficient way to get nutrients, I guess. I made some pocky, if you're hungry. ...Don't expect anything special."],
        "dandere": ["U-um, I tried baking a cake... It might be a little burnt, b-but I hope you like it. It's supposed to taste like pocky. ...P-please be honest about how it tastes..."],
        "himedere": ["I have prepared a feast worthy of a princess! It includes your favorite, pocky, of course. You should be grateful that I even considered your tastes!"]
    }
}

def talk_about_interest(waifu_memory: Any, current_dere: str, used_responses: List[str], debug: bool) -> str:
    """
    Generates a response about a random interest, considering the current dere type.

    Args:
        waifu_memory: An object containing the waifu's memory and preferences.
        current_dere: The current dere type of the waifu (e.g., "tsundere", "yandere").
        used_responses: A list of responses that have already been used to avoid repetition.
        debug: A boolean indicating whether to print debug messages.

    Returns:
        A string containing the generated response.
    """
    if not waifu_memory.interests:
        # Use deredere-specific fallbacks if no interests are defined
        deredere_interest_fallbacks = [
            "I haven't thought much about interests yet! What do you like?",
            "Hehe, I'm still discovering my interests! Tell me about yours!",
            "Hmm, interests... Let's talk about something else for now!",
        ]
        return random.choice(deredere_interest_fallbacks)

    interest = random.choice(waifu_memory.interests)
    if interest in interest_templates:
        templates = interest_templates[interest]
        if current_dere in templates:
            response = random.choice(templates[current_dere])
            return response
    # Fallback if specific template for interest/dere combo not found
    deredere_interest_fallbacks = [
        f"Hmm, I like {interest}, but I'm not sure what to say right now! Hehe.",
        f"Talking about {interest} is fun! What do you think about it?",
        f"Oh, {interest}! Let's chat about something else for a moment!",
        "My mind went blank! What were we talking about? Haha!",
    ]
    # Use deredere fallbacks if current_dere is deredere, otherwise a generic positive one
    if current_dere == "deredere":
         return random.choice(deredere_interest_fallbacks)
    else:
         # Generic positive fallback for other deres if template missing
         return f"That's an interesting topic ({interest})! Tell me more about what you think."

def introduce_topic(topic: str, waifu_memory: Any, current_dere: str, used_responses: List[str], debug: bool) -> str:
    """Introduces a new topic with a relevant dere-style phrase.

    Args:
        topic: The topic to introduce (e.g., "family", "childhood").
        waifu_memory: An object containing the waifu's memory and preferences.
        current_dere: The current dere type of the waifu.
        used_responses: A list of responses that have already been used.
        debug: A boolean indicating whether to print debug messages.

    Returns:
        A string containing the introduction to the topic.
    """
    dere_context = DereContext(waifu_memory, current_dere, set(used_responses), debug)
    response = dere_response(dere_context, set(),
        "Hmph, why do you want to talk about this all of a sudden?",
        "I suppose we can talk about that, if you insist.",
        "Um, what about this...?",
        "You should be honored that I'm even talking to you about this!"
    )

    if topic == "favorite_food":
        return f"{response} What's your favorite food?"
    elif topic == "relationship_status":
        return f"{response} How do you feel about our relationship?"
    else:
        return f"{response} Could you tell me more about {topic}?"