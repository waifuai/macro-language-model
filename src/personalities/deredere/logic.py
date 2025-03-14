from typing import List, Dict, Any, Optional
from personalities.personality_interface import PersonalityInterface
from .defaults import get_default_response
from topic_manager import TopicManager
from topics import talk_about_interest
from memory import remember
from dere_data.deredere import deredere_default_responses
import random

class DeredereLogic(PersonalityInterface):
    def __init__(self, debug: bool):
        self.debug = debug
        self.topic_manager = None
        self.waifu_chatbot = None

    def generate_response(self, input_tokens: List[str], context: Dict[str, Any]) -> str:
        if self.waifu_chatbot is None:
            self.waifu_chatbot = context["waifu_chatbot"]
            self.topic_manager = TopicManager(self.waifu_chatbot)

        # Introduce a new topic sometimes
        maybe_topic_response = self.maybe_introduce_topic(" ".join(input_tokens), context["waifu_chatbot"].turn_count)
        if maybe_topic_response:
            return maybe_topic_response

        # Prioritize topic response if a topic is active
        if self.topic_manager.get_current_topic():
            topic_response = self.topic_manager.generate_topic_response(self.topic_manager.get_current_topic(), input_tokens)
            self.topic_manager.decrement_topic_turns()
            if topic_response:
                return topic_response

        # Probabilistic response selection (if no active topic)
        choice = random.random()

        if choice < 0.1:  # 10% chance to talk about interest
            return talk_about_interest(context["waifu_memory"], context["current_dere"], [], self.debug)
        elif choice < 0.4:  # 30% chance for a default response
            return random.choice(deredere_default_responses)
        else:  # 60% chance for input-specific responses
            input_str = " ".join(input_tokens)
            if "sad" in input_str:
                return "Aww, I'm sorry to hear you're feeling sad.  Is there anything I can do?"
            elif "happy" in input_str:
                return "Yay! I'm so glad you're happy!  What's making you so cheerful?"
            elif "angry" in input_str:
                return "Whoa, you seem angry!  What happened?"
            elif "hi" in input_tokens or "hello" in input_tokens:
                return "Hiya! It’s so great to see you again!"
            elif "bye" in input_tokens:
                return random.choice(self.waifu_chatbot.farewells)
            elif "family" in input_str:
                return "Family is super important! Tell me more about yours!"
            elif "games" in input_str or "game" in input_str:
                return "Games are so fun! What do you play?"
            elif "food" in input_str:
                return "Ooh, food! What's your favorite?"
            elif "work" in input_str:
                return "Work can be tough sometimes! Do you want to talk about it?"
            else:
                return "Tell me more!"  # Generic response if no keywords matched


    def introduce_topic(self, topic: str, context: Dict[str, Any]) -> Optional[str]:
        if topic == "family":
            return "Hey, let’s chat about family! What are they like?"
        elif topic == "food":
            return "Hey, let's talk about food! What's your favorite thing to eat?"
        elif topic == "games":
            return "Hey, let's talk about games! What do you like to play?"
        return None

    def maybe_introduce_topic(self, input_str: str, turn_count: int) -> Optional[str]:
        if random.random() < 0.2 and turn_count % 3 == 0:  # Every 3 turns, 20% chance
            topics = ["family", "food", "games"]
            return self.topic_manager.maybe_introduce_topic(input_str, turn_count, random.choice(topics))
        return None

    def get_default_response(self, context: Dict[str, Any]) -> str:
        return get_default_response(context)

    def get_data(self) -> Dict[str, Any]:
        return {}

    def talk_about_interest(self, waifu_memory: Any, current_dere: str, used_responses: List[str], debug: bool) -> str:
        return talk_about_interest(waifu_memory, current_dere, used_responses, debug)

    def remember(self, waifu_memory: Any, slot: str, value: str, affection_change: int = 0) -> None:
        return remember(waifu_memory, slot, value, affection_change)
