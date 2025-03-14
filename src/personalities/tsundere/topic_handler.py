from typing import Optional, Dict, Any
from topic_manager import TopicManager

def introduce_topic(self, topic: str, context: Dict[str, Any]) -> Optional[str]:
    introductions = {
        "family": "It's not like I care, b-baka, but what's your family like?",
        "childhood": "I-I'm not interested in your childhood, but tell me anyway!",
        "feelings": "Hmph, feelings... Don't expect me to care, but tell me.",
        "interest_manga": "M-Manga? It's not like I read it all the time...",
        "interest_anime": "A-Anime? It's not like I watch it or anything!",
        "interest_games": "G-Games? I only play them because I have nothing else to do!",
        "interest_cooking": "C-Cooking? I'm not doing it for you, b-baka!",
        "relationship_status": "R-Relationship? It's none of your business!",
        "favorite_food": "F-Favorite food? It's not like I'll share it with you!",
        "personality_quirks": "Q-Quirks? I don't have any weird quirks, b-baka!"
    }
    return introductions.get(topic)

def maybe_introduce_topic(self, topic_manager: TopicManager, input_str: str, turn_count: int) -> Optional[str]:
    return topic_manager.maybe_introduce_topic(input_str, turn_count)