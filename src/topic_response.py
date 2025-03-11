import random
from typing import List, Optional, Dict, Any, Tuple
from dere_manager import DereContext, dere_response
from utils import tokenize, matches
from topics import introduce_topic
from conversation_context import ConversationContext
from response_generation import generate_response
import re

def respond_based_on_current_topic(self, tokens: List[str], keywords: Dict[str, List[Tuple[str, Any]]]) -> Optional[str]:
    """Responds based on the current topic, if any."""
    if self.waifu_chatbot.debug:
        print(f"TopicManager.respond_based_on_current_topic: Entering with tokens: {tokens}")
    if self.current_topic:
        if self.waifu_chatbot.debug:
            print(f"TopicManager.respond_based_on_current_topic: Current topic: {self.current_topic}, topic_turns: {self.topic_turns}")

        # Check if user input relates to the current topic
        input_relates_to_topic = False
        for token in tokens:
            if token in self.current_topic or (self.current_topic in keywords and any(token in entry[0] for entry in keywords[self.current_topic])):
                input_relates_to_topic = True
                break

        if self.topic_turns > 0: # Only respond if topic_turns > 0
            if self.current_topic in keywords:
                for resp_pattern, resp_text in keywords[self.current_topic]:
                    if matches(tokenize(resp_pattern), tokens):
                        self.dere_context.used_responses.add(resp_text)
                        #self.current_topic = None  # Reset topic after a match
                        #self.topic_dere = None # Reset the dere type
                        #self.topic_turns = 0 # Reset topic turns
                        if self.waifu_chatbot.debug:
                            print(f"TopicManager.respond_based_on_current_topic: Found response: {resp_text}")
                        return resp_text

            # If we have a current_topic, but no specific keyword was found:
            # Call generate_response with the current topic
            if self.waifu_chatbot.debug:
                print(f"TopicManager.respond_based_on_current_topic: No keywords matched, calling generate_response with topic: {self.current_topic}")
            substitutions = {}
            if self.current_topic == "favorite_food":
                substitutions = {"favorite_food": self.waifu_memory.favorite_food}
            response = generate_response(
                self.response_templates, # Pass response_templates
                self.current_topic,  # Use current_topic as keyword
                substitutions,  # Pass substitutions
                self.waifu_chatbot.dere_context.used_responses,
                self.waifu_memory,
                self.waifu_chatbot.dere_context.current_dere, # Use the current dere type
                dere_response,
                self.waifu_chatbot.debug,
                self.waifu_chatbot.response_generator.used_default_responses, # Pass used_default_responses
                self.previous_input # Pass previous input
            )
            if response: # If a topic-specific response was generated
                if self.waifu_chatbot.debug:
                    print(f"TopicManager.respond_based_on_current_topic: Before decrement, topic_turns = {self.topic_turns}")
                if input_relates_to_topic:
                    self.topic_turns -= 1 # Decrement topic_turns
                else:
                    self.topic_turns -= 2  # Decrement faster if user doesn't engage
                    if self.topic_turns < 0:
                        self.topic_turns = 0
                if self.waifu_chatbot.debug:
                    print(f"TopicManager.respond_based_on_current_topic: After decrement, topic_turns = {self.topic_turns}")

                if self.topic_turns == 0:
                    self.current_topic = None  # Reset the topic when turns run out
                    self.topic_dere = None
                self.turns_since_last_topic = 0 # Reset the counter
                self.waifu_chatbot.response_generator.topic_context = False # Reset topic_context


            return response
        else:
            if self.waifu_chatbot.debug:
                print(f"TopicManager.respond_based_on_current_topic: No more topic turns remaining")
            self.current_topic = None # Reset if no current topic
            self.topic_dere = None
            self.turns_since_last_topic = 0 # Reset turns_since_last_topic

    if self.topic_turns <= 0 or not input_relates_to_topic:
        if self.waifu_chatbot.debug:
            print("TopicManager.respond_based_on_current_topic: Exiting topic due to no engagement or turns limit")
        self.current_topic = None
        self.topic_dere = None
        self.turns_since_last_topic = 0

    return None