from typing import Optional
from tenacity import retry, stop_after_attempt, wait_exponential

# New SDK import is centralized in genai_client to avoid import scattering
# This module now consumes a client instance and the model name.
def is_echoed_response(user_response: str, waifu_response: str) -> bool:
    return user_response.lower().strip() == waifu_response.lower().strip()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def generate_with_retry(client, model_name: str, prompt: str, previous_waifu_response: str) -> str:
    """
    Generates content using the Google GenAI SDK client with retry logic.

    Args:
        client: genai.Client instance from google.genai.
        model_name: The model to call, e.g., "gemini-2.5-pro".
        prompt: String prompt contents.
        previous_waifu_response: Used to detect echoing.

    Returns:
        The response text content.
    """
    response = client.models.generate_content(model=model_name, contents=prompt)

    # The new SDK exposes `text` convenience when the response is text-based.
    response_text: Optional[str] = None
    try:
        response_text = getattr(response, "text", None)
    except Exception as e:
        print(f"DEBUG: Error accessing response.text: {e}")

    if not response_text:
        # Fallback: attempt parts extraction if present
        try:
            parts = getattr(response, "candidates", None) or getattr(response, "parts", None)
            if parts and hasattr(parts, "__iter__"):
                # Try typical text field of first item
                first = next(iter(parts))
                # Different SDKs may differ; try common attributes
                for attr in ("text", "content", "output_text"):
                    if hasattr(first, attr):
                        response_text = getattr(first, attr)
                        break
        except Exception as e:
            print(f"DEBUG: Could not extract text from response: {e}")

    if not response_text:
        raise Exception("Failed to extract text from GenAI response.")

    if is_echoed_response(response_text, previous_waifu_response):
        raise Exception("Echoed response detected. Retrying...")

    return response_text