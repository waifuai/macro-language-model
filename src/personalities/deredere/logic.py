from typing import List, Dict, Any, Optional
from personalities.personality_interface import PersonalityInterface
from .response_generator import generate_response
from .topic_handler import introduce_topic, maybe_introduce_topic
from .defaults import get_default_response
from topic_manager import TopicManager
from topic_response import respond_based_on_current_topic
from keyword_handler import handle_keywords
from topics import talk_about_interest
from memory import remember
from transformations import apply_transformations

class DeredereLogic(PersonalityInterface):
    def __init__(self, debug: bool):
        self.debug = debug
        self.topic_manager = None  # Initialize to None
        self.waifu_chatbot = None


    def generate_response(self, input_tokens: List[str], context: Dict[str, Any]) -> str:
        if self.waifu_chatbot is None:
            self.waifu_chatbot = context["waifu_chatbot"]
            self.topic_manager = TopicManager(self.waifu_chatbot)
        return generate_response(self, input_tokens, context)

    def introduce_topic(self, topic: str, context: Dict[str, Any]) -> Optional[str]:
        return introduce_topic(self, topic, context)

    def maybe_introduce_topic(self, input_str: str, turn_count: int) -> Optional[str]:
        return maybe_introduce_topic(self, self.topic_manager, input_str, turn_count)

    def get_default_response(self, context: Dict[str, Any]) -> str:
        return get_default_response(context)

    def get_data(self) -> Dict[str, Any]:
        return {}

    def respond_based_on_current_topic(self, topic_manager: Any, tokens: List[str], keywords: Dict[str, List[Any]], context: Dict[str, Any], response_templates: Dict[tuple[str, str], List[str]]) -> Optional[str]:
        return respond_based_on_current_topic(topic_manager, tokens, keywords, context["dere_context"], response_templates)

    def handle_keywords(self, tokens: List[str], keywords: Dict[str, List[Any]], debug: bool) -> Optional[str]:
        return handle_keywords(tokens, keywords, debug)

    def handle_transformations(self, transformations, tokens, waifu_memory, talk_about_interest_func, introduce_topic_func, debug):
        return apply_transformations(transformations, tokens, waifu_memory, self.waifu_chatbot.current_dere, self.talk_about_interest, self.introduce_topic, self.waifu_chatbot.response_generator.dere_response, self.waifu_chatbot.response_generator.response_templates, self.waifu_chatbot.conversation_context.used_responses, self.get_data().get("dere_types", []), debug, self.waifu_chatbot)

    def talk_about_interest(self, waifu_memory: Any, current_dere: str, used_responses: List[str], debug: bool) -> str:
        return talk_about_interest(waifu_memory, current_dere, used_responses, debug)

    def remember(self, waifu_memory: Any, slot: str, value: str, affection_change: int = 0) -> None:
        return remember(waifu_memory, slot, value, affection_change)
