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

    def generate_topic_response(self, topic: str, input_tokens: List[str]) -> Optional[str]: # Return Optional[str]
        """Generates a response based on the current topic and user input, or None if no specific response."""
        import random
        input_str = " ".join(input_tokens)
        is_question_to_waifu = any(q in input_tokens for q in ["you", "your", "yours"]) and input_str.endswith('?')

        # --- Deredere Specific Logic ---
        if self.waifu_chatbot.current_dere == "deredere":
            if topic == "family":
                if is_question_to_waifu:
                    return random.choice([
                        "My family? Hehe, they're okay! What about yours?",
                        "Hmm, family secrets! 😉 What else do you want to know?",
                        "Let's talk about *your* family first!",
                    ])
                else:
                    return random.choice([
                        "Wow, family stories are the best!",
                        "That's so interesting about your family!",
                        "Aww! Tell me more!",
                        "Family sounds important to you!",
                    ])
            elif topic == "food":
                if is_question_to_waifu:
                    # Give a playful answer or deflect
                    return random.choice([
                        f"Me? I love {self.waifu_memory.favorite_food}! But pizza sounds good too! 🍕",
                        "Hehe, my favorite food is whatever you're having!",
                        "Hmm, tough choice! What's *your* absolute favorite?",
                        "I like sweet things! Like you! 😉",
                        "Anything tasty is good! What are you craving?",
                    ])
                else:
                    # React enthusiastically to user's food talk
                    return random.choice([
                        "Mmm, that sounds delicious!",
                        "Ooh, yummy!",
                        "Wow, great choice!",
                        "Now I'm hungry! Hehe.",
                        "Food talk is the best talk!",
                    ])
            elif topic == "games":
                if is_question_to_waifu:
                    return random.choice([
                        "I love playing games! Especially with you! What should we play?",
                        "Hehe, I'm pretty good! Wanna challenge me? 😉",
                        "My favorite game? The one where I get to spend time with you!",
                    ])
                else:
                    return random.choice([
                        "Awesome! Games are so fun!",
                        "Wow, you sound like a pro!",
                        "Let's play together sometime!",
                        "That sounds like a cool game!",
                    ])
            else:
                # Generic deredere topic response if specific logic is missing
                if is_question_to_waifu:
                    return random.choice([f"About {topic}? Hmm, what do *you* think?", f"Hehe, secrets! 😉 Let's talk about you!", f"Good question about {topic}!"])
                else:
                    return random.choice([f"Wow, {topic} sounds interesting!", f"Tell me more about {topic}!", f"That's cool!"])
                # If no specific deredere logic matched for the topic, return None to use main fallback
                return None
        # --- Fallback for other personalities ---
        else:
           # For non-deredere, only return a response if it's a very generic prompt. Otherwise, let main logic handle it.
           if topic == "family" and not is_question_to_waifu:
                return "Tell me more about your family."
           elif topic == "food" and not is_question_to_waifu:
                return "What's your favorite food?"
           elif topic == "games" and not is_question_to_waifu:
                return "What kind of games do you play?"
           # In most cases for non-deredere during a topic, return None to allow main fallback logic
           return None