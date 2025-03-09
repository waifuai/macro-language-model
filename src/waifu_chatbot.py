import random
from typing import Dict, List, Tuple, Callable, Any, Optional, Set
import re

from transformations import deftransform
from memory import remember
from dere_manager import get_current_dere, maybe_change_dere, dere_response, DereContext
from dere_data import dere_types  # Corrected import
from topics import talk_about_interest, introduce_topic
from utils import tokenize, matches
from waifu_frame import WaifuFrame
from topic_manager import TopicManager
from response_generator import ResponseGenerator
from conversation_context import ConversationContext
from response_generation import generate_response
from chatbot_config import greetings, farewells


class WaifuChatbot:
    """A chatbot that simulates a waifu."""
    # Removed response_templates from __init__
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
        self.conversation_context = ConversationContext()
        self.last_topic_introduction: Optional[str] = None  # Store the last topic introduction
        self.turn_count: int = 0  # Add a turn counter
        self.previous_input: str = ""  # Add previous_input
        self.expecting_topic_input: bool = False  # Flag for topic input
        self.turns_in_same_dere: int = 0 # Add a turn counter for dere type

        self.greetings = greetings
        self.farewells = farewells

        self.current_dere: str = random.choice(dere_types)
        self.dere_context = DereContext(self.waifu_memory, self.current_dere, self.conversation_context.used_responses, self.debug)
        self.topic_manager: TopicManager = TopicManager(self)  # Pass self
        # Removed response_templates
        self.response_generator = ResponseGenerator(self, self.waifu_memory, self.keywords, self.transformations, talk_about_interest, introduce_topic, generate_response, remember, self.debug)

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
        if self.debug: # Debug print
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
        original_input = input_str # Store for later
        self.turn_count += 1 # Increment the turn count

        # Remove the last topic introduction phrase, if it exists
        if self.last_topic_introduction and self.last_topic_introduction in input_str:
            input_str = input_str.replace(self.last_topic_introduction, "").strip()


        if self.expecting_topic_input:
            self.expecting_topic_input = False  # Reset the flag
            if not input_str:
                return "..." # Or some other default response
        else:
            # Pre-process input: lowercase and remove punctuation
            input_str = re.sub(r'[^\w\s]', '', input_str).lower()

        tokens = tokenize(input_str)
        if self.debug:
            print(f"Type of self.used_responses in respond: {type(self.conversation_context.used_responses)}")
            print(f"WaifuChatbot.respond: Input: {input_str}")

        response = self.topic_manager.maybe_introduce_topic(input_str, self.turn_count) # Pass turn_count
        if response:
            if self.debug:
                print(f"WaifuChatbot.respond: Topic introduced: {response}")
            self.last_topic_introduction = response  # Store the topic introduction
            self.expecting_topic_input = True
            return response

        # Maybe change dere type
        maybe_change_dere(self.dere_context, dere_types, self) # Pass self

        if self.debug:
            print(f"WaifuChatbot.respond: Calling response generator")
        response = self.response_generator.generate(input_str, tokens)


        self.previous_input = original_input # Store the original input before processing

        # Add a small random affection change
        affection_change = random.randint(-1, 2)  # -1, 0, 1, or 2
        self.waifu_memory.affection += affection_change
        self.waifu_memory.affection = max(0, min(100, self.waifu_memory.affection)) # Keep within 0-100
        if self.debug:
            print(f"WaifuChatbot.respond: Affection changed by {affection_change}, new affection: {self.waifu_memory.affection}")



        return response