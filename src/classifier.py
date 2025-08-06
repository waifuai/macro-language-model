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