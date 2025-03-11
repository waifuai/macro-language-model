from typing import Dict, List, Tuple, Callable, Any, Optional, Set
from transformations import apply_transformations
from utils import tokenize, matches
from dere_manager import DereContext
from dere_response_selection import get_dere_default_response
from dere_data import dere_types, default_responses
from conversation_context import ConversationContext
import json
import random
from response_template_loader import load_response_templates
from keyword_handler import handle_keywords
from small_talk import maybe_use_small_talk


class ResponseGenerator:
    def __init__(self, waifu_chatbot: Any, waifu_memory: Any, keywords: Dict[str, List[Tuple[str, Any]]], transformations: Dict[str, Tuple[Any, Optional[str], int]], talk_about_interest: Callable[..., str], introduce_topic: Callable[..., str], remember: Callable[..., None], debug: bool = False):
        self.waifu_chatbot = waifu_chatbot  # Store the WaifuChatbot instance
        self.waifu_memory = waifu_memory
        self.keywords = keywords
        self.transformations = transformations
        self.response_templates = load_response_templates() # Use the loader function
        self.talk_about_interest = talk_about_interest
        self.introduce_topic = introduce_topic
        self.remember = remember
        self.debug = debug
        self.topic_context = False  # Flag for topic-specific context
        self.used_default_responses: Set[str] = set()
        self.used_small_talk: Set[str] = set()
        with open("chatbot_config.json", "r") as f:
            config = json.load(f)
            self.small_talk: List[str] = config["small_talk"]

    def _handle_transformations(self, tokens: List[str]) -> Optional[str]:
        """Handles transformations."""
        if self.waifu_chatbot.debug:
            print(f"ResponseGenerator._handle_transformations: Entering")
        return apply_transformations(self.transformations, tokens, self.waifu_memory, self.waifu_chatbot.dere_context.current_dere, self.talk_about_interest, self.introduce_topic, get_dere_default_response, self.response_templates, self.waifu_chatbot.dere_context.used_responses, dere_types, self.waifu_chatbot.debug, self.waifu_chatbot)

    
    def _select_response(self, tokens: List[str]) -> str:
        """Selects the most appropriate response based on priority."""
        # 1. Topic-specific responses
        topic_response = self.waifu_chatbot.topic_manager.respond_based_on_current_topic(tokens, self.keywords)
        if topic_response:
            self.topic_context = True
            return topic_response

        # 2. Transformations
        transformed_response = self._handle_transformations(tokens) # Simplified call
        if transformed_response:
            return transformed_response

        # 3. Keywords
        keyword_response = handle_keywords(tokens, self.keywords, self.waifu_chatbot.dere_context.used_responses, self.debug) # Use handler
        if keyword_response:
            return keyword_response

        # 4. Small talk (less frequent)
        small_talk_response = maybe_use_small_talk(self.small_talk, self.used_small_talk) # Use imported function
        if small_talk_response:
            return small_talk_response

        # 5. Default response
        return get_dere_default_response(self.waifu_chatbot.dere_context, self.used_default_responses) # Use imported function

    def generate(self, input_str: str, tokens: List[str]) -> str:
        """Generates a response to the user's input."""
        if self.waifu_chatbot.debug:
            print(f"ResponseGenerator.generate: Entering with input: {input_str}")
            print(f"ResponseGenerator.generate: topic_context = {self.topic_context}")

        return self._select_response(tokens)
