"""
Command-line interface module for the Waifu Chatbot application.

This module handles all command-line argument parsing and validation for the Waifu
Chatbot system. It provides a user-friendly interface for selecting conversation
modes, configuring waifu personality traits, setting debug options, and choosing
AI providers. The module uses argparse to create a comprehensive CLI with helpful
examples and validation for mutually exclusive mode selection.

Supported features:
- Interactive mode for real-time conversation
- Auto mode for AI vs AI conversation simulation
- Gemini mode for direct AI interaction
- Personality selection (deredere, tsundere, kuudere, yandere, dandere, himedere)
- Debug mode for detailed logging
- Multiple AI provider support (Gemini, OpenRouter)
"""
import argparse
from typing import List

from chat_provider import get_available_providers, get_default_provider

# Personality types available for the waifu
PERSONALITY_CHOICES: List[str] = [
    "deredere", "dandere", "himedere", "kuudere", "tsundere", "yandere"
]


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the Waifu Chatbot.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Waifu Chatbot - AI-powered conversational character",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  %(prog)s --interactive --personality tsundere --waifu_name "Sakura"
  %(prog)s --auto 5 --debug --provider openrouter
  %(prog)s --gemini --waifu_name "Luna" --provider gemini
  %(prog)s --interactive --provider openrouter

Available providers: {', '.join(get_available_providers())}
Default provider: {get_default_provider()}
        """
    )

    # Mode selection (mutually exclusive group)
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--interactive",
        action="store_true",
        help="Enable interactive mode for real-time conversation"
    )
    mode_group.add_argument(
        "--auto",
        nargs="?",
        const=10,
        type=int,
        metavar="TURNS",
        help="Enable automatic conversation mode with optional number of turns (default: 10)"
    )
    mode_group.add_argument(
        "--gemini",
        action="store_true",
        help="Enable direct Gemini mode for simplified interaction"
    )

    # Configuration options
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode with detailed logging"
    )
    parser.add_argument(
        "--waifu_name",
        default="Waifu",
        metavar="NAME",
        help="Set the waifu's name (default: Waifu)"
    )
    parser.add_argument(
        "--personality",
        default="deredere",
        choices=PERSONALITY_CHOICES,
        metavar="TYPE",
        help=f"Set the waifu's personality (choices: {', '.join(PERSONALITY_CHOICES)})"
    )
    parser.add_argument(
        "--provider",
        default=get_default_provider(),
        choices=get_available_providers(),
        metavar="PROVIDER",
        help=f"AI provider for chat generation (choices: {', '.join(get_available_providers())}) (default: {get_default_provider()})"
    )

    return parser.parse_args()