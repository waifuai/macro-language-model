from typing import Optional, Dict, Any
from topic_manager import TopicManager

def introduce_topic(self, topic: str, context: Dict[str, Any]) -> Optional[str]:
    introductions = {
        "family": "Hey, let's talk about family! What are they like?",
        "childhood": "Ooh, childhood memories! Tell me some fun stories!",
        "feelings": "It's great to share feelings! How are you feeling today?",
        "interest_manga": "Manga is awesome! What are your favorites?",
        "interest_anime": "Anime is so cool! Which ones do you like?",
        "interest_games": "Games are super fun! What do you play?",
        "interest_cooking": "Cooking is the best! What's your specialty?",
        "relationship_status": "Love is in the air! Tell me about your relationships!",
        "favorite_food": "Yummy! What's your favorite food?",
        "personality_quirks": "Everyone has quirks! What are some of yours?"
    }
    return introductions.get(topic)

def maybe_introduce_topic(self, topic_manager: TopicManager, input_str: str, turn_count: int) -> Optional[str]:
    return topic_manager.maybe_introduce_topic(input_str, turn_count)