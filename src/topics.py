import random
from dere_types import dere_response
from typing import List, Dict, Any

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
    if debug:
        print(f"Type of used_responses in talk_about_interest: {type(used_responses)}")
    interest = random.choice(waifu_memory.interests)
    if interest == "reading manga":
        genre = dere_response(waifu_memory, current_dere, used_responses, debug, 'a magical girl fighting evil', 'a group of friends who form a band', 'a lone swordsman on a quest for revenge')
        response = f"You know, I've been reading this really great manga lately. It's about {genre}. You should check it out!"
    elif interest == "watching anime":
        genre = dere_response(waifu_memory, current_dere, used_responses, debug, 'slice-of-life', 'action-packed', 'romantic')
        response = f"I just finished watching this amazing anime. It's a {genre} anime with {dere_response(waifu_memory, current_dere, used_responses, debug, 'beautiful animation', 'a really catchy soundtrack', 'a complex plot')}. I cried at the end, not that I would admit that normally."
    elif interest == "playing video games":
        genre = dere_response(waifu_memory, current_dere, used_responses, debug, 'JRPG', 'visual novel', 'rhythm game')
        response = f"I'm so addicted to this new game! It's a {genre} where you have to {dere_response(waifu_memory, current_dere, used_responses, debug, 'collect rare items', 'build relationships with other characters', 'get the highest score')}. Wanna play with me sometime?"
    elif interest == "cooking":
        response = dere_response(waifu_memory, current_dere, used_responses, debug,
            f"I-it's not like I made these cookies for you or anything, b-baka! I just had some extra ingredients. They're {waifu_memory.favorite_food} flavored.",
            f"Cooking is... an efficient way to get nutrients, I guess. I made some {waifu_memory.favorite_food}, if you're hungry.",
            f"U-um, I tried baking a cake... It might be a little burnt, b-but I hope you like it. It's supposed to taste like {waifu_memory.favorite_food}",
            f"Fufufu, I have prepared a feast worthy of a princess! It includes your favorite, {waifu_memory.favorite_food}, of course."
        )
    else:
        response = dere_response(waifu_memory, current_dere, used_responses, debug,
            "What are you talking about?", "I don't get it.", "Hmph.", "O-okay..."
        )

    # Add a follow-up question or comment based on the current dere type and interest
    if current_dere == "tsundere":
        if interest == "reading manga":
            response += " ...Not that I care if you read it or not. B-baka!"
        elif interest == "watching anime":
            response += " ...Don't get any weird ideas just because I shared this with you."
        elif interest == "playing video games":
            response += " ...But don't think this means I'll go easy on you!"
        elif interest == "cooking":
            response += " ...And don't expect me to cook for you again!"
    elif current_dere == "yandere":
        if interest == "reading manga":
            response += " You'll love it, because I love it, right? We have to like the same things."
        elif interest == "watching anime":
            response += " We should watch it together, every night! Just the two of us."
        elif interest == "playing video games":
            response += " We'll be the best team ever! No one will ever defeat us."
        elif interest == "cooking":
            response += " You'll love everything I cook for you, because it's made with my love."
    elif current_dere == "kuudere":
        if interest == "reading manga":
            response += " ...Do as you wish."
        elif interest == "watching anime":
            response += " ...Suit yourself."
        elif interest == "playing video games":
            response += " ...If you insist."
        elif interest == "cooking":
            response += " ...Don't expect anything special."
    elif current_dere == "dandere":
        if interest == "reading manga":
            response += " ...I-if you're interested, that is..."
        elif interest == "watching anime":
            response += " ...I-I hope I'm not bothering you by talking about this..."
        elif interest == "playing video games":
            response += " ...I-I'm not very good, but I'll try my best..."
        elif interest == "cooking":
            response += " ...P-please be honest about how it tastes..."
    elif current_dere == "himedere":
        if interest == "reading manga":
            response += " You should be honored that I'm sharing my refined tastes with you!"
        elif interest == "watching anime":
            response += " You're lucky I'm even telling you about such a masterpiece."
        elif interest == "playing video games":
            response += " You'll probably lose, but I'll allow you to play with me."
        elif interest == "cooking":
            response += " You should be grateful that I even considered your tastes!"

    return response

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
    if debug:
        print(f"Type of used_responses in introduce_topic: {type(used_responses)}")
    
    response = dere_response(waifu_memory, current_dere, used_responses, debug,
        "Hmph, why do you want to talk about this all of a sudden?",
        "I suppose we can talk about that, if you insist.",
        "Um, what about this...?",
        "You should be honored that I'm even talking to you about this!"
    )
    
    return f"{response} Could you tell me more about {topic}?"