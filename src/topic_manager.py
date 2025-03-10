import random
from typing import List, Optional, Dict, Any, Tuple
from dere_manager import DereContext, dere_response
from utils import tokenize, matches
from topics import introduce_topic
from conversation_context import ConversationContext
from response_generation import generate_response
import re
# Corrected imports:
from response_templates.tsundere import tsundere_responses
from response_templates.yandere import yandere_responses
from response_templates.kuudere import kuudere_responses
from response_templates.dandere import dandere_responses
from response_templates.himedere import himedere_responses

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
        self.max_topic_turns: int = 4 # Maximum turns to stay on a topic

        self.response_templates = {
            ("feeling", "tsundere"): tsundere_responses["feeling"],
            ("family", "tsundere"): tsundere_responses["family"],
            ("childhood", "tsundere"): tsundere_responses["childhood"],
            ("insult", "tsundere"): tsundere_responses["insult"],
            ("compliment", "tsundere"): tsundere_responses["compliment"],
            ("interest_manga", "tsundere"): tsundere_responses["interest_manga"],
            ("interest_anime", "tsundere"): tsundere_responses["interest_anime"],
            ("interest_games", "tsundere"): tsundere_responses["interest_games"],
            ("interest_cooking", "tsundere"): tsundere_responses["interest_cooking"],
            ("relationship_status", "tsundere"): tsundere_responses["relationship_status"],
            ("favorite_food", "tsundere"): tsundere_responses["favorite_food"],
            ("personality_quirks", "tsundere"): tsundere_responses["personality_quirks"],
            ("feeling", "yandere"): yandere_responses["feeling"],
            ("family", "yandere"): yandere_responses["family"],
            ("childhood", "yandere"): yandere_responses["childhood"],
            ("insult", "yandere"): yandere_responses["insult"],
            ("compliment", "yandere"): yandere_responses["compliment"],
            ("interest_manga", "yandere"): yandere_responses["interest_manga"],
            ("interest_anime", "yandere"): yandere_responses["interest_anime"],
            ("interest_games", "yandere"): yandere_responses["interest_games"],
            ("interest_cooking", "yandere"): yandere_responses["interest_cooking"],
            ("relationship_status", "yandere"): yandere_responses["relationship_status"],
            ("favorite_food", "yandere"): yandere_responses["favorite_food"],
            ("personality_quirks", "yandere"): yandere_responses["personality_quirks"],
            ("feeling", "kuudere"): kuudere_responses["feeling"],
            ("family", "kuudere"): kuudere_responses["family"],
            ("childhood", "kuudere"): kuudere_responses["childhood"],
            ("insult", "kuudere"): kuudere_responses["insult"],
            ("compliment", "kuudere"): kuudere_responses["compliment"],
            ("interest_manga", "kuudere"): kuudere_responses["interest_manga"],
            ("interest_anime", "kuudere"): kuudere_responses["interest_anime"],
            ("interest_games", "kuudere"): kuudere_responses["interest_games"],
            ("interest_cooking", "kuudere"): kuudere_responses["interest_cooking"],
            ("relationship_status", "kuudere"): kuudere_responses["relationship_status"],
            ("favorite_food", "kuudere"): kuudere_responses["favorite_food"],
            ("personality_quirks", "kuudere"): kuudere_responses["personality_quirks"],
            ("feeling", "dandere"): dandere_responses["feeling"],
            ("family", "dandere"): dandere_responses["family"],
            ("childhood", "dandere"): dandere_responses["childhood"],
            ("insult", "dandere"): dandere_responses["insult"],
            ("compliment", "dandere"): dandere_responses["compliment"],
            ("interest_manga", "dandere"): dandere_responses["interest_manga"],
            ("interest_anime", "dandere"): dandere_responses["interest_anime"],
            ("interest_games", "dandere"): dandere_responses["interest_games"],
            ("interest_cooking", "dandere"): dandere_responses["interest_cooking"],
            ("relationship_status", "dandere"): dandere_responses["relationship_status"],
            ("favorite_food", "dandere"): dandere_responses["favorite_food"],
            ("personality_quirks", "dandere"): dandere_responses["personality_quirks"],
            ("feeling", "himedere"): himedere_responses["feeling"],
            ("family", "himedere"): himedere_responses["family"],
            ("childhood", "himedere"): himedere_responses["childhood"],
            ("insult", "himedere"): himedere_responses["insult"],
            ("compliment", "himedere"): himedere_responses["compliment"],
            ("interest_manga", "himedere"): himedere_responses["interest_manga"],
            ("interest_anime", "himedere"): himedere_responses["interest_anime"],
            ("interest_games", "himedere"): himedere_responses["interest_games"],
            ("interest_cooking", "himedere"): himedere_responses["interest_cooking"],
            ("relationship_status", "himedere"): himedere_responses["relationship_status"],
            ("favorite_food", "himedere"): himedere_responses["favorite_food"],
            ("personality_quirks", "himedere"): himedere_responses["personality_quirks"],
        }


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

                # More natural and dere-specific topic introductions
                dere_introductions = {
                    "tsundere": {
                        "family": "It's not like I care, b-baka, but what's your family like?",
                        "childhood": "Hmph, I bet your childhood was boring. Tell me about it anyway.",
                        "feelings": "Don't get the wrong idea! I'm not asking because I care, but... what are you feeling?",
                        "interests": "Whatever. I guess we could talk about interests... if you insist.",
                        "relationship_status": "It's none of your business, but... what's your relationship status?",
                        "favorite_food": "B-baka! Tell me your favorite food... not that I'll make it for you!",
                        "personality_quirks": "Hmph. Do you have any weird quirks? Not like I care.",
                    },
                    "yandere": {
                        "family": "Tell me everything about your family. I need to know who might interfere with us.",
                        "childhood": "I want to know everything about your past. Every single detail.",
                        "feelings": "Tell me your deepest feelings. I'm the only one who understands you.",
                        "interests": "We should share all our interests. Tell me yours.",
                        "relationship_status": "We're meant to be together, so tell me about your relationship history.",
                        "favorite_food": "Your favorite food is my favorite food. Tell me what it is!",
                        "personality_quirks": "I love everything about you, even your quirks. Tell me.",
                    },
                    "kuudere": {
                        "family": "Family is a social construct. Tell me about yours.",
                        "childhood": "Childhood experiences shape individuals. Describe yours.",
                        "feelings": "Feelings are fleeting. What are you experiencing?",
                        "interests": "Interests are logical pursuits. What are yours?",
                        "relationship_status": "Relationship status is a label. What is yours?",
                        "favorite_food": "Sustenance is necessary. What is your preferred food?",
                        "personality_quirks": "Quirks are deviations from the norm. Describe yours.",
                    },
                    "dandere": {
                        "family": "U-um... could you tell me about your family...?",
                        "childhood": "I-I was wondering... what was your childhood like...?",
                        "feelings": "A-are you feeling okay...?  Maybe we could talk about feelings...",
                        "interests": "Um... do you have any interests...? I-I'd like to hear about them...",
                        "relationship_status": "I-I'm a little shy, but... um... what's your relationship status...?",
                        "favorite_food": "M-maybe we could share our favorite foods...?  If you want...",
                        "personality_quirks": "S-sorry if I'm awkward... Do you have any quirks...?",
                    },
                    "himedere": {
                        "family": "Your family should be honored to be in my presence. Tell me about them.",
                        "childhood": "I assume your childhood was unremarkable. Prove me wrong.",
                        "feelings": "As a princess, my feelings are paramount. But tell me yours, peasant.",
                        "interests": "You should be interested in what *I* am interested in. However, tell me yours.",
                        "relationship_status": "You should be grateful to even be considered. What's your relationship status?",
                        "favorite_food": "Only the finest foods for me. What do *you* eat, commoner?",
                        "personality_quirks": "My quirks are perfection. What are yours, I wonder?",
                    },
                }
                response = dere_introductions.get(self.dere_context.current_dere, {}).get(new_topic, f"Let's talk about {new_topic}.")
                if self.waifu_chatbot.debug:
                    print(f"TopicManager.maybe_introduce_topic: Using intro: {response}")

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
                self.topic_turns = 2 # Reduced topic_turns
                self.waifu_chatbot.response_generator.topic_context = True # Set topic_context
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

            # Check if user input relates to the current topic
            input_relates_to_topic = False
            for token in tokens:
                if token in self.current_topic or (self.current_topic in keywords and any(token in entry[0] for entry in keywords[self.current_topic])):
                    input_relates_to_topic = True
                    break

            if self.topic_turns > 0: # Only respond if topic_turns > 0
                if self.current_topic in keywords:
                    for resp_pattern, resp_text in keywords[self.current_topic]:
                        if matches(tokenize(resp_pattern), tokens):
                            self.dere_context.used_responses.add(resp_text)
                            #self.current_topic = None  # Reset topic after a match
                            #self.topic_dere = None # Reset the dere type
                            #self.topic_turns = 0 # Reset topic turns
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
                    self.response_templates, # Pass response_templates
                    self.current_topic,  # Use current_topic as keyword
                    substitutions,  # Pass substitutions
                    self.waifu_chatbot.dere_context.used_responses,
                    self.waifu_memory,
                    self.waifu_chatbot.dere_context.current_dere, # Use the current dere type
                    dere_response,
                    self.waifu_chatbot.debug,
                    self.waifu_chatbot.response_generator.used_default_responses, # Pass used_default_responses
                    self.previous_input # Pass previous input
                )
                if response: # If a topic-specific response was generated
                    if input_relates_to_topic:
                        self.topic_turns -= 1 # Decrement topic_turns
                    else:
                        self.topic_turns -= 2  # Decrement faster if user doesn't engage
                        if self.topic_turns < 0:
                            self.topic_turns = 0

                    if self.topic_turns == 0:
                        self.current_topic = None  # Reset the topic when turns run out
                        self.topic_dere = None
                    self.turns_since_last_topic = 0 # Reset the counter
                    self.waifu_chatbot.response_generator.topic_context = False # Reset topic_context
                    if self.waifu_chatbot.debug:
                        print(f"TopicManager.respond_based_on_current_topic: topic_turns set to {self.topic_turns}")

                return response
            else:
                if self.waifu_chatbot.debug:
                    print(f"TopicManager.respond_based_on_current_topic: No more topic turns remaining")
                self.current_topic = None # Reset if no current topic
                self.topic_dere = None
                self.turns_since_last_topic = 0 # Reset turns_since_last_topic

            if self.topic_turns <= 0 or not input_relates_to_topic:
                if self.waifu_chatbot.debug:
                    print("TopicManager.respond_based_on_current_topic: Exiting topic due to no engagement or turns limit")
                self.current_topic = None
                self.topic_dere = None
                self.turns_since_last_topic = 0

        return None