from typing import Optional
import os
from pathlib import Path

# Central model selection with optional override file ~/.model-gemini
def _read_text_file(path: Path) -> Optional[str]:
    try:
        if path.is_file():
            content = path.read_text(encoding="utf-8").strip()
            return content or None
    except Exception as e:
        print(f"Error reading text file {path}: {e}")
    return None

def _resolve_gemini_model() -> str:
    override = _read_text_file(Path.home() / ".model-gemini")
    return override if override else "gemini-2.5-pro"

GEMINI_MODEL = _resolve_gemini_model()

def _read_key_file(path: str) -> Optional[str]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error reading API key from {path}: {e}")
        return None

def resolve_api_key() -> Optional[str]:
    # Env-first
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if api_key:
        return api_key
    # Fallback to ~/.api-gemini
    key_path = os.path.expanduser("~/.api-gemini")
    return _read_key_file(key_path)

def get_client():
    """
    Build and return a google.genai Client using env vars or ~/.api-gemini.

    Prefers:
      - GEMINI_API_KEY
      - GOOGLE_API_KEY
    Fallback:
      - ~/.api-gemini single-line key file
    """
    # Lazy import to avoid top-level hard dependency in modules
    from google import genai
    api_key = resolve_api_key()
    if not api_key:
        raise RuntimeError("No API key found: set GEMINI_API_KEY/GOOGLE_API_KEY or create ~/.api-gemini")
    # Construct central client
    return genai.Client(api_key=api_key)