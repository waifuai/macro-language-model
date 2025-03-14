from typing import List, Dict, Any, Optional
from .data import deredere_responses
from response_generation import generate_response_from_template
import random
from dere_utils import dere_response

def generate_response(self, input_tokens: List[str], context: Dict[str, Any]) -> str:

    if context["waifu_chatbot"].response_generator.topic_context:
        response = context["waifu_chatbot"].response_generator.generate_topic_response(input_tokens, context)
        if response:
            return response

    transformed_input = ""

    response_template = context["waifu_chatbot"].response_generator.get_response_template(transformed_input, context)

    if response_template:
        # Corrected line: Pass substitutions instead of context
        response = generate_response_from_template(response_template, context["waifu_chatbot"].response_generator.substitutions if hasattr(context["waifu_chatbot"].response_generator, 'substitutions') else {})
    else:
        response = self.get_default_response(context)
    return response