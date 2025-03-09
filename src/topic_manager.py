import random
from typing import List, Optional, Dict, Any, Tuple
from dere_manager import DereContext, dere_response
from utils import tokenize, matches
from topics import introduce_topic
from conversation_context import ConversationContext # New import
from response_generation import generate_response
import re


class TopicManager:
    def __init__(self, waifu_chatbot: Any):
        self.waifu_chatbot = waifu_chatbot
        self.waifu_memory = waifu_chatbot.waifu_memory
        self.dere_context = waifu_chatbot.dere_context
        self.current_topic: Optional[str] = None
        self.last_topic: Optional[str] = None
        self.last_topic_keyword: Optional[str] = None # Store the extracted topic keyword
        self.turns_since_last_topic: int = 0 # Counter for turns since last topic
        self.previous_input: str = "" # Store the previous input
        self.topic_dere: Optional[str] = None # Store the dere type when the topic was introduced
        self.topic_turns: int = 0 # Counter for turns since a topic-specific response


    def maybe_introduce_topic(self, input_str: str, turn_count: int) -> Optional[str]:
        """Introduces a new topic based on affection level, randomness, and topic counts."""
        if self.waifu_chatbot.debug:
            print(f"TopicManager.maybe_introduce_topic: Entering with input: {input_str}, turn: {turn_count}")
        if (self.waifu_memory.affection > 30 and # Lowered affection threshold
                random.random() < 0.3 and # Decreased probability
                (self.last_topic_keyword is None or self.last_topic_keyword not in input_str) and
                self.turns_since_last_topic >= 5 and # Increased turns_since_last_topic
                self.topic_turns == 0): # Only introduce a new topic if topic_turns is 0

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
                response = introduce_topic(new_topic, self.waifu_memory, self.dere_context.current_dere, list(self.dere_context.used_responses), self.waifu_chatbot.debug)
                self.current_topic = new_topic
                self.topic_dere = self.dere_context.current_dere # Store the current dere type

                # Increment the topic count
                self.waifu_memory.topic_counts[new_topic] += 1
                if self.waifu_chatbot.debug:
                    print(f"TopicManager.maybe_introduce_topic: Introduced topic: {new_topic}")
                # Extract and store the topic keyword

                self.last_topic_keyword = new_topic # Store topic directly
                if self.waifu_chatbot.debug:
                    print(f"TopicManager.maybe_introduce_topic: Stored topic keyword: {self.last_topic_keyword}")
                self.turns_since_last_topic = 0 # Reset the counter
                self.topic_turns = 2 # Set topic_turns to 2
                return response
        self.turns_since_last_topic += 1 # Increment the counter
        self.last_topic = None  # Reset last_topic if no new topic is introduced
        self.last_topic_keyword = None # Reset the keyword as well
        #self.topic_dere = None # Removed: Only reset when a NEW topic is introduced
        return None

    def respond_based_on_current_topic(self, tokens: List[str], keywords: Dict[str, List[Tuple[str, Any]]]) -> Optional[str]:
        """Responds based on the current topic, if any."""
        if self.waifu_chatbot.debug:
            print(f"TopicManager.respond_based_on_current_topic: Entering with tokens: {tokens}")
        if self.current_topic:
            if self.waifu_chatbot.debug:
                print(f"TopicManager.respond_based_on_current_topic: Current topic: {self.current_topic}, topic_turns: {self.topic_turns}")
            if self.topic_turns > 0: # Only respond if topic_turns > 0
                if self.current_topic in keywords:
                    for resp_pattern, resp_text in keywords[self.current_topic]:
                        if matches(tokenize(resp_pattern), tokens):
                            self.dere_context.used_responses.add(resp_text)
                            self.current_topic = None  # Reset topic after a match
                            self.topic_dere = None # Reset the dere type
                            self.topic_turns = 0 # Reset topic turns
                            if self.waifu_chatbot.debug:
                                print(f"TopicManager.respond_based_on_current_topic: Found response: {resp_text}")
                            return resp_text

                # If we have a current_topic, but no specific keyword was found:
                # Call generate_response with the current topic
                if self.waifu_chatbot.debug:
                    print(f"TopicManager.respond_based_on_current_topic: No keywords matched, calling generate_response with topic: {self.current_topic}")
                substitutions = {}
                if self.current_topic == "favorite_food":
                    substitutions = {"favorite_food": self.waifu_memory.favorite_food}
                response = generate_response(
                    self.waifu_chatbot.response_generator.response_templates, # Pass response_templates
                    self.current_topic,  # Use current_topic as keyword
                    substitutions,  # Pass substitutions
                    self.dere_context.used_responses,
                    self.waifu_memory,
                    self.topic_dere, # Use the stored dere type
                    dere_response,
                    self.waifu_chatbot.debug,
                    self.previous_input # Pass previous input
                )
                if response: # If a topic-specific response was generated
                    self.topic_turns = 0 # Reset topic turns
                    self.current_topic = None # Reset the topic
                    self.topic_dere = None # Reset dere type
                    self.turns_since_last_topic = 0 # Reset the counter
                    self.waifu_chatbot.response_generator.topic_context = False # Reset topic_context
                    if self.waifu_chatbot.debug:
                        print(f"TopicManager.respond_based_on_current_topic: topic_turns set to {self.topic_turns}")
                else:
                    self.topic_turns -= 1
                    if self.waifu_chatbot.debug:
                        print(f"TopicManager.respond_based_on_current_topic: topic_turns remains {self.topic_turns}")
                return response
            else:
                if self.waifu_chatbot.debug:
                    print(f"TopicManager.respond_based_on_current_topic: No more topic turns remaining")
                self.current_topic = None # Reset if no current topic
                self.topic_dere = None
        return None