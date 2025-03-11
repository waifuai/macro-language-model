import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
from gemini_utils import generate_with_retry

def setup_gemini_api():
    """Sets up the Gemini API key."""
    try:
        with open("../../api.txt", "r") as f:
            api_key = f.read().strip()
    except FileNotFoundError:
        print("Error: api.txt not found in the parent directory.")
        return None
    except Exception as e:
        print(f"Error reading API key from file: {e}")
        return None

    genai.configure(api_key=api_key)
    return genai