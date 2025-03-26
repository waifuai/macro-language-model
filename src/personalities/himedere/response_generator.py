from typing import List, Dict, Any, Optional
from keyword_handler import handle_keywords
from response_generation import generate_response_from_template
from keyword_handler import handle_keywords # Keep import for now

def generate_response(self, input_tokens: List[str], context: Dict[str, Any]) -> str:
    # keyword_response = handle_keywords(input_tokens, context["waifu_chatbot"].registry.keywords, context["debug"]) # REMOVED
    # if keyword_response:
    #     return keyword_response

    if context["waifu_chatbot"].response_generator.topic_context:
        response = context["waifu_chatbot"].response_generator.generate_topic_response(input_tokens, context)
        if response:
            return response

    transformed_input = context["waifu_chatbot"].registry.apply_transformations(input_tokens, context)
    response_template = context["waifu_chatbot"].response_generator.get_response_template(transformed_input, context)

    if response_template:
        response = generate_response_from_template(response_template, context)
    else:
        response = self.get_default_response(context)
    return response