import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from provider_openrouter import (
    classify_with_openrouter,
    _resolve_openrouter_api_key,
    OPENROUTER_API_KEY_FILE_PATH,
)


def test_resolve_key_from_env(monkeypatch, tmp_path):
    monkeypatch.setenv("OPENROUTER_API_KEY", "env-key")
    # Ensure no file is consulted
    monkeypatch.setattr("provider_openrouter.OPENROUTER_API_KEY_FILE_PATH", tmp_path / ".api-openrouter")
    assert _resolve_openrouter_api_key() == "env-key"


def test_resolve_key_from_file(monkeypatch, tmp_path):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    # Mock the config system to return our test key
    def mock_get_api_key(provider):
        if provider == "openrouter":
            return "file-key"
        return None

    monkeypatch.setattr("provider_openrouter.get_api_key", mock_get_api_key)
    assert _resolve_openrouter_api_key() == "file-key"


@patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}, clear=True)
@patch("provider_openrouter.requests.post")
def test_openrouter_success_returns_1(mock_post):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"choices": [{"message": {"content": "1"}}]}
    mock_post.return_value = mock_resp

    result = classify_with_openrouter("example")
    assert result == "1"
    mock_post.assert_called_once()


@patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}, clear=True)
@patch("provider_openrouter.requests.post")
def test_openrouter_heuristic_0_only(mock_post):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"choices": [{"message": {"content": "Output: 0"}}]}
    mock_post.return_value = mock_resp

    result = classify_with_openrouter("example")
    assert result == "0"


@patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}, clear=True)
@patch("provider_openrouter.requests.post")
def test_openrouter_heuristic_1_only(mock_post):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"choices": [{"message": {"content": "Label 1"}}]}
    mock_post.return_value = mock_resp

    result = classify_with_openrouter("example")
    assert result == "1"


@patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}, clear=True)
@patch("provider_openrouter.requests.post")
def test_openrouter_non_200(mock_post):
    mock_resp = MagicMock()
    mock_resp.status_code = 429
    mock_resp.text = "rate limited"
    mock_post.return_value = mock_resp
    result = classify_with_openrouter("example")
    assert result is None


@patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}, clear=True)
@patch("provider_openrouter.requests.post")
def test_openrouter_missing_choices(mock_post):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {}
    mock_post.return_value = mock_resp
    result = classify_with_openrouter("example")
    assert result is None


@patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}, clear=True)
@patch("provider_openrouter.requests.post", side_effect=Exception("timeout"))
def test_openrouter_exception_returns_none(mock_post):
    result = classify_with_openrouter("example")
    assert result is None