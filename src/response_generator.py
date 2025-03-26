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

    # Removed _handle_transformations and _select_response methods

    def generate(self, input_str: str, tokens: List[str]) -> str:
        """Generates a response by delegating to the current personality."""
        if self.debug:
             print(f"ResponseGenerator.generate: Delegating to personality: {type(self.waifu_chatbot.personality).__name__}")

        # Prepare context for the personality
        context = {
            "waifu_memory": self.waifu_memory,
            "debug": self.debug,
            "conversation_context": self.waifu_chatbot.conversation_context, # Pass full context if needed
            "current_dere": self.waifu_chatbot.current_dere,
            "waifu_chatbot": self.waifu_chatbot, # Give personality access to the main chatbot object
            "response_templates": self.response_templates, # Pass templates if personality needs them
            "used_default_responses": self.used_default_responses, # Pass used responses set
            # Add other relevant state if needed by personalities
        }

        # Delegate response generation to the personality logic
        response = self.waifu_chatbot.personality.generate_response(tokens, context)

        # Ensure final response is UTF-8 (personalities should ideally handle this, but safety net)
        try:
            response = str(response).encode('utf-8', 'replace').decode('utf-8')
        except Exception as e:
            if self.debug:
                print(f"ResponseGenerator.generate: Final response encoding error: {e}")
            response = "I'm not sure how to respond to that." # Fallback

        return response

    # Removed the other generate method and get_response_template
    # get_response_template might be needed if personalities use it, but simplifying for now.
