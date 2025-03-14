from typing import List, Dict, Any, Optional, Set, Tuple, Callable
import random
from personalities.personality_interface import PersonalityInterface
from personalities.deredere.data import deredere_responses
from keyword_handler import handle_keywords
from transformations import apply_transformations


class DeredereLogic(PersonalityInterface):
    def __init__(self, debug: bool = False):
        self.debug = debug

    def generate_response(self, input_tokens: List[str], context: Dict[str, Any]) -> str:
        waifu = context["waifu_chatbot"]

        # Handle keywords
        keyword_response = self.handle_keywords(input_tokens, waifu.registry.keywords, self.debug) # Call the local handle_keywords
        if keyword_response:
            return keyword_response

        # Handle transformations
        transformed_response = self.handle_transformations(waifu.registry.transformations, input_tokens, context["waifu_memory"], context["current_dere"],
            lambda *args: "I like chatting!", self.introduce_topic,
            lambda context, *resps: random.choice(resps or ["..."]), {}, set(), [], self.debug, waifu
        )

        if transformed_response:
            return transformed_response

        # Handle topic-specific responses
        if waifu.current_topic and waifu.topic_turns > 0:
            topic_response = self.handle_topic_response(input_tokens, waifu.current_topic, context)
            if topic_response:
                waifu.topic_turns -= 1
                if waifu.topic_turns == 0:
                    waifu.current_topic = None
                return topic_response

        # Get default response
        return self.get_default_response(context)

    def handle_topic_response(self, input_tokens: List[str], topic: str, context: Dict[str, Any]) -> Optional[str]:
        if topic in deredere_responses:
            responses = deredere_responses[topic]
            unused_responses = [resp for resp in responses if resp not in context["conversation_context"].used_responses]
            if unused_responses:
                response = random.choice(unused_responses)
                context["conversation_context"].used_responses.add(response)
                return response
            else:
                context["conversation_context"].used_responses.clear()
                return random.choice(responses)
        return None

    def get_default_response(self, context: Dict[str, Any]) -> str:
        used = context["conversation_context"].used_responses
        defaults = ["Okay!", "Tell me more!", "That’s fun!", "Sounds good!"]
        unused = [r for r in defaults if r not in used]
        response = random.choice(unused or defaults)
        used.add(response)
        return response

    def introduce_topic(self, topic: str, context: Dict[str, Any]) -> str:
        introductions = {
            "family": "Hey, let’s talk about family! What are yours like?",
            "childhood": "Ooh, childhood stories! What was yours like?",
            "feelings": "How are you feeling today? I’d love to know!",
            "relationship": "So, are you seeing anyone special?",
            "food": "What’s your favorite food? I’m curious!",
            "interest_manga": "I love manga! What are you reading?",
            "interest_anime": "Anime is awesome! What are you watching?",
            "interest_games": "Let's play some games! What are your favorites?",
            "interest_cooking": "I love to cook! What's your favorite dish to make?",
        }
        return introductions.get(topic, f"Let’s chat about {topic}!")

    def get_data(self) -> Dict[str, Any]:
        return {"responses": deredere_responses, "default_responses": ["Okay!", "Tell me more!", "That's fun!", "Sounds good!"]}

    def handle_keywords(self, tokens: List[str], keywords: Dict[str, List[Tuple[str, Any]]], debug: bool) -> Optional[str]:
        """Handles general keywords."""
        return handle_keywords(tokens, keywords, set(), debug)

    def handle_transformations(self, transformations: Dict[str, Tuple[Any, Optional[str], int]], input_list: List[str], waifu_memory: Any, current_dere: str, talk_about_interest: Callable[..., str], introduce_topic: Callable[..., str], dere_response: Callable[..., str], response_templates: Dict[tuple[str, str], List[str]], used_responses: Set[str], dere_types: List[str], debug: bool, waifu_chatbot: Any) -> Optional[str]:
        """Applies transformations to the input and returns a transformed response."""
        return apply_transformations(transformations, input_list, waifu_memory, current_dere, talk_about_interest, introduce_topic, dere_response, response_templates, used_responses, dere_types, debug, waifu_chatbot)

    def maybe_introduce_topic(self, context: Dict[str, Any], input_str: str, turn_count: int) -> Optional[str]:
        return None

    def respond_based_on_current_topic(self, topic_manager: Any, tokens: List[str], keywords: Dict[str, List[Tuple[str, Any]]], context: Dict[str, Any], response_templates: Dict[tuple[str, str], List[str]]) -> Optional[str]:
        return None