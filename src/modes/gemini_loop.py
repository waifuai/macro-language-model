from gemini_utils import generate_with_retry
import traceback

def run_conversation(waifu, model, max_turns: int, debug: bool):
    greeting = waifu.greetings[0]
    print(f"Waifu: {greeting}")
    conversation_history = [f"{waifu.waifu_memory.name}: {greeting}"]

    for turn in range(max_turns):
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        conversation_history.append(f"User: {user_input}")
        prompt = "\\n".join(conversation_history) + "\\nWaifu:"
        try:
            response = generate_with_retry(model, prompt, debug)
            if response:
                print(f"Waifu: {response}")
                conversation_history.append(f"{waifu.waifu_memory.name}: {response}")
            else:
                print("Waifu: I'm sorry, I'm having trouble understanding. Can you try again?")
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
            break