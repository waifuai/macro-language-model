from typing import Dict, List, Tuple, Callable, Any, Optional, Set
from transformations import apply_transformations  # Modified import
from utils import tokenize, matches
from conversation_context import ConversationContext
import json
import random
from response_template_loader import load_response_templates
from small_talk import maybe_use_small_talk


class ResponseGenerator:
    def __init__(self, waifu_chatbot: Any, waifu_memory: Any, transformations: Dict[str, Tuple[Any, Optional[str], int]], talk_about_interest: Callable[..., str], introduce_topic: Callable[..., str], remember: Callable[..., None], debug: bool = False): # Removed keywords parameter
        self.waifu_chatbot = waifu_chatbot  # Store the WaifuChatbot instance
        self.waifu_memory = waifu_memory
        # self.keywords = keywords # REMOVED
        self.transformations = transformations
        self.response_templates = load_response_templates()  # Use the loader function
        self.talk_about_interest = talk_about_interest
        self.introduce_topic = introduce_topic
        self.remember = remember
        self.debug = debug
        self.topic_context = False  # Flag for topic-specific context
        self.used_default_responses: Set[str] = set()
        self.used_small_talk: Set[str] = set()
        self.turns_since_small_talk = 0  # Add a counter for small talk
        with open("chatbot_config.json", "r") as f:
            config = json.load(f)
            self.small_talk: List[str] = config["small_talk"]

    def _handle_transformations(self, tokens: List[str]) -> Optional[str]:
        """Handles transformations."""
        # if self.waifu_chatbot.debug:
        #     print(f"ResponseGenerator._handle_transformations: Entering")
        # Delegate transformation handling to the personality
        return self.waifu_chatbot.personality.handle_transformations(self.transformations, tokens, self.waifu_memory, self.talk_about_interest, self.introduce_topic, self.debug)


    def _select_response(self, tokens: List[str]) -> str:
        """Selects the most appropriate response based on priority."""
        # if self.waifu_chatbot.debug:
        #     print(f"ResponseGenerator._select_response: Entering")

        # 1. Keywords (Prioritized) - REMOVED

        # 2. Topic-specific responses
        if self.waifu_chatbot.topic_manager.current_topic:
            # Delegate to personality
            # Removed self.keywords from the call below
            topic_response = self.waifu_chatbot.personality.respond_based_on_current_topic(tokens, {"dere_context": self.waifu_chatbot.dere_context}, self.response_templates)
            if topic_response:
                # if self.waifu_chatbot.debug:
                #     print(f"ResponseGenerator._select_response: Topic response selected: {topic_response}")
                return topic_response

        # 3. Transformations
        transformed_response = self._handle_transformations(tokens)
        if transformed_response:
            # if self.waifu_chatbot.debug:
            #     print(f"ResponseGenerator._select_response: Transformed response selected: {transformed_response}")
            return transformed_response

        # 4. Small talk (more frequent)
        if self.turns_since_small_talk > 1:  # Reduced threshold
            small_talk_response = maybe_use_small_talk(self.small_talk, self.used_small_talk)
            if small_talk_response:
                # if self.waifu_chatbot.debug:
                #     print(f"ResponseGenerator._select_response: Small talk response selected: {small_talk_response}")
                self.turns_since_small_talk = 0  # Reset the counter
                return small_talk_response
        else:
            self.turns_since_small_talk += 1
            # if self.waifu_chatbot.debug:
            #     print(f"ResponseGenerator._select_response: Skipping small talk, turns_since_small_talk = {self.turns_since_small_talk}")

        # 5. Default response
        # Delegate to personality
        default_response = self.waifu_chatbot.personality.get_default_response({"waifu_memory": self.waifu_memory, "debug": self.debug, "conversation_context": self.waifu_chatbot.conversation_context})

        # if self.waifu_chatbot.debug:
        #     print(f"ResponseGenerator._select_response: Default response selected: {default_response}")
        return default_response

    def generate(self, input_str: str, tokens: List[str], keyword: str = None, substitutions: Dict[str, Any] = None) -> str:
        """Generates a response to the user's input. Now accepts optional keyword and substitutions."""
        # if self.waifu_chatbot.debug:
        #     print(f"ResponseGenerator.generate: Entering with input: {input_str}")
        #     print(f"ResponseGenerator.generate: topic_context = {self.topic_context}")

        response = self._select_response(tokens)
        return response.encode('utf-8', 'replace').decode('utf-8')

    # REMOVED generate method that accepted keyword/substitutions
    # def generate(self, input_str: str, tokens: List[str], keyword: str = None, substitutions: Dict[str, Any] = None) -> str:
    #     """Generates a response to the user's input. Now accepts optional keyword and substitutions."""
    #     # if self.waifu_chatbot.debug:
    #     #     print(f"ResponseGenerator.generate: Entering with input: {input_str}")
    #     #     print(f"ResponseGenerator.generate: topic_context = {self.topic_context}")
    #
    #     response = self._select_response(tokens)
    #     return response.encode('utf-8', 'replace').decode('utf-8')

    def generate(self, input_str: str, tokens: List[str]) -> str: # Simplified generate method
        """Generates a response to the user's input."""
        # if self.waifu_chatbot.debug:
        #     print(f"ResponseGenerator.generate: Entering with input: {input_str}")
        #     print(f"ResponseGenerator.generate: topic_context = {self.topic_context}")

        response = self._select_response(tokens)
        return response.encode('utf-8', 'replace').decode('utf-8')


    def get_response_template(self, transformed_input: str, context: Dict[str, Any]) -> Optional[str]:
        """Gets a response template based on the transformed input."""
        # Basic implementation: Return None, which will lead to using the default response.
        # if self.waifu_chatbot.debug:
        #     print("get_response_template called")
        return None
