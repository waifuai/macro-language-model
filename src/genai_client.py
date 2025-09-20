import logging
import os
from pathlib import Path
from typing import Optional

from config import get_api_key, get_model, DEFAULT_GEMINI_MODEL

# Configure logging for this module
logger = logging.getLogger(__name__)


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
        logger.warning(f"Error reading text file {path}: {e}")
    return None


def _resolve_gemini_model() -> str:
    """
    Resolve the Gemini model to use using the centralized configuration system.

    Returns:
        Model name to use for Gemini API calls.
    """
    return get_model('gemini')


def resolve_api_key() -> Optional[str]:
    """
    Resolve the API key using the centralized configuration system.

    Returns:
        API key string if found, None otherwise.
    """
    return get_api_key('gemini')


def get_client(api_key: Optional[str] = None) -> 'genai.Client':
    """
    Build and return a Google GenAI client instance.

    Args:
        api_key: Optional API key. If not provided, will resolve automatically.

    Returns:
        Configured genai.Client instance.

    Raises:
        RuntimeError: If no API key can be resolved.
        ImportError: If google-genai package is not installed.
    """
    # Lazy import to avoid top-level hard dependency
    try:
        from google import genai
    except ImportError as e:
        logger.error("google-genai package not installed")
        raise ImportError("google-genai package is required. Install with: pip install google-genai") from e

    # Resolve API key if not provided
    if not api_key:
        api_key = resolve_api_key()

    if not api_key:
        raise RuntimeError(
            "No API key found. Set GEMINI_API_KEY/GOOGLE_API_KEY environment variables "
            "or create ~/.api-gemini file with your API key."
        )

    try:
        client = genai.Client(api_key=api_key)
        logger.info("Successfully initialized GenAI client")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize GenAI client: {e}")
        raise


# Module-level model constant
GEMINI_MODEL = _resolve_gemini_model()