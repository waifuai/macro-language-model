import win_unicode_console
win_unicode_console.enable()

from waifu_chatbot import WaifuChatbot
from typing import Optional, Dict, List, Tuple
import os
from cli import parse_arguments
from modes.auto_mode import run_auto_mode
from modes.gemini_mode import run_gemini_mode
from modes.interactive_mode import run_interactive_mode


def main() -> None:
    """Main function to run the Waifu Chatbot."""
    args = parse_arguments()
    if args.debug:  # Only print if debug is true
        print(f"Parsed arguments: {args}")
        print("Starting up...")

    if args.interactive:
        run_interactive_mode(args.waifu_name, args.debug)

    elif args.auto is not None:
        run_auto_mode(args.waifu_name, args.debug, args.auto)

    elif args.gemini:
        run_gemini_mode(args.waifu_name, args.debug)

if __name__ == "__main__":
    main()