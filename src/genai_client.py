"""
OpenRouter API client management for the Waifu Chatbot application.

This module handles the initialization and management of OpenRouter API client
instances, providing a centralized interface for API key resolution and client
configuration. It supports multiple methods for API key provision and includes
comprehensive error handling for client initialization failures.

Key features:
- Centralized API key resolution from environment variables or files
- OpenRouter API client with retry logic
- Response text extraction with multiple fallback strategies
- Echo response detection to prevent repetitive conversations
- Exponential backoff retry logic for API failures
- Comprehensive error handling and logging
- Configurable generation parameters (temperature, tokens)
- UTF-8 encoding support for international text

The module serves as the primary interface between the application and OpenRouter's
LLM service, ensuring secure and reliable API access while providing
clear error messages for configuration issues.
"""
import logging
import os
import requests
from pathlib import Path
from typing import Optional, Any, Dict

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from config import get_api_key, get_model

# Configure logging for this module
logger = logging.getLogger(__name__)

BASE_URL = "https://openrouter.ai/api/v1"


def _resolve_openrouter_model() -> str:
    """
    Resolve the OpenRouter model to use using the centralized configuration system.

    Returns:
        Model name to use for OpenRouter API calls.
    """
    return get_model('openrouter')


def resolve_api_key() -> Optional[str]:
    """
    Resolve the API key using the centralized configuration system.

    Returns:
        API key string if found, None otherwise.
    """
    return get_api_key('openrouter')


def get_client(api_key: Optional[str] = None) -> dict:
    """
    Build and return an OpenRouter client configuration dict.

    Args:
        api_key: Optional API key. If not provided, will resolve automatically.

    Returns:
        Dict with 'api_key' and 'headers' for making OpenRouter API calls.

    Raises:
        RuntimeError: If no API key can be resolved.
    """
    # Resolve API key if not provided
    if not api_key:
        api_key = resolve_api_key()

    if not api_key:
        raise RuntimeError(
            "No API key found. Set OPENROUTER_API_KEY environment variable "
            "or create ~/.api-openrouter file with your API key."
        )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://waifuai.com",
        "X-Title": "Waifu AI"
    }

    logger.info("Successfully initialized OpenRouter client")
    return {"api_key": api_key, "headers": headers}


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
    client: Any,
    model_name: str,
    prompt: str,
    previous_waifu_response: str = "",
    max_tokens: Optional[int] = None,
    temperature: float = 0.7
) -> str:
    """
    Generate content using the OpenRouter API with retry logic.

    Args:
        client: Client dict from get_client() with 'api_key' and 'headers'.
        model_name: The model to call, e.g., "openrouter/free".
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

    if not client or "headers" not in client:
        raise RuntimeError("Invalid client. Call get_client() first.")

    payload: Dict[str, Any] = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature
    }
    if max_tokens:
        payload["max_tokens"] = max_tokens

    url = f"{BASE_URL}/chat/completions"

    try:
        response = requests.post(
            url,
            headers=client["headers"],
            json=payload,
            timeout=120
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            raise RuntimeError("Invalid OpenRouter API key")
        elif e.response.status_code == 429:
            raise RuntimeError("Rate limit exceeded. Retrying...")
        elif e.response.status_code >= 500:
            raise RuntimeError(f"Server error {e.response.status_code}. Retrying...")
        else:
            raise RuntimeError(f"API error: {e}")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request failed: {e}. Retrying...")

    data = response.json()

    # Extract text from response
    response_text = None
    try:
        choices = data.get("choices", [])
        if choices:
            response_text = choices[0].get("message", {}).get("content", "").strip()
    except Exception as e:
        logger.debug(f"Error extracting text from response: {e}")

    if not response_text:
        logger.error("Failed to extract text from OpenRouter response")
        raise Exception("Failed to extract text from OpenRouter response.")

    # Check for echoed response if previous response is provided
    if previous_waifu_response and is_echoed_response(response_text, previous_waifu_response):
        logger.warning("Echoed response detected, will retry")
        raise Exception("Echoed response detected. Retrying...")

    logger.debug(f"Generated response: {response_text[:100]}...")
    return response_text


# Module-level model constant
OPENROUTER_MODEL = _resolve_openrouter_model()
