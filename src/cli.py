import argparse

def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Waifu Chatbot")
    parser.add_argument("--interactive", action="store_true", help="Enable interactive mode")
    parser.add_argument("--auto", nargs="?", const=10, type=int, default=None, help="Enable automatic conversation mode with optional number of turns")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--waifu_name", default="Waifu", help="Set the waifu's name")
    parser.add_argument("--gemini", action="store_true", help="Enable Gemini mode")
    parser.add_argument("--personality", default="deredere", choices=["deredere", "dandere", "himedere", "kuudere", "tsundere", "yandere", "dynamic"], help="Set the waifu's personality")
    args = parser.parse_args()
    return args