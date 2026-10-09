import pytest

from codedoctor.security.guardrails import (
    validate_submission,
)


def test_accepts_supported_language():
    result = validate_submission(
        source_code="print('hello')",
        language="python",
    )

    assert result.allowed is True
    assert result.reasons == ()


def test_normalizes_language():
    result = validate_submission(
        source_code="console.log('hello')",
        language=" JavaScript ",
    )

    assert result.allowed is True


def test_rejects_unsupported_language():
    result = validate_submission(
        source_code="print('hello')",
        language="ruby",
    )

    assert result.allowed is False
    assert "Unsupported programming language." in result.reasons


def test_rejects_empty_source():
    result = validate_submission(
        source_code="   ",
        language="python",
    )

    assert result.allowed is False


def test_rejects_oversized_source():
    result = validate_submission(
        source_code="x" * 50_001,
        language="python",
    )

    assert result.allowed is False


@pytest.mark.parametrize("timeout", [0, 11, -1, True, 1.5])
def test_rejects_invalid_timeout(timeout):
    result = validate_submission(
        source_code="print('hello')",
        language="python",
        timeout_seconds=timeout,
    )

    assert result.allowed is False