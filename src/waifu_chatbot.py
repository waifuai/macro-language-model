import random
from typing import Dict, List, Tuple, Callable, Any, Optional, Set
import re

from transformations import deftransform
from memory import remember
from dere_utils import get_dere_default_response, maybe_change_dere, dere_response  # Updated import
from dere_types import DereContext  # Updated import
from topics import talk_about_interest  # Keep this for now, used in response_generator
from utils import tokenize, matches
from waifu_frame import WaifuFrame
from topic_manager import TopicManager  # Corrected import
from response_generator import ResponseGenerator
from conversation_context import ConversationContext
from chatbot_config import greetings, farewells
from response_templates.deredere import deredere_responses
from core.registry import Registry
from waifu_actions import register_actions
from personalities.personality_interface import PersonalityInterface  # Import the interface
from dere_data import dere_types


class WaifuChatbot:
    """A chatbot that simulates a waifu."""
    def __init__(self, name: str, personality: str = "deredere", debug: bool = False) -> None:
        """Initializes the WaifuChatbot.

        Args:
            name: The name of the waifu.
            personality: The personality of the waifu.
            debug: A boolean indicating whether to print debug messages.
        """
        self.registry = Registry()
        self.keywords = self.registry.keywords  # Use the registry's keywords
        self.transformations = self.registry.transformations  # Use the registry's transformations
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

        # Modified personality loading
        self.personality: Optional[PersonalityInterface] = None  # Store the personality *instance*
        if personality == "tsundere":
            from personalities.tsundere.logic import TsundereLogic
            self.personality = TsundereLogic()
        elif personality == "yandere":
            from personalities.yandere.logic import YandereLogic
            self.personality = YandereLogic()
        elif personality == "kuudere":
            from personalities.kuudere.logic import KuudereLogic
            self.personality = KuudereLogic()
        elif personality == "dandere":
            from personalities.dandere.logic import DandereLogic
            self.personality = DandereLogic()
        elif personality == "himedere":
            from personalities.himedere.logic import HimedereLogic
            self.personality = HimedereLogic()
        elif personality == "deredere":
            from personalities.deredere.logic import DeredereLogic
            self.personality = DeredereLogic(self.debug)
        else:
            raise ValueError(f"Invalid personality: {personality}")

        self.current_dere = personality
        self.dere_context = DereContext(self.waifu_memory, self.current_dere, set(), self.debug)
        self.topic_manager: TopicManager = TopicManager(self)  # Pass self
        self.response_generator = ResponseGenerator(self, self.waifu_memory, self.keywords, self.transformations, talk_about_interest, self.topic_manager.maybe_introduce_topic, remember, self.debug)

        register_actions(self) # Register actions from waifu_actions.py


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

        # Dynamic dere type switching logic
        maybe_change_dere_response = maybe_change_dere(self.dere_context, dere_types)
        if maybe_change_dere_response:
            self.turns_in_same_dere = 0  # Reset turns_in_same_dere
            if self.debug:
                print(f"WaifuChatbot.respond: Dere type changed: {maybe_change_dere_response}")
            return maybe_change_dere_response
        else:
            self.turns_in_same_dere += 1  # Increment turns_in_same_dere

        if self.debug:
            print(f"WaifuChatbot.respond: Calling response generator")
        # Delegate to the personality's generate_response method
        response = self.personality.generate_response(tokens, {"waifu_memory": self.waifu_memory, "debug": self.debug, "conversation_context": self.conversation_context, "current_dere": self.current_dere, "waifu_chatbot": self})


        self.previous_input = original_input # Store the original input before processing

        # Add a small random affection change
        affection_change = random.randint(-1, 2)  # -1, 0, 1, or 2
        self.waifu_memory.affection += affection_change
        self.waifu_memory.affection = max(0, min(100, self.waifu_memory.affection)) # Keep within 0-100
        if self.debug:
            print(f"WaifuChatbot.respond: Affection changed by {affection_change}, new affection: {self.waifu_memory.affection}")




        return response