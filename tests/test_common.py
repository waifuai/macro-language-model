"""Regression coverage for common OpenRouter mode helpers."""

import logging

import pytest

from modes.common import validate_client


def test_validate_client_rejects_none_and_logs_reason(caplog):
    """Only an absent client is invalid, and its diagnostic remains available."""
    with caplog.at_level(logging.ERROR, logger="modes.common"):
        assert validate_client(None) is False

    assert "Client is None" in caplog.messages


@pytest.mark.parametrize("client", [False, 0, "", [], {}, object()])
def test_validate_client_accepts_non_none_values(client):
    """Validation is an initialization sentinel check, not a truthiness/type check."""
    assert validate_client(client) is True
