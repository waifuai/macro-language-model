from waifu_chatbot import WaifuChatbot
import argparse
from main_transforms import register_transforms
from main_keywords import register_keywords
from waifu_chatbot import WaifuChatbot
from typing import Optional

def main() -> None:
    """Main function to run the Waifu Chatbot."""
    parser = argparse.ArgumentParser(description="Waifu Chatbot")
    parser.add_argument("--interactive", action="store_true", help="Enable interactive mode")
    parser.add_argument("--auto", nargs="?", const=10, type=int, default=10, help="Enable automatic conversation mode with optional number of turns")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--waifu_name", default="Waifu", help="Set the waifu's name")
    args = parser.parse_args()

    print("Starting up...")
    waifu = WaifuChatbot(args.waifu_name, debug=args.debug)

    register_keywords(waifu)
    register_transforms(waifu)

    if args.interactive:
        # Interactive conversation loop
        print(f"{waifu.waifu_memory.name}: {waifu.greetings[0]}")

        while True:
            user_input = input("User: ")
            response = waifu.respond(user_input)
            print(f"{waifu.waifu_memory.name}: {response}")

            if response in waifu.farewells:
                break

    elif args.auto is not None:
        # Automatic conversation loop
        max_turns = args.auto
        user_input = waifu.greetings[0]

        if args.debug:
            # Self-conversation loop for debugging
            max_turns = 10
            user_input = waifu.greetings[0]
    
            for _ in range(max_turns):
                print(f"User: {user_input}")
                response = waifu.respond(user_input)
                print(f"{waifu.waifu_memory.name}: {response}")
                print()
    
                if response in waifu.farewells:
                    break
    
                user_input = response
        else:
            # Automatic conversation loop
            max_turns = args.auto
            user_input = waifu.greetings[0]
    
            for _ in range(max_turns):
                print(f"User: {user_input}")
                response = waifu.respond(user_input)
                print(f"{waifu.waifu_memory.name}: {response}")
                print()
    
                if response in waifu.farewells:
                    break
    
                user_input = response

if __name__ == "__main__":
    main()
