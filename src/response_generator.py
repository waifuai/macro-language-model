from typing import Dict, List, Tuple, Callable, Any, Optional, Set
from transformation_handlers import apply_transformations # Modified import
from utils import tokenize, matches
from dere_manager import DereContext, get_current_dere
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
        self.turns_since_small_talk = 0 # Add a counter for small talk
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
        if self.waifu_chatbot.debug:
            print(f"ResponseGenerator._select_response: Entering")

        # 1. Keywords (Prioritized)
        print(f"ResponseGenerator: Type of dere_context.used_responses before keyword: {type(self.waifu_chatbot.dere_context.used_responses)}") # DEBUG PRINT
        keyword_response = handle_keywords(tokens, self.keywords, self.waifu_chatbot.dere_context.used_responses, self.debug)
        print(f"ResponseGenerator: Type of dere_context.used_responses after keyword: {type(self.waifu_chatbot.dere_context.used_responses)}") # DEBUG PRINT
        if keyword_response:
            if self.waifu_chatbot.debug:
                print(f"ResponseGenerator._select_response: Keyword response selected: {keyword_response}")
            return keyword_response

        # 2. Topic-specific responses
        if self.waifu_chatbot.topic_manager.current_topic:
            print(f"ResponseGenerator: Type of dere_context.used_responses before topic: {type(self.waifu_chatbot.dere_context.used_responses)}") # DEBUG PRINT
            topic_response = self.waifu_chatbot.topic_manager.respond_based_on_current_topic(tokens, self.keywords, self.waifu_chatbot.dere_context, self.response_templates) # Pass response_templates
            print(f"ResponseGenerator: Type of dere_context.used_responses after topic: {type(self.waifu_chatbot.dere_context.used_responses)}") # DEBUG PRINT
            if topic_response:
                if self.waifu_chatbot.debug:
                    print(f"ResponseGenerator._select_response: Topic response selected: {topic_response}")
                return topic_response

        # 3. Transformations
        transformed_response = self._handle_transformations(tokens)
        if transformed_response:
            if self.waifu_chatbot.debug:
                print(f"ResponseGenerator._select_response: Transformed response selected: {transformed_response}")
            return transformed_response

        # 4. Small talk (more frequent)
        if self.turns_since_small_talk > 1: # Reduced threshold
            small_talk_response = maybe_use_small_talk(self.small_talk, self.used_small_talk)
            if small_talk_response:
                if self.waifu_chatbot.debug:
                    print(f"ResponseGenerator._select_response: Small talk response selected: {small_talk_response}")
                self.turns_since_small_talk = 0 # Reset the counter
                return small_talk_response
        else:
            self.turns_since_small_talk += 1
            if self.waifu_chatbot.debug:
                print(f"ResponseGenerator._select_response: Skipping small talk, turns_since_small_talk = {self.turns_since_small_talk}")

        # 5. Default response
        default_response = get_dere_default_response(self.waifu_chatbot.dere_context, self.used_default_responses)
        if self.waifu_chatbot.debug:
            print(f"ResponseGenerator._select_response: Default response selected: {default_response}")
        return default_response

    def generate(self, input_str: str, tokens: List[str], keyword: str = None, substitutions: Dict[str, Any] = None) -> str:
        """Generates a response to the user's input. Now accepts optional keyword and substitutions."""
        if self.waifu_chatbot.debug:
            print(f"ResponseGenerator.generate: Entering with input: {input_str}")
            print(f"ResponseGenerator.generate: topic_context = {self.topic_context}")

        # Use provided keyword and substitutions if available, otherwise proceed as before
        if keyword:
            if self.waifu_chatbot.debug:
                print(f"ResponseGenerator.generate: Generating response for topic keyword: {keyword}")
            return generate_response(
                self.response_templates,
                keyword,
                substitutions if substitutions else {},
                self.waifu_chatbot.dere_context.used_responses,
                self.waifu_memory,
                self.waifu_chatbot.dere_context.current_dere,
                dere_response,
                self.waifu_chatbot.debug,
                self.used_default_responses,
                input_str
            )
        else:
            return self._select_response(tokens)
