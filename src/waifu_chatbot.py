import random
from typing import Dict, List, Tuple, Callable, Any, Optional, Set

from response_generation import generate_response
from transformations import deftransform, apply_transformations
from memory import remember
from dere_types import get_current_dere, maybe_change_dere, dere_response
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
        self.greetings: List[str] = [
            "Senpai, you're back! How was your day?",
            "Welcome home, Onii-chan! What did you do today?",
            "Ara ara, you seem troubled. Tell me everything.",
            "I'm here for you, okay? Let's talk."
        ]
        self.farewells: List[str] = [
            "See you later, Senpai! Stay safe!",
            "Bye-bye, Onii-chan! Don't forget about me!",
            "Oyasumi nasai. Sweet dreams!",
            "Come back soon, okay?"
        ]
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
        keyword_list = self.keywords[word]
        for syn in synonyms:
            if syn not in self.keywords:
                self.keywords[syn] = keyword_list

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

    def respond(self, input_str: str) -> str:
        """Generates a response to the user's input.

        Args:
            input_str: The user's input string.

        Returns:
            A string containing the generated response.
        """
        self.waifu_memory.conversation_history.append(("user", input_str))
        tokens = tokenize(input_str)
        if self.debug:
            print(f"Type of self.used_responses in respond: {type(self.used_responses)}")

        # Check for topic-specific responses first
        if self.current_topic and self.current_topic in self.keywords:
            print(f"Current topic: {self.current_topic}")
            for resp_pattern, resp_text in self.keywords[self.current_topic]:
                print(f"Checking pattern: {resp_pattern}, response: {resp_text}")
                if matches(tokenize(resp_pattern), tokens):
                    self.used_responses.add(resp_text)
                    self.current_topic = None
                    return resp_text

        # Then check for transformations
        transformed = apply_transformations(self.transformations, tokens, self.waifu_memory, self.current_dere, talk_about_interest, introduce_topic, dere_response, maybe_change_dere, generate_response, remember, self.response_templates, self.used_responses, self.dere_types, self.debug)
        if transformed:
            return transformed

        # Then check for general keywords
        for word in tokens:
            if word in self.keywords:
                print(f"Found keyword: {word}")
                responses = self.keywords[word]
                for resp_pattern, resp_text in responses:
                    if matches(tokenize(resp_pattern), tokens):
                        self.used_responses.add(resp_text)
                        self.current_topic = None  # Reset the topic if a keyword is matched
                        return resp_text

        # Introduce a new topic based on affection level and randomness
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

            # Filter out last topic if exists
            if self.last_topic in available_topics:
                available_topics.remove(self.last_topic)

            if available_topics:
                new_topic = random.choice(available_topics)
                self.current_topic = new_topic
                self.last_topic = new_topic
                response = introduce_topic(new_topic, self.waifu_memory,
                                         self.current_dere, self.used_responses,
                                         self.debug)
                return response

        # Respond based on the current topic, if any
        if self.current_topic:
            # Check if current_topic is favorite_food and replace with actual value
            topic_value = self.waifu_memory.favorite_food if self.current_topic == "favorite_food" else self.current_topic
            response = dere_response(self.waifu_memory, self.current_dere, self.used_responses, self.debug,
                f"We were talking about {topic_value}, remember?",
                f"Let's get back to {topic_value}.",
                f"A-are you trying to avoid talking about {topic_value}...?",
                f"As I was saying about {topic_value}..."
            )
            return response

        response = maybe_change_dere(self.waifu_memory, self.current_dere, self.dere_types, self.used_responses, self.debug,
            "What are you talking about?", "I don't get it.", "Hmph.", "O-okay..."
        )
        return response