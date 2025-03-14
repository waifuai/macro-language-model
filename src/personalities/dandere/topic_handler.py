from typing import Optional, Dict, Any
from topic_manager import TopicManager

def introduce_topic(self, topic: str, context: Dict[str, Any]) -> Optional[str]:
    introductions = {
        "family": "U-um... could you tell me about your family...?",
        "childhood": "Y-Your childhood... was it... nice...?",
        "feelings": "I-It's okay to have feelings... um...",
        "interest_manga": "M-Manga...? Do you... like it...?",
        "interest_anime": "A-Anime...? Um... it's okay if you watch it...",
        "interest_games": "G-Games...? I-I don't play much...",
        "interest_cooking": "C-Cooking...? I-I'm not very good...",
        "relationship_status": "R-Relationship...? Um...",
        "favorite_food": "F-Favorite food...? I-I like...",
        "personality_quirks": "Q-Quirks...? I-I don't have any..."
    }
    return introductions.get(topic)

def maybe_introduce_topic(self, topic_manager: TopicManager, input_str: str, turn_count: int) -> Optional[str]:
    return topic_manager.maybe_introduce_topic(input_str, turn_count)