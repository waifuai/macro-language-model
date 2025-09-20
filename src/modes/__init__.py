"""
Package initialization for the Waifu Chatbot modes module.

This file marks the modes directory as a Python package and provides convenient
imports for all conversation mode implementations. It serves as the central
entry point for accessing different conversation modes (Interactive, Auto, Gemini)
used throughout the Waifu Chatbot application.

The module exports the main functions for running each conversation mode:
- run_gemini_mode: Direct Gemini AI interaction mode
- run_auto_mode: AI vs AI conversation simulation mode
- run_interactive_mode: Real-time user interaction mode
"""
from .gemini_mode import run_gemini_mode
from .auto_mode import run_auto_mode
from .interactive_mode import run_interactive_mode