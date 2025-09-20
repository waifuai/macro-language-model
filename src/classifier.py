"""
Provider-agnostic text classification interface for the Waifu Chatbot application.

This module provides a unified facade for text classification services, abstracting
the implementation details of different AI providers. It currently supports OpenRouter
for content classification and is designed to be easily extensible for additional
providers.

Key features:
- Unified interface for multiple classification providers
- Provider abstraction for easy switching and extension
- Consistent API across different classification services
- Error handling and fallback mechanisms
- Extensible design for future AI providers
- Centralized provider management

The module serves as a bridge between the application and various text classification
services, ensuring consistent behavior and providing a clean interface for determining
whether text content is human-written or machine-generated.
"""
from typing import Optional

from provider_openrouter import classify_with_openrouter, DEFAULT_OPENROUTER_MODEL


def classify(text: str, provider: str = "openrouter", model: Optional[str] = None) -> Optional[str]:
    """
    Provider-agnostic facade for classification.
    Currently supports:
      - provider="openrouter" using OpenRouter chat completions

    Returns:
      "0" or "1" on success, None on failure.
    """
    if provider == "openrouter":
        return classify_with_openrouter(text, model_name=model or DEFAULT_OPENROUTER_MODEL)
    # Placeholder for future providers (e.g., gemini, openai) following same interface
    return None