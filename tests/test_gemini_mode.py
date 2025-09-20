"""
Unit tests for the Gemini conversation mode in the Waifu Chatbot application.

This module contains comprehensive unit tests for the Gemini mode functionality,
including tests for API failures, user interactions, conversation loops, exception
handling, and provider parameter passing. The tests use mocking to simulate various
scenarios without requiring actual API calls.

Test coverage includes:
- API failure scenarios and error handling
- User input simulation and exit conditions
- Conversation loop functionality with multiple turns
- Exception handling and recovery mechanisms
- Provider parameter validation and routing
- Debug mode functionality and logging

The tests ensure robust behavior of the Gemini mode under various conditions
and help maintain code quality during development and refactoring.
"""
import builtins
import pytest
from unittest.mock import patch


def test_no_api(monkeypatch, capsys):
    # Mock generate_chat_response to return None (API failure)
    with patch('modes.gemini_mode.generate_chat_response', return_value=None):
        from modes.gemini_mode import run_gemini_mode
        run_gemini_mode('W', 'p', debug=False)
        captured = capsys.readouterr()
        assert 'Error: Could not generate greeting.' in captured.out


def test_exit_immediately(monkeypatch, capsys):
    # Mock generate_chat_response to return a fixed greeting
    with patch('modes.gemini_mode.generate_chat_response', return_value='Hello!'):
        from modes.gemini_mode import run_gemini_mode
        # Simulate user input 'exit'
        inputs = iter(['exit'])
        monkeypatch.setattr(builtins, 'input', lambda prompt='': next(inputs))
        run_gemini_mode('Waifu', 'deredere', debug=False)
        captured = capsys.readouterr()
        # Expect greeting and exit message
        assert 'Waifu: Hello!' in captured.out
        assert 'Exiting Gemini mode.' in captured.out


def test_loop_and_response(monkeypatch, capsys):
    # Test one round of conversation then exit
    responses = ['Hi there!', 'User response']
    response_iter = iter(responses)

    def mock_generate_chat_response(*args, **kwargs):
        try:
            return next(response_iter)
        except StopIteration:
            return None

    with patch('modes.gemini_mode.generate_chat_response', side_effect=mock_generate_chat_response):
        from modes.gemini_mode import run_gemini_mode
        # Simulate user inputs: first normal, then 'quit'
        inputs = iter(['hello', 'quit'])
        monkeypatch.setattr(builtins, 'input', lambda prompt='': next(inputs))

        run_gemini_mode('A', 'b', debug=True)
        captured = capsys.readouterr()
        # Check that debug info and conversation are printed
        assert 'A: Hi there!' in captured.out
        assert '[DEBUG] User input: hello' in captured.out
        assert '[DEBUG] Conversation history:' in captured.out
        assert 'A: User response' in captured.out
        assert 'Exiting Gemini mode.' in captured.out


def test_exception_handling(monkeypatch, capsys):
    # Test exception handling in greeting generation
    with patch('modes.gemini_mode.generate_chat_response', side_effect=Exception('API Error')):
        from modes.gemini_mode import run_gemini_mode
        run_gemini_mode('Waifu', 'deredere', debug=False)
        captured = capsys.readouterr()
        assert 'Error generating greeting: API Error' in captured.out


def test_provider_parameter(monkeypatch, capsys):
    # Test that provider parameter is passed correctly
    with patch('modes.gemini_mode.generate_chat_response') as mock_generate:
        mock_generate.return_value = 'Hello from OpenRouter!'
        inputs = iter(['exit'])
        monkeypatch.setattr(builtins, 'input', lambda prompt='': next(inputs))

        from modes.gemini_mode import run_gemini_mode
        run_gemini_mode('Waifu', 'deredere', debug=False, provider='openrouter')

        captured = capsys.readouterr()
        assert 'Waifu: Hello from OpenRouter!' in captured.out
        # Verify that generate_chat_response was called with the correct provider
        mock_generate.assert_called()
        call_args = mock_generate.call_args
        assert call_args[1]['provider'] == 'openrouter'
