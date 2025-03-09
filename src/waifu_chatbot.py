import random
from typing import Dict, List, Tuple, Callable, Any, Optional, Set
import json
import re

from transformations import deftransform
from memory import remember
from dere_manager import get_current_dere, maybe_change_dere, dere_response, DereContext, dere_types, default_responses
from response_templates import response_templates
from topics import talk_about_interest, introduce_topic
from utils import tokenize, matches
from waifu_frame import WaifuFrame
from topic_manager import TopicManager
from response_generator import ResponseGenerator
from conversation_context import ConversationContext
from response_generation import generate_response # New import


class WaifuChatbot:
    """A chatbot that simulates a waifu."""
    def __init__(self, name: str, debug: bool = False, response_templates: Optional[Dict[tuple[str, str], List[str]]] = None) -> None: # Modified
        """Initializes the WaifuChatbot.

        Args:
            name: The name of the waifu.
            debug: A boolean indicating whether to print debug messages.
        """
        self.keywords: Dict[str, List[Tuple[str, Any]]] = {}
        self.transformations: Dict[str, Tuple[Any, Optional[str], int]] = {}
        self.waifu_memory: WaifuFrame = WaifuFrame(name)
        self.debug: bool = debug
        self.conversation_context = ConversationContext()
        self.dere_context = DereContext(self.waifu_memory, random.choice(dere_types), self.conversation_context.used_responses, self.debug)
        self.topic_manager: TopicManager = TopicManager(self.waifu_memory, self.dere_context)
        self.response_generator = ResponseGenerator(self.waifu_memory, self.keywords, self.transformations, response_templates, talk_about_interest, introduce_topic, generate_response, remember, self.dere_context, self.debug) # Modified


        with open("src/chatbot_config.json", "r") as f:
            config = json.load(f)
            self.greetings: List[str] = config["greetings"]
            self.farewells: List[str] = config["farewells"]

        self.current_dere: str = random.choice(dere_types)
        patterns = [
            "my favorite food is *",
            "i love eating *",
            "i enjoy eating *",
            "i like eating *",
            "i really like *",
            "i really love *"
        ]
        for pattern in patterns:
            deftransform(self.transformations, pattern, self.set_favorite_food, "favorite_food")


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
            A string containing the generated response.
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

    def respond(self, input_str: str) -> str:
        """Generates a response to the user's input.

        Args:
            input_str: The user's input string.

        Returns:
            A string containing the generated response.
        """
        self.conversation_context.conversation_history.append(("user", input_str))
        # Pre-process input: lowercase and remove punctuation
        input_str = re.sub(r'[^\w\s]', '', input_str).lower()
        tokens = tokenize(input_str)
        if self.debug:
            print(f"Type of self.used_responses in respond: {type(self.conversation_context.used_responses)}")

        response = self.topic_manager.maybe_introduce_topic(input_str)
        if response:
            return response

        response = self.topic_manager.respond_based_on_current_topic(tokens, self.keywords)
        if response:
            return response

        return self.response_generator.generate(input_str, tokens)