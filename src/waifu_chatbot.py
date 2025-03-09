import random
from typing import Dict, List, Tuple, Callable, Any, Optional, Set
import json
import re

from response_generation import generate_response
from transformations import deftransform, apply_transformations
from memory import remember
from dere_types import get_current_dere, maybe_change_dere, dere_response, DereContext
from response_templates import response_templates
from topics import talk_about_interest, introduce_topic
from utils import tokenize, matches
from waifu_frame import WaifuFrame

class WaifuChatbot:
    """A chatbot that simulates a waifu."""
    def __init__(self, name: str, debug: bool = False) -> None:
        """Initializes the WaifuChatbot.

        Args:
            name: The name of the waifu.
            debug: A boolean indicating whether to print debug messages.
        """
        self.keywords: Dict[str, List[Tuple[str, Any]]] = {}
        self.transformations: Dict[str, Tuple[Any, Optional[str], int]] = {}
        self.waifu_memory: WaifuFrame = WaifuFrame(name)
        self.debug: bool = debug

        with open("src/chatbot_config.json", "r") as f:
            config = json.load(f)
            self.greetings: List[str] = config["greetings"]
            self.farewells: List[str] = config["farewells"]

        self.small_talk: List[str] = [
            "The weather is nice today, isn't it?",
            "Have you heard any good news lately?",
            "Did you see that viral video about the cat playing the piano?",
            "I wonder what the next big trend will be..."
        ]
        self.current_topic: Optional[str] = None
        self.dere_types: List[str] = ["tsundere", "yandere", "kuudere", "dandere", "himedere"]
        self.current_dere: str = random.choice(self.dere_types)
        self.response_templates: Dict[tuple[str, str], List[str]] = response_templates
        self.used_responses: Set[str] = set()  # Initialize used_responses
        self.last_topic: Optional[str] = None
        deftransform(self.transformations, "my favorite food is *", self.set_favorite_food, "favorite_food")
        deftransform(self.transformations, "i love eating *", self.set_favorite_food, "favorite_food")
        deftransform(self.transformations, "i enjoy eating *", self.set_favorite_food, "favorite_food")
        deftransform(self.transformations, "i like eating *", self.set_favorite_food, "favorite_food")
        deftransform(self.transformations, "i really like *", self.set_favorite_food, "favorite_food")
        deftransform(self.transformations, "i really love *", self.set_favorite_food, "favorite_food")

        self.default_responses: Dict[str, List[str]] = {
            "tsundere": [
                "Hmph, what do *you* want?",
                "It's not like I care what you say, b-baka!",
                "Whatever.",
                "Don't get the wrong idea!",
                "I'm not doing this for *you* or anything."
            ],
            "yandere": [
                "Oh, you're back! I was waiting for you.",
                "Where have you been? I was so worried...",
                "You're the only one I care about.",
                "Don't leave me again, okay?",
                "We'll be together forever, right?"
            ],
            "kuudere": [
                "...",
                "I see.",
                "That is logical.",
                "Hmph.",
                "Understood."
            ],
            "dandere": [
                "U-um...",
                "I-I'm sorry...",
                "P-please don't be mad...",
                "O-okay...",
                "I-I'll try my best...",
                "D-do you need something?",
                "I-is everything alright?",
                "M-maybe we could...",
            ],
            "himedere": [
                "Fufufu, you're finally back.",
                "Kneel before me!",
                "You should be honored to be in my presence.",
                "Of course, I'm always right.",
                "Remember your place."
            ]
        }


    def defkeyword(self, keyword: str, responses: List[str]) -> None:
        """Defines a keyword and its associated responses.

        Args:
            keyword: The keyword to define.
            responses: A list of responses associated with the keyword.
        """
        if responses and isinstance(responses[0], tuple):
            self.keywords[keyword] = responses
        else:
            self.keywords[keyword] = [(keyword, response) for response in responses]

    def set_favorite_food(self, food: str) -> str:
        """Updates the waifu's favorite food.

        Args:
            food: The waifu's favorite food.

        Returns:
            A string containing the response.
        """
        self.waifu_memory.set_favorite_food(food)
        response = f"Okay, I'll remember that your favorite food is {food}!"
        print(f"{self.waifu_memory.name}: {response}")
        print()
        return response

    def defsynonym(self, word: str, *synonyms: str) -> None:
        """Defines synonyms for a given word.

        Args:
            word: The word to define synonyms for.
            *synonyms: Variable number of synonyms for the word.
        """
        if word not in self.keywords:
            return

        for syn in synonyms:
            self.keywords[syn] = self.keywords[word][:]  # Create a copy of list.

    def def_topic_response(self, topic: str, pattern: str, response: str) -> None:
        """Defines a response for a specific topic.

        Args:
            topic: The topic to define the response for.
            pattern: The pattern to match against the input.
            response: The response to return if the pattern matches.
        """
        if topic not in self.keywords:
            self.keywords[topic] = []
        self.keywords[topic].append((pattern, response))

    def _handle_topic_specific_response(self, tokens: List[str]) -> Optional[str]:
        """Handles topic-specific responses."""
        return None

    def _handle_transformations(self, tokens: List[str]) -> Optional[str]:
        """Handles transformations."""
        transformed = apply_transformations(self.transformations, tokens, self.waifu_memory, self.current_dere, talk_about_interest, introduce_topic, dere_response, maybe_change_dere, generate_response, remember, self.response_templates, self.used_responses, self.dere_types, self.debug)
        return transformed

    def _handle_keywords(self, tokens: List[str]) -> Optional[str]:
        """Handles general keywords."""
        for word in tokens:
            if word in self.keywords:
                responses = self.keywords[word]
                for resp_pattern, resp_text in responses:
                    if matches(tokenize(resp_pattern), tokens):
                        self.used_responses.add(resp_text)
                        return resp_text
        return None

    def _maybe_introduce_topic(self, input_str: str) -> Optional[str]:
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
                dere_context = DereContext(self.waifu_memory, self.current_dere, self.used_responses, self.debug)
                response = introduce_topic(new_topic, self.waifu_memory,
                                         self.current_dere, self.used_responses,
                                         self.debug)
                self.current_topic = new_topic

                # Increment the topic count
                self.waifu_memory.topic_counts[new_topic] += 1
                return response
        return None

    def _respond_based_on_current_topic(self, tokens: List[str]) -> Optional[str]:
        """Responds based on the current topic, if any."""
        if self.current_topic:
            if self.current_topic in self.keywords:
                for resp_pattern, resp_text in self.keywords[self.current_topic]:
                    if matches(tokenize(resp_pattern), tokens):
                        self.used_responses.add(resp_text)
                        self.current_topic = None  # Reset topic after a match
                        return resp_text

            # If we have a current_topic, but no specific response was found:
            dere_context = DereContext(self.waifu_memory, self.current_dere, self.used_responses, self.debug)
            if self.current_topic == "favorite_food":
                response = dere_response(dere_context,
                    f"We were talking about your favorite food, {self.waifu_memory.favorite_food}, remember?",
                    f"Let's get back to your favorite food, {self.waifu_memory.favorite_food}.",
                    f"A-are you trying to avoid talking about your favorite_food, {self.waifu_memory.favorite_food}...?",
                    f"As I was saying about your favorite food, {self.waifu_memory.favorite_food}..."
                )
            else:
                response = dere_response(dere_context,
                    f"We were talking about {self.current_topic}, remember?",
                    f"Let's get back to {self.current_topic}.",
                    f"A-are you trying to avoid talking about {self.current_topic}...?",
                    f"As I was saying about {self.current_topic}..."
                )
            self.current_topic = None  # Reset topic even if no match is found
            return response

        return None

    def _get_default_response(self) -> str:
        """Gets the default response."""
        dere_context = DereContext(self.waifu_memory, self.current_dere, self.used_responses, self.debug)
        current_dere = get_current_dere(self.waifu_memory.affection)  # Get the current dere type
        if current_dere in self.default_responses:
            return random.choice(self.default_responses[current_dere])
        else:
            # Fallback if dere type somehow not in defaults
            return maybe_change_dere(dere_context, self.dere_types,
                "What are you talking about?", "I don't get it.", "Hmph.", "O-okay..."
            )
    def _maybe_use_small_talk(self) -> Optional[str]:
        """Uses small talk based on randomness"""
        if (random.random() < 0.1):
            return random.choice(self.small_talk)
        return None

    def respond(self, input_str: str) -> str:
        """Generates a response to the user's input.

        Args:
            input_str: The user's input string.

        Returns:
            A string containing the generated response.
        """
        self.waifu_memory.conversation_history.append(("user", input_str))
        # Pre-process input: lowercase and remove punctuation
        input_str = re.sub(r'[^\w\s]', '', input_str).lower()
        tokens = tokenize(input_str)
        if self.debug:
            print(f"Type of self.used_responses in respond: {type(self.used_responses)}")

        # Introduce a new topic based on affection level, randomness, and topic counts
        response = self._maybe_introduce_topic(input_str)
        if response:
            return response

        # Check for topic-specific responses first and respond based on the current topic, if any
        response = self._respond_based_on_current_topic(tokens)
        if response:
            return response
        # Then check for transformations
        response = self._handle_transformations(tokens)
        if response:
            return response
        # Then check for general keywords
        response = self._handle_keywords(tokens)
        if response:
            return response
        # Use small talk
        response = self._maybe_use_small_talk()
        if response:
            return response

        # Get the default response
        return self._get_default_response()