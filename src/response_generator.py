from typing import Dict, List, Tuple, Callable, Any, Optional, Set
from transformations import apply_transformations
from utils import tokenize, matches
from dere_manager import dere_response, default_responses, get_current_dere, maybe_change_dere, dere_types
from conversation_context import ConversationContext
import json
import random # New import

class ResponseGenerator:
    def __init__(self, waifu_memory: Any, keywords: Dict[str, List[Tuple[str, Any]]], transformations: Dict[str, Tuple[Any, Optional[str], int]], response_templates: Dict[tuple[str, str], List[str]],  talk_about_interest: Callable[..., str], introduce_topic: Callable[..., str], generate_response: Callable[...,str], remember: Callable[..., None], dere_context: Any, debug: bool = False):
        self.waifu_memory = waifu_memory
        self.keywords = keywords
        self.transformations = transformations
        self.response_templates = response_templates
        self.talk_about_interest = talk_about_interest
        self.introduce_topic = introduce_topic
        self.generate_response = generate_response
        self.remember = remember
        self.dere_context = dere_context
        self.debug = debug
        with open("src/chatbot_config.json", "r") as f:
            config = json.load(f)
            self.small_talk: List[str] = config["small_talk"]


    def _handle_topic_specific_response(self, tokens: List[str]) -> Optional[str]:
        """Handles topic-specific responses."""
        return None

    def _handle_transformations(self, tokens: List[str]) -> Optional[str]:
        """Handles transformations."""
        transformed = apply_transformations(self.transformations, tokens, self.waifu_memory, self.dere_context.current_dere, self.talk_about_interest, self.introduce_topic, dere_response, maybe_change_dere, self.generate_response, self.remember, self.response_templates, self.dere_context.used_responses, dere_types, self.debug)
        return transformed

    def _handle_keywords(self, tokens: List[str]) -> Optional[str]:
        """Handles general keywords."""
        for word in tokens:
            if word in self.keywords:
                responses = self.keywords[word]
                for resp_pattern, resp_text in responses:
                    if matches(tokenize(resp_pattern), tokens):
                        self.dere_context.used_responses.add(resp_text)
                        return resp_text
        return None

    def _get_default_response(self) -> str:
        """Gets the default response."""
        current_dere = get_current_dere(self.waifu_memory.affection)  # Get the current dere type
        if current_dere in default_responses:
            return random.choice(default_responses[current_dere])
        else:
            # Fallback if dere type somehow not in defaults
            return maybe_change_dere(self.dere_context, dere_types,
                "What are you talking about?", "I don't get it.", "Hmph.", "O-okay..."
            )

    def _maybe_use_small_talk(self) -> Optional[str]:
        """Uses small talk based on randomness"""
        if (random.random() < 0.1):
            return random.choice(self.small_talk)
        return None

    def generate(self, input_str: str, tokens: List[str]) -> str:
        """Generates a response to the user's input.
                """
        # Check for topic-specific responses first and respond based on the current topic, if any

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