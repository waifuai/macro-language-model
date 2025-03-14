from typing import Dict, List
from chatbot_config import greetings, farewells
from waifu_frame import WaifuFrame
from conversation_context import ConversationContext
from waifu_chatbot_response import respond
from waifu_chatbot_init import initialize_personality, register_components

class WaifuChatbot:
    def __init__(self, name: str, personality: str = "deredere", debug: bool = False):
        self.waifu_memory = WaifuFrame(name)
        self.debug = debug
        self.conversation_context = ConversationContext()
        self.greetings = greetings
        self.farewells = farewells
        self.current_topic = None
        self.turns_since_last_topic = 0
        self.topic_turns = 0
        self.max_topic_turns = 3
        self.turn_count = 0
        self.previous_input = ""
        initialize_personality(self, personality)
        register_components(self)

    def respond(self, input_str: str) -> str:
        return respond(self, input_str)
