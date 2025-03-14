from typing import List, Dict, Any, Optional
from personalities.personality_interface import PersonalityInterface
from .response_generator import generate_response
from .topic_handler import introduce_topic, maybe_introduce_topic
from .defaults import get_default_response
from topic_manager import TopicManager

class DeredereLogic(PersonalityInterface):
    def __init__(self, debug: bool):
        self.debug = debug
        self.topic_manager = TopicManager()


    def generate_response(self, input_tokens: List[str], context: Dict[str, Any]) -> str:
        return generate_response(self, input_tokens, context)

    def introduce_topic(self, topic: str, context: Dict[str, Any]) -> Optional[str]:
        return introduce_topic(self, topic, context)

    def maybe_introduce_topic(self, input_str: str, turn_count: int) -> Optional[str]:
        return maybe_introduce_topic(self, self.topic_manager, input_str, turn_count)

    def get_default_response(self, context: Dict[str, Any]) -> str:
        return get_default_response(context)
