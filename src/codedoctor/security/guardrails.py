from dataclasses import dataclass


SUPPORTED_LANGUAGES = {
    "python",
    "javascript",
    "java",
    "c",
    "cpp",
    "c++",
}

MAX_SOURCE_LENGTH = 50_000
MIN_TIMEOUT_SECONDS = 1
MAX_TIMEOUT_SECONDS = 10


@dataclass(frozen=True)
class GuardrailResult:
    allowed: bool
    reasons: tuple[str, ...] = ()


def validate_submission(
    source_code: str,
    language: str,
    timeout_seconds: int = 5,
) -> GuardrailResult:
    reasons: list[str] = []

    if not isinstance(source_code, str):
        return GuardrailResult(
            allowed=False,
            reasons=("Source code must be a string.",),
        )

    if not isinstance(language, str):
        return GuardrailResult(
            allowed=False,
            reasons=("Language must be a string.",),
        )

    if not source_code.strip():
        reasons.append("Source code cannot be empty.")

    if len(source_code) > MAX_SOURCE_LENGTH:
        reasons.append("Source code exceeds the size limit.")

    if language.strip().lower() not in SUPPORTED_LANGUAGES:
        reasons.append("Unsupported programming language.")

    # bool is a subclass of int in Python, so reject it explicitly.
    if (
        isinstance(timeout_seconds, bool)
        or not isinstance(timeout_seconds, int)
        or not MIN_TIMEOUT_SECONDS
        <= timeout_seconds
        <= MAX_TIMEOUT_SECONDS
    ):
        reasons.append("Invalid execution timeout.")

    return GuardrailResult(
        allowed=not reasons,
        reasons=tuple(reasons),
    )