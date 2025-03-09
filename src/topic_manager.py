import random
from typing import List, Optional, Dict, Any, Tuple
from dere_manager import DereContext, dere_response
from utils import tokenize, matches
from topics import introduce_topic
from conversation_context import ConversationContext # New import


class TopicManager:
    def __init__(self, waifu_memory: Any, dere_context: DereContext):
        self.waifu_memory = waifu_memory
        self.dere_context = dere_context
        self.current_topic: Optional[str] = None
        self.last_topic: Optional[str] = None


    def maybe_introduce_topic(self, input_str: str) -> Optional[str]:
        """Introduces a new topic based on affection level, randomness, and topic counts."""
        if (self.waifu_memory.affection > 40 and
                random.random() < 0.2 and
                input_str != self.last_topic):

            available_topics = [
                "family",
                "childhood",
                "feelings",
                "interests",
                "relationship_status",
                "favorite_food",
                "personality_quirks",
            ]

            # Initialize topic counts if not already present
            for topic in available_topics:
                if topic not in self.waifu_memory.topic_counts:
                    self.waifu_memory.topic_counts[topic] = 0

            # Filter out last topic if exists
            if self.last_topic in available_topics:
                available_topics.remove(self.last_topic)

            if available_topics:
                # Create a list of (topic, count) tuples and sort by count
                topic_counts = [(topic, self.waifu_memory.topic_counts[topic]) for topic in available_topics]
                topic_counts.sort(key=lambda x: x[1])  # Sort by count (ascending)

                # Get the topics with the lowest count
                min_count = topic_counts[0][1]
                min_count_topics = [topic for topic, count in topic_counts if count == min_count]

                # Choose a random topic from the topics with the lowest count
                new_topic = random.choice(min_count_topics)

                self.last_topic = new_topic
                response = introduce_topic(new_topic, self.waifu_memory, self.dere_context.current_dere, list(self.dere_context.used_responses), self.dere_context.debug)
                self.current_topic = new_topic

                # Increment the topic count
                self.waifu_memory.topic_counts[new_topic] += 1
                return response
        return None

    def respond_based_on_current_topic(self, tokens: List[str], keywords: Dict[str, List[Tuple[str, Any]]]) -> Optional[str]:
        """Responds based on the current topic, if any."""

        if self.current_topic:
            if self.current_topic in keywords:
                for resp_pattern, resp_text in keywords[self.current_topic]:
                    if matches(tokenize(resp_pattern), tokens):
                        self.dere_context.used_responses.add(resp_text)
                        self.current_topic = None  # Reset topic after a match
                        return resp_text

            # If we have a current_topic, but no specific response was found:
            if self.current_topic == "favorite_food":
                response = dere_response(self.dere_context,
                    f"We were talking about your favorite food, {self.waifu_memory.favorite_food}, remember?",
                    f"Let's get back to your favorite food, {self.waifu_memory.favorite_food}.",
                    f"A-are you trying to avoid talking about your favorite_food, {self.waifu_memory.favorite_food}...?",
                    f"As I was saying about your favorite food, {self.waifu_memory.favorite_food}..."
                )
            else:
                response = dere_response(self.dere_context,
                    f"We were talking about {self.current_topic}, remember?",
                    f"Let's get back to {self.current_topic}.",
                    f"A-are you trying to avoid talking about {self.current_topic}...?",
                    f"As I was saying about {self.current_topic}..."
                )
            self.current_topic = None  # Reset topic even if no match is found
            return response
        return None