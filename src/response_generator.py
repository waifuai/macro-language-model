from typing import Dict, List, Tuple, Callable, Any, Optional, Set
from transformations import apply_transformations
from utils import tokenize, matches
from dere_manager import dere_response, get_current_dere, maybe_change_dere, DereContext
from dere_data import dere_types, default_responses
from conversation_context import ConversationContext
import json
import random
# Corrected imports:
from response_templates.tsundere import tsundere_responses
from response_templates.yandere import yandere_responses
from response_templates.kuudere import kuudere_responses
from response_templates.dandere import dandere_responses
from response_templates.himedere import himedere_responses
from response_templates.deredere import deredere_responses


class ResponseGenerator:
    # Removed response_templates from __init__
    def __init__(self, waifu_chatbot: Any, waifu_memory: Any, keywords: Dict[str, List[Tuple[str, Any]]], transformations: Dict[str, Tuple[Any, Optional[str], int]], talk_about_interest: Callable[..., str], introduce_topic: Callable[..., str], generate_response: Callable[...,str], remember: Callable[..., None], debug: bool = False):
        self.waifu_chatbot = waifu_chatbot  # Store the WaifuChatbot instance
        self.waifu_memory = waifu_memory
        self.keywords = keywords
        self.transformations = transformations
        # Construct response_templates here:
        self.response_templates = {
            ("feeling", "tsundere"): tsundere_responses["feeling"],
            ("family", "tsundere"): tsundere_responses["family"],
            ("childhood", "tsundere"): tsundere_responses["childhood"],
            ("insult", "tsundere"): tsundere_responses["insult"],
            ("compliment", "tsundere"): tsundere_responses["compliment"],
            ("interest_manga", "tsundere"): tsundere_responses["interest_manga"],
            ("interest_anime", "tsundere"): tsundere_responses["interest_anime"],
            ("interest_games", "tsundere"): tsundere_responses["interest_games"],
            ("interest_cooking", "tsundere"): tsundere_responses["interest_cooking"],
            ("relationship_status", "tsundere"): tsundere_responses["relationship_status"],
            ("favorite_food", "tsundere"): tsundere_responses["favorite_food"],
            ("personality_quirks", "tsundere"): tsundere_responses["personality_quirks"],
            ("feeling", "yandere"): yandere_responses["feeling"],
            ("family", "yandere"): yandere_responses["family"],
            ("childhood", "yandere"): yandere_responses["childhood"],
            ("insult", "yandere"): yandere_responses["insult"],
            ("compliment", "yandere"): yandere_responses["compliment"],
            ("interest_manga", "yandere"): yandere_responses["interest_manga"],
            ("interest_anime", "yandere"): yandere_responses["interest_anime"],
            ("interest_games", "yandere"): yandere_responses["interest_games"],
            ("interest_cooking", "yandere"): yandere_responses["interest_cooking"],
            ("relationship_status", "yandere"): yandere_responses["relationship_status"],
            ("favorite_food", "yandere"): yandere_responses["favorite_food"],
            ("personality_quirks", "yandere"): yandere_responses["personality_quirks"],
            ("feeling", "kuudere"): kuudere_responses["feeling"],
            ("family", "kuudere"): kuudere_responses["family"],
            ("childhood", "kuudere"): kuudere_responses["childhood"],
            ("insult", "kuudere"): kuudere_responses["insult"],
            ("compliment", "kuudere"): kuudere_responses["compliment"],
            ("interest_manga", "kuudere"): kuudere_responses["interest_manga"],
            ("interest_anime", "kuudere"): kuudere_responses["interest_anime"],
            ("interest_games", "kuudere"): kuudere_responses["interest_games"],
            ("interest_cooking", "kuudere"): kuudere_responses["interest_cooking"],
            ("relationship_status", "kuudere"): kuudere_responses["relationship_status"],
            ("favorite_food", "kuudere"): kuudere_responses["favorite_food"],
            ("personality_quirks", "kuudere"): kuudere_responses["personality_quirks"],
            ("feeling", "dandere"): dandere_responses["feeling"],
            ("family", "dandere"): dandere_responses["family"],
            ("childhood", "dandere"): dandere_responses["childhood"],
            ("insult", "dandere"): dandere_responses["insult"],
            ("compliment", "dandere"): dandere_responses["compliment"],
            ("interest_manga", "dandere"): dandere_responses["interest_manga"],
            ("interest_anime", "dandere"): dandere_responses["interest_anime"],
            ("interest_games", "dandere"): dandere_responses["interest_games"],
            ("interest_cooking", "dandere"): dandere_responses["interest_cooking"],
            ("relationship_status", "dandere"): dandere_responses["relationship_status"],
            ("favorite_food", "dandere"): dandere_responses["favorite_food"],
            ("personality_quirks", "dandere"): dandere_responses["personality_quirks"],
            ("feeling", "himedere"): himedere_responses["feeling"],
            ("family", "himedere"): himedere_responses["family"],
            ("childhood", "himedere"): himedere_responses["childhood"],
            ("insult", "himedere"): himedere_responses["insult"],
            ("compliment", "himedere"): himedere_responses["compliment"],
            ("interest_manga", "himedere"): himedere_responses["interest_manga"],
            ("interest_anime", "himedere"): himedere_responses["interest_anime"],
            ("interest_games", "himedere"): himedere_responses["interest_games"],
            ("interest_cooking", "himedere"): himedere_responses["interest_cooking"],
            ("relationship_status", "himedere"): himedere_responses["relationship_status"],
            ("favorite_food", "himedere"): himedere_responses["favorite_food"],
            ("personality_quirks", "himedere"): himedere_responses["personality_quirks"],
            ("feeling", "deredere"): deredere_responses["feeling"],
            ("family", "deredere"): deredere_responses["family"],
            ("childhood", "deredere"): deredere_responses["childhood"],
            ("insult", "deredere"): deredere_responses["insult"],
            ("compliment", "deredere"): deredere_responses["compliment"],
            ("interest_manga", "deredere"): deredere_responses["interest_manga"],
            ("interest_anime", "deredere"): deredere_responses["interest_anime"],
            ("interest_games", "deredere"): deredere_responses["interest_games"],
            ("interest_cooking", "deredere"): deredere_responses["interest_cooking"],
            ("relationship_status", "deredere"): deredere_responses["relationship_status"],
            ("favorite_food", "deredere"): deredere_responses["favorite_food"],
            ("personality_quirks", "deredere"): deredere_responses["personality_quirks"],
        }
        self.talk_about_interest = talk_about_interest
        self.introduce_topic = introduce_topic
        self.generate_response = generate_response  # Unused
        self.remember = remember
        #self.dere_context = dere_context # Removed
        self.debug = debug
        self.topic_context = False  # Flag for topic-specific context
        self.used_default_responses: Set[str] = set() # Add used_default_responses
        self.used_small_talk: Set[str] = set()
        with open("src/chatbot_config.json", "r") as f:
            config = json.load(f)
            self.small_talk: List[str] = config["small_talk"]
        # self.small_talk: List[str] = []


    def _handle_topic_specific_response(self, tokens: List[str]) -> Optional[str]:
        """Handles topic-specific responses."""
        return None

    def _handle_transformations(self, tokens: List[str]) -> Optional[str]:
        """Handles transformations."""
        if self.waifu_chatbot.debug:
            print(f"ResponseGenerator._handle_transformations: Entering")
        # Access dere_context from waifu_chatbot instance
        transformed = apply_transformations(self.transformations, tokens, self.waifu_memory, self.waifu_chatbot.dere_context.current_dere, self.talk_about_interest, self.introduce_topic, dere_response, maybe_change_dere, self.generate_response, self.remember, self.response_templates, self.waifu_chatbot.dere_context.used_responses, dere_types, self.waifu_chatbot.debug, self.waifu_chatbot)
        return transformed

    def _handle_keywords(self, tokens: List[str]) -> Optional[str]:
        """Handles general keywords."""
        if self.waifu_chatbot.debug:
            print(f"ResponseGenerator._handle_keywords: Entering")
        for word in tokens:
            if word in self.keywords:
                responses = self.keywords[word]
                for resp_pattern, resp_text in responses:
                    if matches(tokenize(resp_pattern), tokens):
                        # Access dere_context from waifu_chatbot instance
                        self.waifu_chatbot.dere_context.used_responses.add(resp_text)
                        if self.waifu_chatbot.debug:
                            print (f"ResponseGenerator._handle_keywords: Matched keyword: {word}, response: {resp_text}")
                        return resp_text
        return None

    def _get_intelligent_default_response(self, context: DereContext) -> str:
        """Returns a more intelligent default response based on the dere type."""
        dere_defaults = {
            "tsundere": [
                "Hmph, whatever.",
                "It's not like I care, b-baka!",
                "Don't get the wrong idea!",
                "Whatever you say...",
                "I'm not interested in that."
            ],
            "yandere": [
                "...",
                "I only care about you.",
                "Don't leave me.",
                "We'll be together forever.",
                "You're mine."
            ],
            "kuudere": [
                "...",
                "I see.",
                "That is logical.",
                "Indifferent.",
                "As you wish."
            ],
            "dandere": [
                "U-um...",
                "I-I'm sorry...",
                "O-okay...",
                "I-I'll try my best...",
                "E-excuse me..."
            ],
            "himedere": [
                "Fufufu...",
                "Kneel before me!",
                "You should be honored.",
                "Of course.",
                "Remember your place."
            ],
            "deredere": [
                "Okay!",
                "Sure!",
                "I understand.",
                "No problem!",
                "Got it!"
            ]
        }

        default_list = dere_defaults.get(context.current_dere, ["..."])
        unused_responses = [resp for resp in default_list if resp not in self.used_default_responses]

        if unused_responses:
            response = random.choice(unused_responses)
            self.used_default_responses.add(response)
            return response
        else:
            self.used_default_responses.clear()
            return random.choice(default_list)


    def _get_default_response(self) -> str:
        """Gets the default response."""
        if self.waifu_chatbot.debug:
            print(f"ResponseGenerator._get_default_response: Entering")
        # Access dere_context from waifu_chatbot instance
        #current_dere = get_current_dere(self.waifu_memory.affection)  # Get the current dere type # Removed
        #used_default_responses: Set[str] = set() # Removed

        #return dere_response(self.waifu_chatbot.dere_context, self.used_default_responses, *default_responses.get(current_dere, ["..."])) # Use dere_response
        return self._get_intelligent_default_response(self.waifu_chatbot.dere_context)

    def _maybe_use_small_talk(self) -> Optional[str]:
        """Uses small talk based on randomness"""
        unused_small_talk = [phrase for phrase in self.small_talk if phrase not in self.used_small_talk]
        if (random.random() < 0.1 and unused_small_talk):
            response = random.choice(unused_small_talk)
            self.used_small_talk.add(response)
            return response
        elif (random.random() < 0.1):
            # if all small talk has been used, we clear the used_small_talk
            # and pick a response again.
            self.used_small_talk.clear()
            response = random.choice(self.small_talk)
            self.used_small_talk.add(response)
            return random.choice(self.small_talk)
        return None

    def generate(self, input_str: str, tokens: List[str]) -> str:
        """Generates a response to the user's input.
                """
        # Check for topic-specific responses first and respond based on the current topic, if any
        if self.waifu_chatbot.debug:
            print(f"ResponseGenerator.generate: Entering with input: {input_str}")
            print(f"ResponseGenerator.generate: topic_context = {self.topic_context}") # Debug print
        topic_response = self.waifu_chatbot.topic_manager.respond_based_on_current_topic(tokens, self.keywords)
        if topic_response:
            if self.waifu_chatbot.debug:
                print(f"ResponseGenerator.generate: Returning topic response: {topic_response}")
            self.topic_context = True # Set topic_context to True
            return topic_response

        # Then check for transformations
        response = self._handle_transformations(tokens)
        if response:
            if self.waifu_chatbot.debug:
                print(f"ResponseGenerator.generate: Returning transformation response: {response}")
            return response

        # Then check for keywords
        response = self._handle_keywords(tokens)
        if response:
            if self.waifu_chatbot.debug:
                print(f"ResponseGenerator.generate: Returning keyword response: {response}")
            return response

        # Use small talk
        response = self._maybe_use_small_talk()
        if response:
            if self.waifu_chatbot.debug:
                print(f"ResponseGenerator.generate: Returning small talk response: {response}")
            return response

        # Get the default response
        response =  self._get_default_response()
        if self.waifu_chatbot.debug:
            print(f"ResponseGenerator.generate: Returning default response: {response}")
        return response
