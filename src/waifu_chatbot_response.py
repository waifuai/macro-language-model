import random
from utils import tokenize
from dere_utils import maybe_change_dere
from dere_data import dere_types

def respond(chatbot, input_str: str) -> str:
    chatbot.conversation_context.conversation_history.append(("user", input_str))
    chatbot.previous_input = input_str
    chatbot.turn_count += 1
    tokens = tokenize(input_str)
    # if chatbot.debug:
    #     print(f"Input: {input_str}, Current Dere: {chatbot.current_dere}, Turn: {chatbot.turn_count}")

    # Dere switching (commented out as in original)
    # maybe_change_dere_response = maybe_change_dere(chatbot.dere_context, dere_types)
    # if maybe_change_dere_response:
    #     chatbot.turns_in_same_dere = 0
    #     return maybe_change_dere_response
    # chatbot.turns_in_same_dere += 1

    context = {
        "waifu_memory": chatbot.waifu_memory,
        "debug": chatbot.debug,
        "conversation_context": chatbot.conversation_context,
        "current_dere": chatbot.current_dere,
        "waifu_chatbot": chatbot
    }
    response = chatbot.personality.generate_response(tokens, context)
    affection_change = random.randint(-1, 2)
    chatbot.waifu_memory.affection += affection_change
    chatbot.waifu_memory.affection = max(0, min(100, chatbot.waifu_memory.affection))
    # if chatbot.debug:
    #    print(f"Response: {response}, Affection change: {affection_change}, New affection: {chatbot.waifu_memory.affection}")
    response = response.encode('utf-8', 'replace').decode('utf-8')
    return response