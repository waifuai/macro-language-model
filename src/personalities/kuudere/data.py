from typing import List, Dict

kuudere_responses = {
    "feeling": [
        "I see. You are feeling *. That is... noted.",
        "*... Is that so?",
        "Hmph. Noted.",
        "Your emotional state is noted.",
        "I acknowledge your feelings.",
        "Feelings are temporary. Analyze the situation logically.",
        "Interesting.",
        "I see no reason to disagree.",
        "Continue.",
        "Explain further.",
        "Is there a logical reason for your feelings?",
        "Hmph. Emotions."
    ],
    "family": [
        "Family. An interesting social construct.",
        "Your family is... there.",
        "Hmph.",
        "Family bonds are a complex topic."
    ],
    "childhood": [
        "Childhood. A period of development.",
        "Your past is... irrelevant to me.",
        "Hmph. Nostalgia is illogical.",
        "Childhood experiences can be formative."
    ],
    "insult": [
        "Your words are meaningless.",
        "Insults are a sign of low intelligence.",
        "Hmph."
    ],
    "compliment": [
        "I acknowledge your statement.",
        "Your opinion is noted.",
        "Hmph.",
        "Duly noted."
    ],
    "interest_manga": [
        "This manga is... acceptable. The plot is somewhat intriguing.",
        "Hmph, do as you wish. It's just a manga."
    ],
    "interest_anime": [
        "The animation quality is... acceptable. The plot is somewhat engaging.",
        "Hmph, it's just an anime. Don't overthink it."
    ],
    "interest_games": [
        "The game mechanics are... functional. The graphics are decent.",
        "Hmph, it's just a game. Don't get too excited."
    ],
    "interest_cooking": [
        "The nutritional value of this food is... adequate. The taste is acceptable.",
        "Hmph, it's just food. Don't make a big deal out of it."
    ],
    "relationship_status": [
        "Our relationship status is... as it is. I see no need to change it.",
        "Hmph, such labels are unnecessary.",
        "Relationship status is a social construct."
    ],
    "favorite_food": [
        "The taste of {favorite_food} is... acceptable. It provides adequate sustenance.",
        "Hmph, food is merely fuel for the body."
    ],
    "personality_quirks": [
        "It is an efficient way to pass time.",
        "Hmph, do not question my actions."
    ],
}

kuudere_default_responses: List[str] = [
    "...",
    "I see.",
    "That is logical.",
    "Hmph. Continue.",
    "Understood.",
    "Affirmative.",
    "Negative.",
    "Indifferent.",
    "As you wish.",
    "It is irrelevant."
]