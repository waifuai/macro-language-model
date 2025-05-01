import google.generativeai as genai
from gemini_utils import generate_with_retry
from modes.common import setup_gemini_api

def run_auto_mode(waifu_name: str, personality: str, debug: bool, max_turns: int = 10) -> None:
    """Simulates a conversation for `max_turns` turns with Gemini as both waifu and user."""
    genai_instance = setup_gemini_api()
    if not genai_instance:
        return
    model = genai_instance.GenerativeModel(
        "gemini-2.5-pro-preview-03-25",
        generation_config={"temperature": 0.9, "top_p": 0.95}
    )
    system_prompt = (
        f"You are {waifu_name}, a {personality} waifu. Respond in character with emotion and style appropriate to your personality."
    )
    # Generate initial greeting
    greeting_prompt = system_prompt + "\n\n### Task: Generate an opening greeting as the waifu.\n"
    try:
        waifu_response = generate_with_retry(model, greeting_prompt, "")
        print(f"{waifu_name}: {waifu_response}")
    except Exception as e:
        print(f"Error generating greeting: {e}")
        return
    conversation_history = [f"{waifu_name}: {waifu_response}"]
    user_input = ""
    for turn in range(max_turns):
        # User (Gemini) turn
        user_prompt = (
            f"You are a human user talking to a waifu named {waifu_name}.\n"
            f"### Conversation so far:\n"
            + "\n".join(conversation_history) +
            "\n### Task: Respond as the user, naturally and briefly.\nUser: "
        )
        try:
            user_input = generate_with_retry(model, user_prompt, waifu_response)
            print(f"User: {user_input}")
        except Exception as e:
            print(f"Error generating user input: {e}")
            break
        conversation_history.append(f"User: {user_input}")
        # Waifu (Gemini) turn
        waifu_prompt = (
            system_prompt +
            "\n\n### Conversation so far:\n" +
            "\n".join(conversation_history) +
            f"\n{waifu_name}:"
        )
        try:
            waifu_response = generate_with_retry(model, waifu_prompt, user_input)
            print(f"{waifu_name}: {waifu_response}")
        except Exception as e:
            print(f"Error generating waifu response: {e}")
            break
        conversation_history.append(f"{waifu_name}: {waifu_response}")
        # Optionally, break if a farewell is detected (not implemented in stub)