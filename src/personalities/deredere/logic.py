from typing import List, Dict, Any, Optional, Set, Tuple, Callable
import random
from personalities.personality_interface import PersonalityInterface
from personalities.deredere.data import deredere_responses
from keyword_handler import handle_keywords
from transformations import apply_transformations
from utils import tokenize, matches


class DeredereLogic(PersonalityInterface):
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.used_default_responses: Set[str] = set()
        self.test_counter = 0 # For testing


    def generate_response(self, input_tokens: List[str], context: Dict[str, Any]) -> str:
        waifu = context["waifu_chatbot"]
        self.test_counter += 1

        if self.debug:
            print(f"DeredereLogic.generate_response: Entering with tokens: {input_tokens}")

        # Handle keywords
        keyword_response = self.handle_keywords(input_tokens, waifu.registry.keywords, self.debug) # Use waifu.registry
        if keyword_response:
            if self.debug:
                print("DeredereLogic.generate_response: Keyword response triggered.")
            return keyword_response

        # Handle transformations
        transformed_response = self.handle_transformations(waifu.registry.transformations, input_tokens, context["waifu_memory"], context["current_dere"],
            lambda *args: "I like chatting!", self.introduce_topic,
            lambda context, *resps: random.choice(resps or ["..."]), {}, set(), [], self.debug, waifu
        ) # Use waifu.registry
        if transformed_response:
            if self.debug:
                print("DeredereLogic.generate_response: Transformation response triggered.")
            return transformed_response

        # Introduce a new topic if needed
        # new_topic_response = self.maybe_introduce_topic(context, " ".join(input_tokens), waifu.turn_count)
        # if new_topic_response:
        #     return new_topic_response

        # Try to respond based on current topic
        # topic_response = self.respond_based_on_current_topic(waifu, input_tokens, waifu.registry.keywords, context, {})
        # if topic_response:
        #     return topic_response


        # # For testing - force different response types
        # if self.test_counter == 1:
        #     return "Forced Keyword Response"
        # elif self.test_counter == 2:
        #     return "Forced Transformation Response"
        # elif self.test_counter == 3:
        #     waifu.current_topic = "family"  # Force a topic
        #     waifu.topic_turns = 2
        #     return "Forced Topic Response"
        # elif self.test_counter == 4:
        #     waifu.current_topic = "family"
        #     waifu.topic_turns = 1 # Simulate topic turn
        #     return self.respond_based_on_current_topic(waifu, ["family"], {}, context, {}) # Force a topic response check
        # else:
        #     return self.get_default_response(context)
        # Get default response
        if self.debug:
            print("DeredereLogic.generate_response: Using default response.")
        return self.get_default_response(context)


    def handle_topic_response(self, input_tokens: List[str], topic: str, context: Dict[str, Any]) -> Optional[str]:
        # This method is not being used correctly. Logic moved to respond_based_on_current_topic
        return None

    def get_default_response(self, context: Dict[str, Any]) -> str:
        # Use the class-level used_default_responses
        defaults = ["Okay!", "Tell me more!", "That’s fun!", "Sounds good!"]
        unused = [r for r in defaults if r not in self.used_default_responses]
        if unused:
            response = random.choice(unused)
            self.used_default_responses.add(response)  # Add to the class-level set
        else:
            self.used_default_responses.clear()
            response = random.choice(defaults)
            self.used_default_responses.add(response)
        return response

    def introduce_topic(self, topic: str, context: Dict[str, Any]) -> str:
        # introductions = {
        #     "family": "Hey, let’s talk about family! What are yours like?",
        #     "childhood": "Ooh, childhood stories! What was yours like?",
        #     "feelings": "How are you feeling today? I’d love to know!",
        #     "relationship": "So, are you seeing anyone special?",
        #     "food": "What’s your favorite food? I’m curious!",
        #     "interest_manga": "I love manga! What are you reading?",
        #     "interest_anime": "Anime is awesome! What are you watching?",
        #     "interest_games": "Let's play some games! What are your favorites?",
        #     "interest_cooking": "I love to cook! What's your favorite dish to make?",
        # }
        # return introductions.get(topic, f"Let’s chat about {topic}!")
        return "" # Disable for now

    def get_data(self) -> Dict[str, Any]:
        return {"responses": deredere_responses, "default_responses": ["Okay!", "Tell me more!", "That's fun!", "Sounds good!"]}

    def handle_keywords(self, tokens: List[str], keywords: Dict[str, List[Tuple[str, Any]]], debug: bool) -> Optional[str]:
        """Handles general keywords."""
        if debug:
            print(f"DeredereLogic.handle_keywords: Entering with tokens: {tokens}")
            print(f"DeredereLogic.handle_keywords: Keywords: {keywords}")

        for word in tokens:
            if word in keywords:
                if debug:
                    print(f"DeredereLogic.handle_keywords: Checking word: {word}")
                responses = keywords[word]
                for resp_pattern, resp_text in responses:
                    if debug:
                        print(f"DeredereLogic.handle_keywords: Checking pattern: {resp_pattern}")
                    if matches(tokenize(resp_pattern), tokens):
                        if debug:
                            print(f"DeredereLogic.handle_keywords: Matched keyword: {word}, response: {resp_text}")
                        return resp_text
        if debug:
            print("DeredereLogic.handle_keywords: No keyword match found.")
        return None


    def handle_transformations(self, transformations: Dict[str, Tuple[Any, Optional[str], int]], input_list: List[str], waifu_memory: Any, current_dere: str, talk_about_interest: Callable[..., str], introduce_topic: Callable[..., str], dere_response: Callable[..., str], response_templates: Dict[tuple[str, str], List[str]], used_responses: Set[str], dere_types: List[str], debug: bool, waifu_chatbot: Any) -> Optional[str]:
        """Applies transformations to the input and returns a transformed response."""
        if self.debug:
            print(f"DeredereLogic.handle_transformations: Entering with input: {input_list}")
            print(f"DeredereLogic.handle_transformations: Transformations: {transformations}")

        for pattern, (response, memory_slot, affection_change) in transformations.items():
            pattern_list = pattern.split()
            if self.debug:
                print(f"DeredereLogic.handle_transformations: Checking pattern: {pattern}")
            if matches(pattern_list, input_list):
                if self.debug:
                    print(f"DeredereLogic.handle_transformations: Matched pattern: {pattern}")
                # Simplified logic for now, no complex response handling
                if isinstance(response, list):
                    response_text = random.choice(response) # Just pick a random response
                else:
                    response_text = str(response)

                # Handle substitutions (only '*' for now)
                for i in range(len(pattern_list)):
                    if pattern_list[i] == '*':
                        if len(input_list) > i:
                            response_text = response_text.replace("*", " ".join(input_list[i:]), 1)
                            break # Only replace the first '*'

                if memory_slot:
                    # Simplified memory handling
                    value = " ".join(input_list)
                    waifu_memory.remember(memory_slot, value, affection_change) # Use the remember method
                    if self.debug:
                        print(f"DeredereLogic.handle_transformations: Remembered: {memory_slot} = {value}")

                return response_text

        if self.debug:
            print("DeredereLogic.handle_transformations: No transformation match found.")
        return None

    def maybe_introduce_topic(self, context: Dict[str, Any], input_str: str, turn_count: int) -> Optional[str]:
        """Introduces a new topic based on affection level, randomness, and topic counts."""
        return None # Disable for now

    def respond_based_on_current_topic(self, waifu_chatbot: Any, tokens: List[str], keywords: Dict[str, List[Tuple[str, Any]]], context: Dict[str, Any], response_templates: Dict[tuple[str, str], List[str]]) -> Optional[str]:
        """Responds based on the current topic, if any."""
        return None # Disable for now
