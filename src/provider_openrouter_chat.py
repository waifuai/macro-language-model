"""
OpenRouter chat generation provider for the Waifu Chatbot application.

This module implements chat completion functionality using the OpenRouter API,
providing an alternative AI provider for conversational interactions. It includes
robust retry logic, echo detection, and comprehensive error handling to ensure
reliable chat generation capabilities.

Key features:
- OpenRouter API integration for chat completions
- Exponential backoff retry logic with configurable attempts
- Echo response detection and prevention
- Message history support for context preservation
- Configurable temperature and token limits
- API key resolution from environment variables or files
- Comprehensive error handling and logging
- Response validation and text extraction

The module serves as a critical component for providing diverse AI responses
and maintaining conversation quality through intelligent retry mechanisms and
echo prevention strategies.
"""
import logging
from typing import Optional, Dict, Any, List
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

import requests
from config import get_api_key, get_model

# Configure logging for this module
logger = logging.getLogger(__name__)

# OpenRouter API configuration
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_OPENROUTER_CHAT_MODEL = "deepseek/deepseek-chat-v3-0324:free"


def _resolve_default_openrouter_chat_model() -> str:
    """
    Resolve the default OpenRouter chat model using the centralized configuration system.

    Returns:
        Model name to use for OpenRouter API calls.
    """
    return get_model('openrouter_chat')


def _resolve_openrouter_api_key() -> Optional[str]:
    """
    Resolve the OpenRouter API key using the centralized configuration system.

    Returns:
        API key string if found, None otherwise.
    """
    return get_api_key('openrouter')


def _build_chat_payload(
    messages: List[Dict[str, str]],
    model_name: str,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None
) -> Dict[str, Any]:
    """
    Build the request payload for OpenRouter chat API.

    Args:
        messages: List of message dictionaries with 'role' and 'content'.
        model_name: Model to use for chat generation.
        temperature: Sampling temperature.
        max_tokens: Maximum tokens to generate.

    Returns:
        Dictionary containing the API request payload.
    """
    payload = {
        "model": model_name,
        "messages": messages,
        "temperature": temperature,
    }

    if max_tokens:
        payload["max_tokens"] = max_tokens

    return payload


def _extract_text_from_openrouter_response(response_data: Dict[str, Any]) -> Optional[str]:
    """
    Extract text content from OpenRouter API response.

    Args:
        response_data: The JSON response from OpenRouter API.

    Returns:
        Extracted text content or None if extraction fails.
    """
    try:
        choices = response_data.get("choices", [])
        if not choices:
            logger.warning("No choices in OpenRouter response")
            return None

        content = choices[0].get("message", {}).get("content", "").strip()
        if not content:
            logger.warning("Empty content in OpenRouter response")
            return None

        return content

    except Exception as e:
        logger.error(f"Error extracting text from OpenRouter response: {e}")
        return None


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((Exception,)),
    reraise=True
)
def generate_chat_with_openrouter(
    messages: List[Dict[str, str]],
    model_name: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    timeout: int = 60,
) -> str:
    """
    Generate chat response using OpenRouter API with retry logic.

    Args:
        messages: List of message dictionaries with 'role' and 'content'.
        model_name: Model to use. If None, uses the default model.
        temperature: Sampling temperature (default: 0.7).
        max_tokens: Maximum tokens to generate (optional).
        timeout: Request timeout in seconds (default: 60).

    Returns:
        The response text content.

    Raises:
        Exception: If API call fails or text extraction fails.
    """
    # Resolve API key
    api_key = _resolve_openrouter_api_key()
    if not api_key:
        logger.error("No OpenRouter API key available")
        raise Exception("No OpenRouter API key available")

    # Use default model if not specified
    if model_name is None:
        model_name = _resolve_default_openrouter_chat_model()

    # Build request payload
    payload = _build_chat_payload(messages, model_name, temperature, max_tokens)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Waifu-Chatbot/1.0",
    }

    logger.debug(f"Calling OpenRouter chat API with model: {model_name}")

    try:
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=timeout
        )

        # Handle HTTP errors
        if response.status_code != 200:
            logger.warning(f"OpenRouter API returned status {response.status_code}: {response.text}")
            raise Exception(f"OpenRouter API error: {response.status_code}")

        # Parse JSON response
        try:
            data = response.json()
        except ValueError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise Exception(f"Failed to parse OpenRouter response: {e}")

        # Extract content from response
        content = _extract_text_from_openrouter_response(data)
        if not content:
            logger.error("Failed to extract text from OpenRouter response")
            raise Exception("Failed to extract text from OpenRouter response")

        logger.debug(f"Generated chat response: {content[:100]}...")
        return content

    except requests.exceptions.Timeout:
        logger.error("OpenRouter API request timed out")
        raise Exception("OpenRouter API request timed out")
    except requests.exceptions.RequestException as e:
        logger.error(f"OpenRouter API request failed: {e}")
        raise Exception(f"OpenRouter API request failed: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in OpenRouter chat generation: {e}")
        raise


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


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((Exception,)),
    reraise=True
)
def generate_with_retry(
    messages: List[Dict[str, str]],
    model_name: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    previous_waifu_response: str = "",
) -> str:
    """
    Generate content using OpenRouter with retry logic, compatible with Gemini interface.

    Args:
        messages: List of message dictionaries with 'role' and 'content'.
        model_name: The model to call.
        temperature: Sampling temperature (default: 0.7).
        max_tokens: Maximum tokens to generate (optional).
        previous_waifu_response: Used to detect echoing (default: empty string).

    Returns:
        The response text content.

    Raises:
        Exception: If text extraction fails or echoed response is detected.
    """
    logger.debug(f"Generating content with OpenRouter model: {model_name or _resolve_default_openrouter_chat_model()}")

    # Generate response
    response_text = generate_chat_with_openrouter(
        messages=messages,
        model_name=model_name,
        temperature=temperature,
        max_tokens=max_tokens
    )

    # Check for echoed response if previous response is provided
    if previous_waifu_response and is_echoed_response(response_text, previous_waifu_response):
        logger.warning("Echoed response detected, will retry")
        raise Exception("Echoed response detected. Retrying...")

    return response_text