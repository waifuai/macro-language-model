import random
from dere_types import dere_response

def talk_about_interest(waifu_memory, current_dere, used_responses, debug):
    """Generates a response about a random interest, considering the current dere type."""
    if debug:
        print(f"Type of used_responses in talk_about_interest: {type(used_responses)}")
    interest = random.choice(waifu_memory.interests)
    if interest == "reading manga":
        response = f"You know, I've been reading this really great manga lately. It's about {dere_response(waifu_memory, current_dere, used_responses, debug, 'a magical girl fighting evil', 'a group of friends who form a band', 'a lone swordsman on a quest for revenge')}. You should check it out!"
    elif interest == "watching anime":
        response = f"I just finished watching this amazing anime. It's a {dere_response(waifu_memory, current_dere, used_responses, debug, 'slice-of-life', 'action-packed', 'romantic')} anime with {dere_response(waifu_memory, current_dere, used_responses, debug, 'beautiful animation', 'a really catchy soundtrack', 'a complex plot')}. I cried at the end, not that I would admit that normally."
    elif interest == "playing video games":
        response = f"I'm so addicted to this new game! It's a {dere_response(waifu_memory, current_dere, used_responses, debug, 'JRPG', 'visual novel', 'rhythm game')} where you have to {dere_response(waifu_memory, current_dere, used_responses, debug, 'collect rare items', 'build relationships with other characters', 'get the highest score')}. Wanna play with me sometime?"
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

def introduce_topic(topic, waifu_memory, current_dere, used_responses, debug):
    """Introduces a new topic with a relevant dere-style phrase."""
    if debug:
        print(f"Type of used_responses in introduce_topic: {type(used_responses)}")
    if topic == "family":
        return dere_response(waifu_memory, current_dere, used_responses, debug,
            "Hmph, why do you want to talk about family all of a sudden?",
            "Family... I suppose we can talk about that, if you insist.",
            "F-family? Um, what about them...?",
            "Your family must be honored to be associated with someone as magnificent as me!"
        ) + " Could you tell me more about your family?"
    elif topic == "childhood":
        return dere_response(waifu_memory, current_dere, used_responses, debug,
            "Childhood memories? Don't bore me with such childish things.",
            "My childhood is none of your concern... unless you're planning to be part of my future.",
            "M-my childhood? I-I don't really want to talk about it...",
            "Even as a child, I was destined for greatness!"
        ) + " What was your childhood like?"
    elif topic == "feelings":
        return dere_response(waifu_memory, current_dere, used_responses, debug,
            "Feelings? Don't be ridiculous, I don't care about your feelings!",
            "Your feelings are my command... don't ever forget that.",
            "Feelings... an interesting concept.",
            "M-my feelings? W-well..."
        ) + " How are you feeling right now?"
    elif topic == "interests":
        return dere_response(waifu_memory, current_dere, used_responses, debug,
            "Hmph, why are you suddenly interested in what I like?",
            "My interests? You'll find out soon enough...",
            "M-my interests? W-well...",
            "A princess has many interests! You couldn't possibly comprehend them all."
        ) + " What are you interested in?"
    elif topic == "relationship_status":
        if current_dere == "tsundere":
            return "H-huh? What's that supposed to mean, baka?! It's not like I care about our relationship status or anything!" + " What do you think about our relationship status?"
        elif current_dere == "yandere":
            return "Our relationship status? We're together forever, of course! There's no other option~" + " Do you agree that we are together forever?"
        elif current_dere == "kuudere":
            return "Relationship status... That's irrelevant. Do what you want." + " What do you want our relationship status to be?"
        elif current_dere == "dandere":
            return "U-um, our relationship status...? I-I... I l-like you..." + " How do you feel about our relationship status?"
        elif current_dere == "himedere":
            return "Hmph, as if a peasant like you could ever change my relationship status. But if you must know, we are destined to be together!" + " Do you think we are destined to be together?"
    elif topic == "favorite_food":
        favorite_food = waifu_memory.favorite_food
        return dere_response(waifu_memory, current_dere, used_responses, debug,
            f"Hmph, why do you want to know about my favorite food all of a sudden? It's {favorite_food}, by the way.",
            f"My favorite food...? I'll only tell you if you prove your worth. It's {favorite_food}, just so you know.",
            f"M-my favorite food? I-It's {favorite_food}...",
            f"A princess enjoys only the finest delicacies! My favorite food, {favorite_food}, is obviously superior to yours."
        ) + f" What's your favorite food? Do you like {favorite_food}?"
    elif topic == "personality_quirks":
        if current_dere == "tsundere":
            return "Hmph, personality quirks? It's not like I have any weird habits or anything! B-baka!" + " Do you think I have personality quirks?"
        elif current_dere == "yandere":
            return "My only quirk is loving you too much! Is that a problem? You're not thinking of leaving me, are you?" + " What personality quirks do you like in a person?"
        elif current_dere == "kuudere":
            return "Quirks... I have no particular quirks. ...Unless you consider my indifference a quirk." + " What personality quirks do you think I have?"
        elif current_dere == "dandere":
            return "P-personality quirks...? U-um... I-I don't think I have any... I-I hope that's okay..." + " Do you have any personality quirks?"
        elif current_dere == "himedere":
            return "Personality quirks? A princess is perfect in every way! Any so-called 'quirks' are simply traits that make me even more unique and desirable!" + " What are your personality quirks?"
    else:
        return dere_response(waifu_memory, current_dere, used_responses, debug,
            "What's that supposed to mean?",
            "Are you trying to change the subject? Don't think you can escape my grasp.",
            "...",
            "U-um, okay..."
        ) + " ...So, what were we talking about?"