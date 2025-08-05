from gemini_utils import generate_with_retry

# New client wrapper centralizes auth and model selection
from genai_client import get_client, GEMINI_MODEL

def setup_gemini_api():
    """
    Returns a ready genai.Client instance or None on failure.
    Prefers env GEMINI_API_KEY or GOOGLE_API_KEY, falls back to ~/.api-gemini.
    """
    try:
        client = get_client()
        return client
    except Exception as e:
        print(f"Error initializing GenAI client: {e}")
        return None