import pytest

from codedoctor.security.validators import (
    validate_python_syntax,
    validate_source,
)


def test_accepts_valid_python():
    result = validate_python_syntax(
        "def add(a, b):\n    return a + b\n"
    )

    assert result.status == "valid"
    assert result.errors == ()


def test_rejects_invalid_python():
    result = validate_python_syntax(
        "def add(a, b)\n    return a + b\n"
    )

    assert result.status == "invalid"
    assert "syntax error" in result.errors[0].lower()


def test_python_language_dispatch():
    result = validate_source(
        "print('hello')",
        "python",
    )

    assert result.status == "valid"


@pytest.mark.parametrize(
    "language",
    ["javascript", "java", "c", "cpp"],
)
def test_other_languages_defer_to_sandbox(language):
    result = validate_source(
        "some source code",
        language,
    )

    assert result.status == "deferred"


def test_rejects_unknown_language():
    result = validate_source(
        "puts 'hello'",
        "ruby",
    )

    assert result.status == "invalid"