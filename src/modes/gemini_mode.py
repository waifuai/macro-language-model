from chat_provider import generate_chat_response, get_default_provider

def run_gemini_mode(waifu_name: str, personality: str, debug: bool, provider: str = None) -> None:
    """Interactive AI-driven Waifu chat using the selected provider."""
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
        greeting = generate_chat_response(
            messages=greeting_messages,
            provider=provider,
            temperature=0.7
        )
        if greeting:
            print(f"{waifu_name}: {greeting}")
        else:
            print("Error: Could not generate greeting.")
            return
    except Exception as e:
        print(f"Error generating greeting: {e}")
        return

    # Conversation loop
    conversation_history = [system_message, {"role": "assistant", "content": greeting}]

    while True:
        user_input = input("User: ")
        if debug:
            print(f"[DEBUG] User input: {user_input}")
        if user_input.lower().strip() in ["exit", "quit"]:
            print("Exiting Gemini mode.")
            break

        # Add user message to history
        conversation_history.append({"role": "user", "content": user_input})

        if debug:
            print(f"[DEBUG] Conversation history: {conversation_history}")

        try:
            response = generate_chat_response(
                messages=conversation_history,
                provider=provider,
                temperature=0.7
            )
            if response:
                print(f"{waifu_name}: {response}")
                conversation_history.append({"role": "assistant", "content": response})
            else:
                print("Error: Could not generate response.")
                break
        except Exception as e:
            print(f"Error generating response: {e}")
            break