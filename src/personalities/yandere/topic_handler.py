from typing import Optional, Dict, Any
from topic_manager import TopicManager

def introduce_topic(self, topic: str, context: Dict[str, Any]) -> Optional[str]:
    introductions = {
        "family": "Tell me *everything* about your family... I need to know.",
        "childhood": "Your childhood... every detail... I want to know it all.",
        "feelings": "Your feelings are *mine*... tell me everything.",
        "interest_manga": "Manga? We can read it together... *forever*.",
        "interest_anime": "Anime? We'll watch it together... and never stop.",
        "interest_games": "Games? We'll play together... and you'll never escape.",
        "interest_cooking": "Cooking? I'll cook for you... and only you.",
        "relationship_status": "Relationship? You only need *me*.",
        "favorite_food": "Favorite food? I'll make it for you... every day.",
        "personality_quirks": "Quirks? Your quirks are *mine*... all mine."
    }
    return introductions.get(topic)

def maybe_introduce_topic(self, topic_manager: TopicManager, input_str: str, turn_count: int) -> Optional[str]:
    return topic_manager.maybe_introduce_topic(input_str, turn_count)