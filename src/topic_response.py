import random
from typing import List, Optional, Dict, Any, Tuple
from dere_types import DereContext  # Updated import
from dere_utils import dere_response
from topics import introduce_topic
from conversation_context import ConversationContext
from response_generation import generate_response  # Updated import
import re

def respond_based_on_current_topic(self, tokens: List[str], dere_context: DereContext, response_templates: Dict[tuple[str, str], List[str]]) -> Optional[str]: # Added response_templates argument
    """Responds based on the current topic, if any."""
    if self.current_topic:
        if self.topic_turns > 0:  # Only respond if topic_turns > 0
            substitutions = {}
            if self.current_topic == "favorite_food":
                substitutions = {"favorite_food": self.waifu_memory.favorite_food}
            response = generate_response(
                response_templates,  # Pass response_templates
                self.current_topic,  # Use current_topic as keyword
                substitutions,  # Pass substitutions
                dere_context.used_responses, # Use passed-in dere_context
                self.waifu_memory,
                dere_context.current_dere,  # Use the current dere type
                dere_response,
                self.waifu_chatbot.debug,
                self.waifu_chatbot.response_generator.used_default_responses,  # Pass used_default_responses
                self.previous_input  # Pass previous input
            )
            if response:  # If a topic-specific response was generated
                # Always decrement by 1
                self.topic_turns -= 1

                if self.topic_turns == 0:
                    self.current_topic = None  # Reset the topic when turns run out
                    self.topic_dere = None
                self.turns_since_last_topic = 0  # Reset the counter
                self.waifu_chatbot.response_generator.topic_context = False  # Reset topic_context

            return response
        else:
            self.current_topic = None  # Reset if no current topic
            self.topic_dere = None
            self.turns_since_last_topic = 0  # Reset turns_since_last_topic

    if self.topic_turns <= 0:
        self.current_topic = None
        self.topic_dere = None
        self.turns_since_last_topic = 0

    return None