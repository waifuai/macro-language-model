import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential

def is_echoed_response(user_response: str, waifu_response: str) -> bool:
    return user_response.lower().strip() == waifu_response.lower().strip()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def generate_with_retry(model, prompt, previous_waifu_response: str):
    """Generates content using the Gemini model with retry logic."""
    # print(f"Calling generate_content with prompt: {prompt[:100]}...") # Debug
    response = model.generate_content(prompt)

    # Access the text part of the response more robustly
    response_text = ""
    try:
        # Gemini API might return parts, try accessing the first part's text
        if response.parts:
            response_text = response.parts[0].text
        else:
            # Fallback if structure is different or text is directly available
            response_text = response.text
    except (AttributeError, IndexError, ValueError) as e:
        print(f"DEBUG: Error accessing Gemini response text: {e}")
        # Attempt a simpler access if the above fails
        try:
            response_text = response.text
        except AttributeError:
             print(f"DEBUG: Could not access response text at all.")
             raise Exception("Failed to extract text from Gemini response.") from e

    # Simple check for echoed response using the extracted text
    if is_echoed_response(response_text, previous_waifu_response):
        raise Exception("Echoed response detected. Retrying...")

    # Return the extracted text directly, encoding handled later
    return response_text