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
        import random # Add import for random

        if topic == "family":
            family_keywords = ["mom", "mother", "dad", "father", "brother", "sister", "sibling", "parents", "family"]
            if any(keyword in input_tokens for keyword in family_keywords) and len(input_tokens) > 5: # Check if user is likely elaborating
                responses = [
                    "Wow, your family sounds interesting!",
                    "That's nice you're sharing about them!",
                    "It sounds like you have a lovely family.",
                    "Keep going, I'm listening!",
                ]
                return random.choice(responses)
            elif any(keyword in input_tokens for keyword in family_keywords):
                 # User mentioned family but didn't elaborate much
                 return "Tell me more about your family!"
            else:
                # Ask a follow-up question if user didn't mention specifics
                return "Family is really important, don't you think? Do you have any siblings?"
        elif topic == "food":
            # Check for specific food items or cooking-related words
            food_keywords = ["pocky", "chocolate", "sweets", "cake", "eat", "steak", "pasta", "cook", "make", "recipe", "bake", "dish", "sauce"]
            if any(keyword in input_tokens for keyword in food_keywords):
                # User mentioned food or cooking
                responses = [
                    "Mmm, that sounds delicious!",
                    "Wow, homemade pasta sounds amazing!",
                    "That's really interesting! You sound like a great cook.",
                    "Ooh, tell me more about that recipe!",
                ]
                return random.choice(responses) # Give a varied positive response
            else:
                # User didn't mention food/cooking, ask a different food question
                responses = [
                    "What's a dish you'd love to try making someday?",
                    "Do you prefer sweet or savory snacks?",
                    "Is there any food you absolutely dislike?",
                    "I love talking about food!", # More generic fallback
                ]
                return random.choice(responses)
        elif topic == "games":
             # Basic check if user mentioned game types or actions
            game_keywords = ["play", "game", "video", "rpg", "rhythm", "fps", "moba", "strategy", "console", "pc"]
            if any(keyword in input_tokens for keyword in game_keywords):
                 return "Awesome! What kind of games do you usually play?"
            else:
                 # Ask a follow-up question
                 return "Video games are so much fun! Do you have a favorite console or platform?"
        else:
            # Generic response for unhandled topics
            return f"That's an interesting topic! Tell me more about {topic}."