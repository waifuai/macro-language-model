from typing import List, Dict, Any, Optional
from .data import deredere_responses
from keyword_handler import handle_keywords
from response_generation import generate_response_from_template
import random
from transformations import apply_transformations
from dere_utils import dere_response

def generate_response(self, input_tokens: List[str], context: Dict[str, Any]) -> str:
    keyword_response = handle_keywords(input_tokens, context["waifu_chatbot"].registry.keywords, context["waifu_chatbot"].conversation_context.used_responses, context["debug"])
    if keyword_response:
        return keyword_response

    if context["waifu_chatbot"].response_generator.topic_context:
        response = context["waifu_chatbot"].response_generator.generate_topic_response(input_tokens, context)
        if response:
            return response

    transformed_input = apply_transformations(
        context["waifu_chatbot"].registry.transformations,
        input_tokens,
        context["waifu_memory"],
        context["current_dere"],
        context["waifu_chatbot"].personality.talk_about_interest,
        context["waifu_chatbot"].personality.introduce_topic,
        dere_response,
        context["waifu_chatbot"].response_generator.response_templates,
        context["waifu_chatbot"].conversation_context.used_responses,
        context["waifu_chatbot"].personality.get_data().get("dere_types", []),
        context["debug"],
        context["waifu_chatbot"]
    )

    response_template = context["waifu_chatbot"].response_generator.get_response_template(transformed_input, context)

    if response_template:
        # Corrected line: Pass substitutions instead of context
        response = generate_response_from_template(response_template, context["waifu_chatbot"].response_generator.substitutions if hasattr(context["waifu_chatbot"].response_generator, 'substitutions') else {})
    else:
        response = self.get_default_response(context)
    return response