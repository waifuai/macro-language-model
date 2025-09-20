from chat_provider import generate_chat_response, get_default_provider

def run_auto_mode(waifu_name: str, personality: str, debug: bool, max_turns: int = 10, provider: str = None) -> None:
    """Simulates a conversation for `max_turns` turns with the selected provider as both waifu and user."""
    if provider is None:
        provider = get_default_provider()

    system_message = {
        "role": "system",
        "content": (
            f"You are {waifu_name}, a {personality} waifu. "
            "Respond in character with emotion and style appropriate to your personality."
        )
    }

    # Generate initial greeting
    greeting_messages = [
        system_message,
        {"role": "user", "content": "### Task: Generate an opening greeting as the waifu."}
    ]

    try:
        waifu_response = generate_chat_response(
            messages=greeting_messages,
            provider=provider,
            temperature=0.7
        )
        if waifu_response:
            print(f"{waifu_name}: {waifu_response}")
        else:
            print("Error: Could not generate greeting.")
            return
    except Exception as e:
        print(f"Error generating greeting: {e}")
        return

    conversation_history = [system_message, {"role": "assistant", "content": waifu_response}]
    user_input = ""

    for turn in range(max_turns):
        # User (AI) turn
        user_system_message = {
            "role": "system",
            "content": f"You are a human user talking to a waifu named {waifu_name}."
        }

        user_messages = [
            user_system_message,
            {"role": "user", "content": f"### Task: Respond as the user, naturally and briefly. The waifu said: {waifu_response}"}
        ]

        try:
            user_input = generate_chat_response(
                messages=user_messages,
                provider=provider,
                temperature=0.7
            )
            if user_input:
                print(f"User: {user_input}")
                conversation_history.append({"role": "user", "content": user_input})
            else:
                print("Error: Could not generate user input.")
                break
        except Exception as e:
            print(f"Error generating user input: {e}")
            break

        # Waifu (AI) turn
        try:
            waifu_response = generate_chat_response(
                messages=conversation_history,
                provider=provider,
                temperature=0.7,
                previous_waifu_response=user_input
            )
            if waifu_response:
                print(f"{waifu_name}: {waifu_response}")
                conversation_history.append({"role": "assistant", "content": waifu_response})
            else:
                print("Error: Could not generate waifu response.")
                break
        except Exception as e:
            print(f"Error generating waifu response: {e}")
            break
        # Optionally, break if a farewell is detected (not implemented)