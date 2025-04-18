import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
from gemini_utils import generate_with_retry

def setup_gemini_api():
    """Sets up the Gemini API key."""
    import os
    try:
        api_path = os.path.expanduser("~/.api-gemini")
        with open(api_path, "r") as f:
            api_key = f.read().strip()
    except FileNotFoundError:
        print(f"Error: ~/.api-gemini not found (looked for {api_path}).")
        return None
    except Exception as e:
        print(f"Error reading API key from {api_path}: {e}")
        return None

    genai.configure(api_key=api_key)
    return genai