from typing import List, Optional, Dict, Any, Tuple

class TopicManager:
    def __init__(self, waifu_chatbot: Any):
        self.waifu_chatbot = waifu_chatbot
        self.waifu_memory = waifu_chatbot.waifu_memory
        self.current_topic: Optional[str] = None
        self.topic_turns: int = 0

    def maybe_introduce_topic(self, input_str: str, turn_count: int, topic: str = None) -> Optional[str]:
        """Introduces a new topic."""
        if topic:
          self.current_topic = topic
          self.topic_turns = 3  # Set initial topic turns
          return self.waifu_chatbot.personality.introduce_topic(topic, {"waifu_chatbot": self.waifu_chatbot})
        return None

    def get_current_topic(self):
        return self.current_topic

    def decrement_topic_turns(self):
        """Decrements the topic turns counter and clears the topic if it reaches 0."""
        if self.topic_turns > 0:
            self.topic_turns -= 1
            if self.topic_turns == 0:
                self.current_topic = None

    def generate_topic_response(self, topic: str, input_tokens: List[str]) -> str:
        """Generates a response based on the current topic and user input."""

        if topic == "family":
            if any(keyword in input_tokens for keyword in ["mom", "mother", "dad", "father", "brother", "sister", "sibling"]):
                return "That's cool! Tell me more about your family!"
            else:
                return "Family is really important, don't you think?"
        elif topic == "food":
            if any(keyword in input_tokens for keyword in ["pocky", "chocolate", "sweets", "cake", "eat"]):
                return "Mmm, that sounds delicious! I love talking about food."
            else:
                return "Food is the best! What's your favorite thing to cook?"
        elif topic == "games":
            if any(keyword in input_tokens for keyword in ["play", "game", "video", "rpg", "rhythm"]):
                return "Awesome! What kind of games do you usually play?"
            else:
                return "Video games are so much fun! Do you have a favorite?"
        else:
            return "That's an interesting topic!" # Generic topic response