"""
Google Gemini utility functions for the Waifu Chatbot application.

This module provides utility functions for interacting with the Google Gemini AI
service, including response generation, text extraction, and echo detection. It
includes robust retry logic and comprehensive error handling for reliable AI
interaction.

Key features:
- Google Gemini API integration with retry mechanisms
- Response text extraction with multiple fallback strategies
- Echo response detection to prevent repetitive conversations
- Exponential backoff retry logic for API failures
- Comprehensive error handling and logging
- Configurable generation parameters (temperature, tokens)
- UTF-8 encoding support for international text

The module serves as a critical interface between the application and Google's
Gemini AI service, ensuring reliable and diverse conversational responses while
preventing repetitive or echoed content.
"""
import logging
from typing import Optional, Any
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Configure logging for this module
logger = logging.getLogger(__name__)


def is_echoed_response(user_response: str, waifu_response: str) -> bool:
    """
    Check if the waifu response is echoing the user's previous response.

    Args:
        user_response: The user's input text.
        waifu_response: The waifu's generated response.

    Returns:
        True if the responses are identical (ignoring case and whitespace), False otherwise.
    """
    return user_response.lower().strip() == waifu_response.lower().strip()


def extract_text_from_response(response: Any) -> Optional[str]:
    """
    Extract text content from a GenAI API response with fallback strategies.

    Args:
        response: The response object from the GenAI API.

    Returns:
        Extracted text content or None if extraction fails.
    """
    # Primary method: direct text attribute
    try:
        response_text = getattr(response, "text", None)
        if response_text:
            return str(response_text).strip()
    except Exception as e:
        logger.debug(f"Error accessing response.text: {e}")

    # Fallback 1: Try candidates/parts extraction
    try:
        parts = getattr(response, "candidates", None) or getattr(response, "parts", None)
        if parts and hasattr(parts, "__iter__"):
            first = next(iter(parts), None)
            if first:
                # Try common text attribute names
                for attr in ("text", "content", "output_text"):
                    if hasattr(first, attr):
                        text_content = getattr(first, attr)
                        if text_content:
                            return str(text_content).strip()
    except Exception as e:
        logger.debug(f"Could not extract text from response parts: {e}")

    # Fallback 2: Try to convert response directly to string
    try:
        response_str = str(response).strip()
        if response_str and response_str != str(type(response)):
            return response_str
    except Exception as e:
        logger.debug(f"Could not convert response to string: {e}")

    return None


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((Exception,)),
    reraise=True
)
def generate_with_retry(
    client: Any,
    model_name: str,
    prompt: str,
    previous_waifu_response: str = "",
    max_tokens: Optional[int] = None,
    temperature: float = 0.7
) -> str:
    """
    Generate content using the Google GenAI SDK client with retry logic.

    Args:
        client: GenAI client instance from google.genai.
        model_name: The model to call, e.g., "gemini-2.5-pro".
        prompt: String prompt contents.
        previous_waifu_response: Used to detect echoing (default: empty string).
        max_tokens: Maximum tokens to generate (optional).
        temperature: Sampling temperature (default: 0.7).

    Returns:
        The response text content.

    Raises:
        Exception: If text extraction fails or echoed response is detected.
    """
    logger.debug(f"Generating content with model: {model_name}")

    # Prepare generation config
    generation_config = {}
    if max_tokens:
        generation_config["max_output_tokens"] = max_tokens
    if temperature != 0.7:
        generation_config["temperature"] = temperature

    try:
        if generation_config:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=generation_config
            )
        else:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
    except Exception as e:
        logger.error(f"API call failed: {e}")
        raise

    # Extract text from response
    response_text = extract_text_from_response(response)

    if not response_text:
        logger.error("Failed to extract text from GenAI response")
        raise Exception("Failed to extract text from GenAI response.")

    # Check for echoed response if previous response is provided
    if previous_waifu_response and is_echoed_response(response_text, previous_waifu_response):
        logger.warning("Echoed response detected, will retry")
        raise Exception("Echoed response detected. Retrying...")

    logger.debug(f"Generated response: {response_text[:100]}...")
    return response_text