import builtins
import pytest
from modes import gemini_mode


class DummyModel:
    pass


class DummyGenAI:
    def GenerativeModel(self, *args, **kwargs):
        return DummyModel()


def test_no_api(monkeypatch, capsys):
    # setup_gemini_api returns None leads to no output
    monkeypatch.setattr(gemini_mode, 'setup_gemini_api', lambda: None)
    gemini_mode.run_gemini_mode('W', 'p', debug=False)
    captured = capsys.readouterr()
    assert captured.out == ''


def test_exit_immediately(monkeypatch, capsys):
    # setup_gemini_api returns a dummy genai instance
    monkeypatch.setattr(gemini_mode, 'setup_gemini_api', lambda: DummyGenAI())
    # Stub generate_with_retry to return a fixed greeting
    monkeypatch.setattr(gemini_mode, 'generate_with_retry', lambda model, prompt, cont: 'Hello!')
    # Simulate user input 'exit'
    inputs = iter(['exit'])
    monkeypatch.setattr(builtins, 'input', lambda prompt='': next(inputs))
    gemini_mode.run_gemini_mode('Waifu', 'deredere', debug=False)
    captured = capsys.readouterr()
    # Expect greeting and exit message
    assert 'Waifu: Hello!' in captured.out
    assert 'Exiting Gemini mode.' in captured.out


def test_loop_and_response(monkeypatch, capsys):
    # Test one round of conversation then exit
    monkeypatch.setattr(gemini_mode, 'setup_gemini_api', lambda: DummyGenAI())
    # First call: greeting, then prompt response
    responses = ['Hi there!', 'User response', 'farewell']
    def fake_generate(model, prompt, cont):
        # Pop next response
        return responses.pop(0)
    monkeypatch.setattr(gemini_mode, 'generate_with_retry', fake_generate)
    # Simulate user inputs: first normal, then 'quit'
    inputs = iter(['hello', 'quit'])
    monkeypatch.setattr(builtins, 'input', lambda prompt='': next(inputs))

    gemini_mode.run_gemini_mode('A', 'b', debug=True)
    captured = capsys.readouterr()
    # Check that debug info and conversation are printed
    assert 'A: Hi there!' in captured.out
    assert '[DEBUG] User input: hello' in captured.out
    assert '[DEBUG] Prompt to Gemini:' in captured.out
    assert 'A: User response' in captured.out
    assert 'Exiting Gemini mode.' in captured.out
