from typing import Dict, List, Tuple, Callable, Any, Optional, Set
from transformations import apply_transformations
from utils import tokenize, matches
from dere_manager import dere_response, default_responses, get_current_dere, maybe_change_dere, dere_types
from conversation_context import ConversationContext
import json
import random # New import

class ResponseGenerator:
    def __init__(self, waifu_chatbot: Any, waifu_memory: Any, keywords: Dict[str, List[Tuple[str, Any]]], transformations: Dict[str, Tuple[Any, Optional[str], int]], response_templates: Dict[tuple[str, str], List[str]],  talk_about_interest: Callable[..., str], introduce_topic: Callable[..., str], generate_response: Callable[...,str], remember: Callable[..., None], debug: bool = False):
        self.waifu_chatbot = waifu_chatbot  # Store the WaifuChatbot instance
        self.waifu_memory = waifu_memory
        self.keywords = keywords
        self.transformations = transformations
        self.response_templates = response_templates
        self.talk_about_interest = talk_about_interest
        self.introduce_topic = introduce_topic
        self.generate_response = generate_response
        self.remember = remember
        #self.dere_context = dere_context # Removed
        self.debug = debug
        self.topic_context = False  # Flag for topic-specific context
        with open("src/chatbot_config.json", "r") as f:
            config = json.load(f)
            self.small_talk: List[str] = config["small_talk"]


    def _handle_topic_specific_response(self, tokens: List[str]) -> Optional[str]:
        """Handles topic-specific responses."""
        return None

    def _handle_transformations(self, tokens: List[str]) -> Optional[str]:
        """Handles transformations."""
        print(f"ResponseGenerator._handle_transformations: Entering")
        # Access dere_context from waifu_chatbot instance
        transformed = apply_transformations(self.transformations, tokens, self.waifu_memory, self.waifu_chatbot.dere_context.current_dere, self.talk_about_interest, self.introduce_topic, dere_response, maybe_change_dere, self.generate_response, self.remember, self.response_templates, self.waifu_chatbot.dere_context.used_responses, dere_types, self.debug, self.waifu_chatbot)
        return transformed

    def _handle_keywords(self, tokens: List[str]) -> Optional[str]:
        """Handles general keywords."""
        print(f"ResponseGenerator._handle_keywords: Entering")
        for word in tokens:
            if word in self.keywords:
                responses = self.keywords[word]
                for resp_pattern, resp_text in responses:
                    if matches(tokenize(resp_pattern), tokens):
                        # Access dere_context from waifu_chatbot instance
                        self.waifu_chatbot.dere_context.used_responses.add(resp_text)
                        print (f"ResponseGenerator._handle_keywords: Matched keyword: {word}, response: {resp_text}")
                        return resp_text
        return None

    def _get_default_response(self) -> str:
        """Gets the default response."""
        print(f"ResponseGenerator._get_default_response: Entering")
        # Access dere_context from waifu_chatbot instance
        current_dere = get_current_dere(self.waifu_memory.affection)  # Get the current dere type
        #if current_dere in default_responses: # Removed
        #    return random.choice(default_responses[current_dere])
        #else:
        #    # Fallback if dere type somehow not in defaults
        #    # Access dere_context from waifu_chatbot instance
        #    return maybe_change_dere(self.waifu_chatbot.dere_context, dere_types,
        #        "What are you talking about?", "I don't get it.", "Hmph.", "O-okay..."
        #    )
        return dere_response(self.waifu_chatbot.dere_context, *default_responses.get(current_dere, ["..."])) # Use dere_response

    def _maybe_use_small_talk(self) -> Optional[str]:
        """Uses small talk based on randomness"""
        if (random.random() < 0.1):
            return random.choice(self.small_talk)
        return None

    def generate(self, input_str: str, tokens: List[str]) -> str:
        """Generates a response to the user's input.
                """
        # Check for topic-specific responses first and respond based on the current topic, if any
        print(f"ResponseGenerator.generate: Entering with input: {input_str}")

        # Call respond_based_on_current_topic here
        print(f"ResponseGenerator.generate: topic_context = {self.topic_context}") # Debug print
        topic_response = self.waifu_chatbot.topic_manager.respond_based_on_current_topic(tokens, self.keywords)
        if topic_response:
            print(f"ResponseGenerator.generate: Returning topic response: {topic_response}")
            self.topic_context = True # Set topic_context to True
            return topic_response

        if self.topic_context:
            print(f"ResponseGenerator.generate: In topic context, trying to generate topic-specific response")
            # Prioritize topic-specific responses
            topic_response = self.waifu_chatbot.topic_manager.respond_based_on_current_topic(tokens, self.keywords)
            if topic_response:
                print(f"ResponseGenerator.generate: Returning topic response: {topic_response}")
                return topic_response
            else:
                # If no topic-specific response, still allow other responses, but with lower priority
                print(f"ResponseGenerator.generate: No specific topic response found in topic context")
                #self.topic_context = False # Reset topic_context if no response found

        # Then check for transformations
        response = self._handle_transformations(tokens)
        if response:
            print(f"ResponseGenerator.generate: Returning transformation response: {response}")
            return response
          
        # Then check for keywords
        response = self._handle_keywords(tokens)
        if response:
            print(f"ResponseGenerator.generate: Returning keyword response: {response}")
            return response



        # Use small talk
        response = self._maybe_use_small_talk()
        if response:
            print(f"ResponseGenerator.generate: Returning small talk response: {response}")
            return response

        # Get the default response
        response =  self._get_default_response()
        print(f"ResponseGenerator.generate: Returning default response: {response}")
        return response