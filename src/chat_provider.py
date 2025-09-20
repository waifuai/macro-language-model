"""
Provider-agnostic chat generation interface for the Waifu Chatbot application.

This module serves as the central facade for AI chat generation, providing a unified
interface for multiple AI providers while abstracting away the implementation details
of each provider. It currently supports Google Gemini and OpenRouter APIs.

Key features:
- Unified interface for multiple AI providers
- Automatic provider routing based on configuration
- Message format conversion for provider compatibility
- Comprehensive error handling and logging
- Provider fallback and switching capabilities
- Temperature and token limit configuration
- Echo detection and prevention mechanisms

The module acts as a bridge between the conversation modes and the underlying AI
services, ensuring consistent behavior across different providers while allowing
for easy addition of new AI services in the future.
"""
from typing import Optional, List, Dict, Any

from gemini_utils import generate_with_retry as generate_with_gemini
from provider_openrouter_chat import generate_with_retry as generate_with_openrouter


def generate_chat_response(
    messages: List[Dict[str, str]],
    provider: str = "gemini",
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    previous_waifu_response: str = "",
) -> Optional[str]:
    """
    Provider-agnostic facade for chat generation.
    Currently supports:
      - provider="gemini" using Google Gemini API
      - provider="openrouter" using OpenRouter API

    Args:
        messages: List of message dictionaries with 'role' and 'content'.
        provider: The provider to use ("gemini" or "openrouter").
        model: Model name to use (optional, uses provider default if None).
        temperature: Sampling temperature (default: 0.7).
        max_tokens: Maximum tokens to generate (optional).
        previous_waifu_response: Previous waifu response for echo detection.

    Returns:
        Generated response text or None on failure.
    """
    try:
        if provider == "gemini":
            # For Gemini, we need to convert messages to a single prompt
            # since Gemini's generate_with_retry expects a string prompt
            if messages:
                # Convert the last user message to a prompt for Gemini compatibility
                last_message = messages[-1]
                if last_message.get("role") == "user":
                    prompt = last_message.get("content", "")
                else:
                    # Fallback to joining all messages
                    prompt = "\n".join([msg.get("content", "") for msg in messages])
            else:
                prompt = ""

            # Import here to avoid circular imports
            from genai_client import get_client
            client = get_client()
            if not client:
                return None

            return generate_with_gemini(
                client=client,
                model_name=model or "gemini-2.5-pro",
                prompt=prompt,
                previous_waifu_response=previous_waifu_response,
                max_tokens=max_tokens,
                temperature=temperature
            )

        elif provider == "openrouter":
            return generate_with_openrouter(
                messages=messages,
                model_name=model,
                temperature=temperature,
                max_tokens=max_tokens,
                previous_waifu_response=previous_waifu_response
            )

        else:
            # Unknown provider
            return None

    except Exception as e:
        # Log error and return None for any failure
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error generating chat response with provider {provider}: {e}")
        return None


def get_available_providers() -> List[str]:
    """
    Get list of available chat providers.

    Returns:
        List of supported provider names.
    """
    return ["gemini", "openrouter"]


def get_default_provider() -> str:
    """
    Get the default chat provider.

    Returns:
        Default provider name.
    """
    return "gemini"  # Maintain backward compatibility