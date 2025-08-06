from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Dict, Any

import requests

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def _read_text_file(path: Path) -> Optional[str]:
    try:
        if path.is_file():
            content = path.read_text(encoding="utf-8").strip()
            return content or None
    except Exception:
        pass
    return None

def _resolve_default_openrouter_model() -> str:
    override = _read_text_file(Path.home() / ".model-openrouter")
    return override if override else "openrouter/horizon-beta"

DEFAULT_OPENROUTER_MODEL = _resolve_default_openrouter_model()
OPENROUTER_API_KEY_FILE_PATH = Path.home() / ".api-openrouter"


def _resolve_openrouter_api_key() -> Optional[str]:
    """
    Resolve the OpenRouter API key using the following order:
      1) Environment variable OPENROUTER_API_KEY (must be non-empty after strip)
      2) File at ~/.api-openrouter (single-line, no extra whitespace)
      3) None if neither is available
    """
    env_key = os.getenv("OPENROUTER_API_KEY")
    if env_key and env_key.strip():
        return env_key.strip()
    try:
        if OPENROUTER_API_KEY_FILE_PATH.is_file():
            return OPENROUTER_API_KEY_FILE_PATH.read_text(encoding="utf-8").strip()
    except Exception:
        # Swallow and return None per design
        pass
    return None


def _classification_prompt(text: str) -> str:
    """
    Deterministic prompt to classify a sentence as human or machine.
    Requests a strict single digit output 0 or 1.
    """
    return (
        "Classify the following sentence as human-written or machine-generated.\n\n"
        "Categories:\n"
        "- '1': Human-written\n"
        "- '0': Machine-generated\n\n"
        "Respond with ONLY the digit '0' or '1'.\n\n"
        f"Sentence: \"{text}\"\n\n"
        "Classification:"
    )


def _build_payload(text: str, model_name: str) -> Dict[str, Any]:
    return {
        "model": model_name,
        "messages": [{"role": "user", "content": _classification_prompt(text)}],
        "temperature": 0.0,
    }


def classify_with_openrouter(
    text: str,
    model_name: str = DEFAULT_OPENROUTER_MODEL,
    timeout: int = 60,
) -> Optional[str]:
    """
    Call OpenRouter chat completions with a deterministic classification prompt.
    Returns:
      - "0" or "1" string on success
      - None on any error path, including missing key, HTTP errors, malformed responses
    """
    api_key = _resolve_openrouter_api_key()
    if not api_key:
        return None

    payload = _build_payload(text, model_name)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=timeout)
        if resp.status_code != 200:
            return None
        data = resp.json()

        choices = data.get("choices", [])
        if not choices:
            return None
        content = (choices[0].get("message", {}).get("content") or "").strip()
        if not content:
            return None

        # Strict normalization
        if content in ("0", "1"):
            return content

        # Cautious fallbacks
        contains0 = "0" in content
        contains1 = "1" in content
        if contains0 and not contains1:
            return "0"
        if contains1 and not contains0:
            return "1"

        return None
    except Exception:
        return None