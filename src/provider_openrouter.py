import logging
import os
from pathlib import Path
from typing import Optional, Dict, Any

import requests
from config import get_api_key, get_model

# Configure logging for this module
logger = logging.getLogger(__name__)

# OpenRouter API configuration
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_OPENROUTER_MODEL = "deepseek/deepseek-chat-v3-0324:free"
OPENROUTER_API_KEY_FILE_PATH = Path.home() / ".api-openrouter"


def _read_text_file(path: Path) -> Optional[str]:
    """
    Read and return the content of a text file, handling errors gracefully.

    Args:
        path: Path to the file to read.

    Returns:
        File content as string if successful and non-empty, None otherwise.
    """
    try:
        if path.is_file():
            content = path.read_text(encoding="utf-8").strip()
            return content or None
    except Exception as e:
        logger.debug(f"Error reading text file {path}: {e}")
    return None


def _resolve_default_openrouter_model() -> str:
    """
    Resolve the default OpenRouter model using the centralized configuration system.

    Returns:
        Model name to use for OpenRouter API calls.
    """
    return get_model('openrouter')


def _resolve_openrouter_api_key() -> Optional[str]:
    """
    Resolve the OpenRouter API key using the centralized configuration system.

    Returns:
        API key string if found, None otherwise.
    """
    return get_api_key('openrouter')


def _classification_prompt(text: str) -> str:
    """
    Generate a deterministic prompt for classifying text as human or machine-written.

    Args:
        text: The text to classify.

    Returns:
        Formatted classification prompt.
    """
    return (
        "Classify the following sentence as human-written or machine-generated.\n\n"
        "Categories:\n"
        "- '1': Human-written\n"
        "- '0': Machine-generated\n\n"
        "Respond with ONLY the digit '0' or '1'. Do not include any other text.\n\n"
        f"Sentence: \"{text}\"\n\n"
        "Classification:"
    )


def _build_payload(text: str, model_name: str) -> Dict[str, Any]:
    """
    Build the request payload for OpenRouter API.

    Args:
        text: Text to classify.
        model_name: Model to use for classification.

    Returns:
        Dictionary containing the API request payload.
    """
    return {
        "model": model_name,
        "messages": [{"role": "user", "content": _classification_prompt(text)}],
        "temperature": 0.0,  # Use deterministic output
        "max_tokens": 10,    # Minimal tokens needed for single digit response
    }


def classify_with_openrouter(
    text: str,
    model_name: Optional[str] = None,
    timeout: int = 60,
) -> Optional[str]:
    """
    Classify text as human-written (1) or machine-generated (0) using OpenRouter.

    Args:
        text: The text to classify.
        model_name: Model to use. If None, uses the default model.
        timeout: Request timeout in seconds.

    Returns:
        "0" if machine-generated, "1" if human-written, None on error.
    """
    # Resolve API key
    api_key = _resolve_openrouter_api_key()
    if not api_key:
        logger.warning("No OpenRouter API key available")
        return None

    # Use default model if not specified
    if model_name is None:
        model_name = _resolve_default_openrouter_model()

    # Build request payload
    payload = _build_payload(text, model_name)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Waifu-Chatbot/1.0",
    }

    logger.debug(f"Calling OpenRouter API with model: {model_name}")

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
            return None

        # Parse JSON response
        try:
            data = response.json()
        except ValueError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return None

        # Extract content from response
        choices = data.get("choices", [])
        if not choices:
            logger.warning("No choices in OpenRouter response")
            return None

        content = (choices[0].get("message", {}).get("content") or "").strip()
        if not content:
            logger.warning("Empty content in OpenRouter response")
            return None

        # Strict normalization to expected values
        if content in ("0", "1"):
            logger.debug(f"Classification result: {content}")
            return content

        # Cautious fallback heuristics
        contains0 = "0" in content
        contains1 = "1" in content
        if contains0 and not contains1:
            logger.debug("Using heuristic: contains '0' but not '1' -> 0")
            return "0"
        if contains1 and not contains0:
            logger.debug("Using heuristic: contains '1' but not '0' -> 1")
            return "1"

        logger.warning(f"Unexpected content in response: {content}")
        return None

    except requests.exceptions.Timeout:
        logger.error("OpenRouter API request timed out")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"OpenRouter API request failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in OpenRouter classification: {e}")
        return None