# waifu_chatbot_response.py
import random
from utils import tokenize
from dere_data import dere_types


def respond(chatbot, input_str: str) -> str:
    try:
        # Basic input validation/sanitization
        if not isinstance(input_str, str):
            input_str = str(input_str)
        # Attempt to handle potential encoding issues more simply
        try:
            # Try decoding if it's bytes, otherwise assume it's already a string
            if isinstance(input_str, bytes):
                input_str = input_str.decode('utf-8', 'replace')
        except Exception as e:
            if chatbot.debug:
                print(f"Input decoding error: {e}")
            input_str = "I couldn't quite understand that." # Fallback

        chatbot.conversation_context.conversation_history.append(("user", input_str))
        chatbot.previous_input = input_str
        chatbot.turn_count += 1
        tokens = tokenize(input_str) # Tokenize after potential decoding

        context = {
            "waifu_memory": chatbot.waifu_memory,
            "debug": chatbot.debug,
            "conversation_context": chatbot.conversation_context,
            "current_dere": chatbot.current_dere,
            "waifu_chatbot": chatbot
        }

        # Use personality to generate response
        response = chatbot.personality.generate_response(tokens, context)

        # REMOVED: Occasionally change dere type for variety
        # if random.random() < 0.1:  # 10% chance
        #     maybe_change_dere_response = maybe_change_dere(chatbot.dere_context, dere_types)
        #     if maybe_change_dere_response:
        #         chatbot.current_dere = chatbot.dere_context.current_dere # Update current_dere
        #         # Ensure the response from maybe_change_dere is also encoded correctly
        #         try:
        #             return maybe_change_dere_response.encode('utf-8', 'replace').decode('utf-8')
        #         except Exception as e:
        #              if chatbot.debug:
        #                 print(f"Encoding error in maybe_change_dere response: {e}")
        #              return "Something changed, but I can't quite say what!" # Fallback

        # REMOVED: Adjust affection based on interaction
        # affection_change = random.randint(-1, 2)
        # chatbot.waifu_memory.affection += affection_change
        # chatbot.waifu_memory.affection = max(0, min(100, chatbot.waifu_memory.affection))

        # Removed the repetitive phrase addition

        # Ensure final response is UTF-8
        try:
            response = response.encode('utf-8', 'replace').decode('utf-8')
        except Exception as e:
            if chatbot.debug:
                print(f"Final response encoding error: {e}")
            response = "I'm not sure how to respond to that." # Fallback

        return response

    except Exception as e:
        print(f"An error occurred: {e}")
        return "I'm having a bit of trouble right now.  Let's talk later!"  # More robust fallback
