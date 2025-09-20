"""
Common utilities for Gemini conversation modes in the Waifu Chatbot application.

This module provides shared utilities and helper functions for the Gemini-specific
conversation modes, including client initialization, validation, and safe content
generation. It centralizes common functionality used across different conversation
modes to ensure consistency and reduce code duplication.

Key features:
- Gemini API client initialization and validation
- Safe content generation with comprehensive error handling
- Retry configuration management for API calls
- Centralized logging and error reporting
- Client state validation and recovery
- Configuration management for generation parameters

The module serves as a foundation for Gemini-based conversation modes, providing
reliable and consistent access to AI generation capabilities while handling
common edge cases and error scenarios.
"""
import logging
from typing import Optional, Any

from gemini_utils import generate_with_retry
from genai_client import get_client, GEMINI_MODEL

# Configure logging for this module
logger = logging.getLogger(__name__)


def setup_gemini_api() -> Optional[Any]:
    """
    Initialize and return a ready GenAI client instance.

    Returns:
        GenAI client instance if successful, None on failure.

    Note:
        The function handles API key resolution and client initialization,
        preferring environment variables or fallback to ~/.api-gemini file.
    """
    try:
        client = get_client()
        logger.info("GenAI client initialized successfully")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize GenAI client: {e}")
        return None


def validate_client(client: Optional[Any]) -> bool:
    """
    Validate that the client is properly initialized.

    Args:
        client: The client instance to validate.

    Returns:
        True if client is valid, False otherwise.
    """
    if client is None:
        logger.error("Client is None")
        return False
    return True


def safe_generate_content(
    client: Any,
    prompt: str,
    model_name: Optional[str] = None,
    max_retries: int = 3,
    **kwargs
) -> Optional[str]:
    """
    Safely generate content with comprehensive error handling.

    Args:
        client: GenAI client instance.
        prompt: The prompt to send to the model.
        model_name: Model to use (defaults to GEMINI_MODEL).
        max_retries: Maximum number of retry attempts.
        **kwargs: Additional arguments for generation.

    Returns:
        Generated content if successful, None on failure.
    """
    if not validate_client(client):
        return None

    if not prompt or not prompt.strip():
        logger.error("Prompt is empty or None")
        return None

    model = model_name or GEMINI_MODEL
    logger.debug(f"Generating content with model: {model}")

    try:
        # Temporarily adjust retry count
        original_stop = generate_with_retry.retry.stop
        generate_with_retry.retry.stop = generate_with_retry.retry.stop.__class__(max_retries)

        result = generate_with_retry(client, model, prompt, **kwargs)

        # Restore original retry configuration
        generate_with_retry.retry.stop = original_stop

        return result

    except Exception as e:
        logger.error(f"Content generation failed: {e}")
        return None