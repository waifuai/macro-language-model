from gemini_utils import generate_with_retry
import traceback
import google.generativeai as genai
from modes.common import setup_gemini_api

def run_conversation(waifu, model, max_turns: int, debug: bool):
    greeting = waifu.greetings[0]
    print(f"{waifu.waifu_memory.name}: {greeting}")
    conversation_history = [f"{waifu.waifu_memory.name}: {greeting}"]

    # System instruction for Gemini
    system_instruction = (
        f"You are a human user interacting with a chatbot named {waifu.waifu_memory.name}. "
        f"Generate engaging, natural responses that continue the conversation in a realistic way. "
        f"Be friendly, curious, and show personality. Avoid repeating what {waifu.waifu_memory.name} says."
    )
    for turn in range(max_turns):
        if turn == 0:
            # Generate first user response to greeting
            prompt = (
                f"{system_instruction}\\n\\n"
                f"### Conversation History:\\n"
                f"{conversation_history[0]}\\n"
                f"### Your Task:\\n"
                f"Respond as the user to this greeting in a natural way.\\n"
                f"User: "
            )
        else:
            # Prepare prompt with full history
            history_text = "\\n".join(conversation_history)
            prompt = (
                f"{system_instruction}\\n\\n"
                f"### Conversation History:\\n"
                f"{history_text}\\n"
                f"### Your Task:\\n"
                f"Respond as the user to {waifu.waifu_memory.name}'s last message in a natural way.\\n"
                f"User: "
            )
        try:
            response = generate_with_retry(model, prompt, greeting if turn == 0 else waifu_response)
            if response:
                user_input = response
                # user_input = user_input.encode('utf-8', 'replace').decode('utf-8') # No longer needed
                print(f"User: {user_input}")
                conversation_history.append(f"User: {user_input}")

                waifu_response = waifu.respond(user_input)
                print(f"{waifu.waifu_memory.name}: {waifu_response}")
                conversation_history.append(f"{waifu.waifu_memory.name}: {waifu_response}")
                if waifu_response in waifu.farewells:
                    break
            else:
                print("Waifu: I'm sorry, I'm having trouble understanding. Can you try again?")
                break

        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
            break