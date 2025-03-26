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
        input_str = " ".join(input_tokens) # Join tokens for easier checks

        if choice < 0.1:  # 10% chance to talk about interest
            return talk_about_interest(context["waifu_memory"], context["current_dere"], [], self.debug)
        # Removed explicit keyword matching block
        # Rely on probabilistic choice or default response
        elif choice < 0.2: # Reduce chance of using the most basic defaults (now 10%)
            response = random.choice(deredere_default_responses)
        else: # Use the expanded, more enthusiastic fallbacks (80% chance)
            fallback_responses = [
                "Wow, really?! Tell me more!",
                "That sounds super interesting!",
                "No way! Go on, I'm listening!",
                "Ooh, exciting! What happened next?",
                "Sounds like fun!",
                "Keep going!",
                "That's amazing!",
                "I wanna hear all about it!",
                "Seriously? That's wild!",
                "Cool!",
                "Awesome!",
            ]
            # Simple reaction based on punctuation
            if input_str.endswith('!'):
                response = random.choice([r for r in fallback_responses if '!' in r]) # Prefer exclamatory responses
            elif input_str.endswith('?'):
                 response = random.choice(["Good question!", "Hmm, let me think...", "What do *you* think?"])
            else:
                response = random.choice(fallback_responses)

        # Add a simple follow-up question sometimes to make it more engaging
        if random.random() < 0.4: # Increased chance slightly to 40%
            # More varied follow-ups, less dependent on specific words
            follow_ups = [
                "What do you think about that?",
                "How did that make you feel?",
                "Anything else happen?",
                "What happened after that?",
                "Is there more to the story?",
                "What are you thinking now?",
                "What's on your mind?",
                "Tell me everything!",
                "And then what?",
            ]
            # Avoid adding a question if the response already ends with one
            if not response.endswith('?'):
                 response += f" {random.choice(follow_ups)}"

        return response


    def introduce_topic(self, topic: str, context: Dict[str, Any]) -> Optional[str]:
        # Ensure standard apostrophe is used
        if topic == "family":
            return "Hey, let's chat about family! What are they like?" # Standard apostrophe
        elif topic == "food":
            return "Hey, let's talk about food! What's your favorite thing to eat?" # Standard apostrophe
        elif topic == "games":
            return "Hey, let's talk about games! What do you like to play?" # Standard apostrophe
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
