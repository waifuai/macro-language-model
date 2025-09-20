"""
Centralized configuration management for the Waifu Chatbot application.

This module handles all configuration settings, environment variables, and file-based
overrides in a centralized manner. It provides a comprehensive configuration system
that manages API keys, model selections, personality settings, and small talk phrases
for the waifu chatbot.

Key features:
- Environment variable support for API keys and settings
- File-based configuration overrides in user home directory
- Centralized model management for different AI providers
- Small talk phrase management with fallback defaults
- Comprehensive error handling and logging
- Configuration caching for performance

The module supports multiple AI providers (Gemini, OpenRouter) and provides
convenient functions for accessing configuration values throughout the application.
"""
"""
Centralized configuration management for the Waifu Chatbot.

This module handles all configuration settings, environment variables,
and file-based overrides in a centralized manner.
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Any

# Configure logging for this module
logger = logging.getLogger(__name__)

# Application constants
APP_NAME = "Waifu Chatbot"
APP_VERSION = "1.0.0"
DEFAULT_WAIFU_NAME = "Waifu"
DEFAULT_PERSONALITY = "deredere"

# Personality types
PERSONALITY_TYPES: List[str] = [
    "deredere", "dandere", "himedere", "kuudere", "tsundere", "yandere"
]

# File paths for configuration files
CONFIG_DIR = Path.home() / ".waifu-chatbot"
SMALL_TALK_FILE = Path(__file__).parent / "chatbot_config.json"

# Model override files
GEMINI_MODEL_FILE = Path.home() / ".model-gemini"
OPENROUTER_MODEL_FILE = Path.home() / ".model-openrouter"
OPENROUTER_CHAT_MODEL_FILE = Path.home() / ".model-openrouter-chat"

# API key files
GEMINI_KEY_FILE = Path.home() / ".api-gemini"
OPENROUTER_KEY_FILE = Path.home() / ".api-openrouter"

# Default models
DEFAULT_GEMINI_MODEL = "gemini-2.5-pro"
DEFAULT_OPENROUTER_MODEL = "deepseek/deepseek-chat-v3-0324:free"
DEFAULT_OPENROUTER_CHAT_MODEL = "deepseek/deepseek-chat-v3-0324:free"


class ConfigManager:
    """Centralized configuration manager for the application."""

    def __init__(self):
        self._small_talk_cache: Optional[List[str]] = None
        self._config_cache: Dict[str, Any] = {}

    def _read_text_file(self, path: Path) -> Optional[str]:
        """Read and return content from a text file."""
        try:
            if path.is_file():
                content = path.read_text(encoding="utf-8").strip()
                return content or None
        except Exception as e:
            logger.debug(f"Error reading file {path}: {e}")
        return None

    def get_api_key(self, provider: str) -> Optional[str]:
        """
        Get API key for the specified provider.

        Args:
            provider: Either 'gemini' or 'openrouter'.

        Returns:
            API key if found, None otherwise.
        """
        if provider.lower() == 'gemini':
            # Check environment variables
            api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
            if api_key and api_key.strip():
                return api_key.strip()

            # Check file
            return self._read_text_file(GEMINI_KEY_FILE)

        elif provider.lower() == 'openrouter':
            # Check environment variable
            api_key = os.environ.get("OPENROUTER_API_KEY")
            if api_key and api_key.strip():
                return api_key.strip()

            # Check file
            return self._read_text_file(OPENROUTER_KEY_FILE)

        else:
            logger.warning(f"Unknown provider: {provider}")
            return None

    def get_model(self, provider: str) -> str:
        """
        Get model name for the specified provider.

        Args:
            provider: Either 'gemini', 'openrouter', or 'openrouter_chat'.

        Returns:
            Model name to use.
        """
        if provider.lower() == 'gemini':
            override = self._read_text_file(GEMINI_MODEL_FILE)
            return override if override else DEFAULT_GEMINI_MODEL

        elif provider.lower() == 'openrouter':
            override = self._read_text_file(OPENROUTER_MODEL_FILE)
            return override if override else DEFAULT_OPENROUTER_MODEL

        elif provider.lower() == 'openrouter_chat':
            override = self._read_text_file(OPENROUTER_CHAT_MODEL_FILE)
            return override if override else DEFAULT_OPENROUTER_CHAT_MODEL

        else:
            logger.warning(f"Unknown provider: {provider}")
            return DEFAULT_GEMINI_MODEL

    def get_small_talk(self) -> List[str]:
        """
        Get small talk phrases from configuration file.

        Returns:
            List of small talk phrases.
        """
        if self._small_talk_cache is not None:
            return self._small_talk_cache

        try:
            if SMALL_TALK_FILE.is_file():
                with open(SMALL_TALK_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    small_talk = config.get('small_talk', [])
                    self._small_talk_cache = small_talk
                    return small_talk
        except Exception as e:
            logger.warning(f"Error loading small talk configuration: {e}")

        # Fallback to default small talk
        default_talk = [
            "I wonder what the next big trend will be...",
            "Do you believe in fate?",
            "What's your favorite color?",
            "If you could have any superpower, what would it be?",
            "What's the meaning of life?",
            "Do you like cats or dogs more?",
            "What's your favorite season?",
            "Do you prefer the mountains or the beach?",
            "What's your favorite type of music?",
            "Do you like to dance?"
        ]
        self._small_talk_cache = default_talk
        return default_talk

    def get_config_value(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.

        Args:
            key: Configuration key.
            default: Default value if key not found.

        Returns:
            Configuration value or default.
        """
        return self._config_cache.get(key, default)

    def set_config_value(self, key: str, value: Any) -> None:
        """
        Set configuration value.

        Args:
            key: Configuration key.
            value: Value to set.
        """
        self._config_cache[key] = value

    def ensure_config_dir(self) -> Path:
        """Ensure configuration directory exists."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        return CONFIG_DIR


# Global configuration manager instance
config_manager = ConfigManager()


def get_api_key(provider: str) -> Optional[str]:
    """Convenience function to get API key."""
    return config_manager.get_api_key(provider)


def get_model(provider: str) -> str:
    """Convenience function to get model."""
    return config_manager.get_model(provider)


def get_small_talk() -> List[str]:
    """Convenience function to get small talk phrases."""
    return config_manager.get_small_talk()