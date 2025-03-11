from waifu_chatbot import WaifuChatbot
from main_transforms import register_transforms
from main_keywords import register_keywords

def run_interactive_mode(waifu_name: str, debug: bool) -> None:
    """Runs the chatbot in interactive mode."""
    waifu = WaifuChatbot(waifu_name, debug=debug)
    register_keywords(waifu)
    register_transforms(waifu)
    # Interactive conversation loop
    print(f"{waifu.waifu_memory.name}: {waifu.greetings[0]}")

    while True:
        user_input = input("User: ")
        response = waifu.respond(user_input)
        print(f"{waifu.waifu_memory.name}: {response}")

        if response in waifu.farewells:
            break