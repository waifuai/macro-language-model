# waifu_chatbot_response.py
import random
from utils import tokenize
from dere_utils import maybe_change_dere
from dere_data import dere_types


def respond(chatbot, input_str: str) -> str:
    try:  # Added try-except block
        # Attempt to decode with UTF-8, replace errors
        try:
            input_str = input_str.encode('utf-8', 'replace').decode('utf-8')
        except Exception as e:
            print(f"Input encoding error: {e}")
            input_str = "I couldn't quite understand that."


        chatbot.conversation_context.conversation_history.append(("user", input_str))
        chatbot.previous_input = input_str
        chatbot.turn_count += 1
        tokens = tokenize(input_str)

        context = {
            "waifu_memory": chatbot.waifu_memory,
            "debug": chatbot.debug,
            "conversation_context": chatbot.conversation_context,
            "current_dere": chatbot.current_dere,
            "waifu_chatbot": chatbot
        }

        # Use personality to generate response without keyword matching
        response = chatbot.personality.generate_response(tokens, context)

        # Occasionally change dere type for variety
        if random.random() < 0.1:  # 10% chance
            maybe_change_dere_response = maybe_change_dere(chatbot.dere_context, dere_types)
            if maybe_change_dere_response:
                chatbot.current_dere = chatbot.dere_context.current_dere  # Update current_dere
                return maybe_change_dere_response

        # Adjust affection based on interaction
        affection_change = random.randint(-1, 2)
        chatbot.waifu_memory.affection += affection_change
        chatbot.waifu_memory.affection = max(0, min(100, chatbot.waifu_memory.affection))

        # Incorporate memory for relevance, checking for favorite_food first
        if "food" in input_str.lower() and chatbot.waifu_memory.favorite_food:
            response += f" Speaking of food, I really like {chatbot.waifu_memory.favorite_food}!"
        elif "you" in input_str.lower():  # More generic "you" check
            response += f" I’m just happy to chat with you!"

        # Ensure consistent UTF-8 encoding
        response = response.encode('utf-8', 'replace').decode('utf-8')
        return response

    except Exception as e:
        print(f"An error occurred: {e}")
        return "I'm having a bit of trouble right now.  Let's talk later!"  # More robust fallback
