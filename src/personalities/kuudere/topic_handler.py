from typing import Optional, Dict, Any
from topic_manager import TopicManager

def introduce_topic(self, topic: str, context: Dict[str, Any]) -> Optional[str]:
    introductions = {
        "family": "Family is a social construct. Tell me about yours.",
        "childhood": "Childhood experiences shape individuals. Describe yours.",
        "feelings": "Emotions are fleeting. Explain your current state.",
        "interest_manga": "Manga is a form of escapism. Do you partake?",
        "interest_anime": "Anime is a visual medium. Do you find it engaging?",
        "interest_games": "Games provide interactive entertainment. Your preference?",
        "interest_cooking": "Cooking is a practical skill. Do you possess it?",
        "relationship_status": "Relationships are complex. What is your status?",
        "favorite_food": "Sustenance is necessary. What is your preferred source?",
        "personality_quirks": "Quirks are deviations from the norm. List yours."
    }
    return introductions.get(topic)

def maybe_introduce_topic(self, topic_manager: TopicManager, input_str: str, turn_count: int) -> Optional[str]:
    return topic_manager.maybe_introduce_topic(input_str, turn_count)