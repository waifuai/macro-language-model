import sys
import os
from typing import Optional

# Handle Windows console encoding
try:
    import win_unicode_console
    win_unicode_console.enable()
except ImportError:
    # Gracefully handle missing dependency on non-Windows systems
    pass

from cli import parse_arguments
from modes.auto_mode import run_auto_mode
from modes.gemini_mode import run_gemini_mode
from modes.interactive_mode import run_interactive_mode


def main() -> None:
    """
    Main entry point for the Waifu Chatbot application.

    Parses command-line arguments and delegates to the appropriate mode handler.
    """
    args = parse_arguments()

    if args.debug:
        print(f"DEBUG: Parsed arguments: {args}")
        print("DEBUG: Starting up...")

    try:
        if args.interactive:
            run_interactive_mode(args.waifu_name, args.personality, args.debug, args.provider)
        elif args.auto is not None:
            run_auto_mode(args.waifu_name, args.personality, args.debug, args.auto, args.provider)
        elif args.gemini:
            run_gemini_mode(args.waifu_name, args.personality, args.debug, args.provider)
        else:
            print("ERROR: No mode selected. Use --interactive, --auto, or --gemini.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nINFO: Application interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()