import random
from typing import Dict, List, Optional
from utils import tokenize
from chatbot_config import greetings, farewells
from core.registry import Registry
from personalities.personality_interface import PersonalityInterface
from dere_types import DereContext
from dere_data import dere_types
from dere_utils import maybe_change_dere
from waifu_frame import WaifuFrame
from conversation_context import ConversationContext
from main_keywords import register_keywords
from main_transforms import register_transforms


class WaifuChatbot(object):
    def __init__(self, name: str, personality: str = "deredere", debug: bool = False) -> None:
        self.registry = Registry()
        self.waifu_memory: WaifuFrame = WaifuFrame(name)
        self.debug: bool = debug
        self.conversation_context = ConversationContext()
        self.greetings = greetings
        self.farewells = farewells
        self.current_topic = None  # Keep
        self.turns_since_last_topic = 0 # Keep
        self.topic_turns = 0 # Keep
        self.max_topic_turns = 3 # Keep
        self.turns_in_same_dere = 0
        self.previous_input = ""
        self.turn_count = 0 # Initialize turn_count

        # Load personality
        if personality == "deredere":
            from personalities.deredere.logic import DeredereLogic
            self.personality = DeredereLogic(debug)
        # Add other personalities similarly
        elif personality == "tsundere":
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
        else:
            raise ValueError(f"Invalid personality: {personality}")

        self.current_dere = personality
        self.dere_context = DereContext(self.waifu_memory, self.current_dere, set(), self.debug)

        register_keywords(self)  # Call keyword registration
        register_transforms(self)  # Call transformation registration
        if self.debug:
            print(f"WaifuChatbot.__init__: Keywords after registration: {self.registry.keywords}")
            print(f"WaifuChatbot.__init__: Transformations after registration: {self.registry.transformations}")


    def respond(self, input_str: str) -> str:
        self.conversation_context.conversation_history.append(("user", input_str))
        self.previous_input = input_str
        self.turn_count += 1
        tokens = tokenize(input_str)

        if self.debug:
            print(f"Input: {input_str}")
            print(f"Current Dere: {self.current_dere}")
            print(f"Turn Count: {self.turn_count}")

        # Dynamic dere type switching logic (Keep this)
        # maybe_change_dere_response = maybe_change_dere(self.dere_context, dere_types)
        # if maybe_change_dere_response:
        #     self.turns_in_same_dere = 0  # Reset turns_in_same_dere
        #     if self.debug:
        #         print(f"Dere type changed: {maybe_change_dere_response}")
        #     return maybe_change_dere_response
        # else:
        #     self.turns_in_same_dere += 1  # Increment turns_in_same_dere

        # # Introduce a new topic periodically
        # if self.turns_since_last_topic >= 5 and random.random() < 0.3:
        #     available_topics = ["family", "childhood", "feelings", "relationship", "food", "interest_manga", "interest_anime", "interest_games", "interest_cooking"]
        #     new_topic = random.choice(available_topics)
        #     self.current_topic = new_topic
        #     self.turns_since_last_topic = 0
        #     self.topic_turns = self.max_topic_turns
        #     intro = self.personality.introduce_topic(new_topic, {"waifu_memory": self.waifu_memory, "debug": self.debug})
        #     if self.debug:
        #         print(f"New topic: {new_topic}")
        #     return intro

        # Generate response using personality logic
        context = {
            "waifu_memory": self.waifu_memory,
            "debug": self.debug,
            "conversation_context": self.conversation_context,
            "current_dere": self.current_dere,
            "waifu_chatbot": self  # Pass the WaifuChatbot instance
        }
        response = self.personality.generate_response(tokens, context)

        if self.debug:
            print(f"Response: {response}")

        # Add a small random affection change
        affection_change = random.randint(-1, 2)  # -1, 0, 1, or 2
        self.waifu_memory.affection += affection_change
        self.waifu_memory.affection = max(0, min(100, self.waifu_memory.affection))  # Keep within 0-100
        if self.debug:
            print(f"Affection changed by {affection_change}, new affection: {self.waifu_memory.affection}")

        return response
