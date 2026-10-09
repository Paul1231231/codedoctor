from dataclasses import dataclass
from typing import Literal


ValidationStatus = Literal[
    "valid",
    "invalid",
    "deferred",
]


@dataclass(frozen=True)
class ValidationResult:
    status: ValidationStatus
    errors: tuple[str, ...] = ()

import ast


def validate_python_syntax(
    source_code: str,
) -> ValidationResult:
    try:
        ast.parse(source_code)
    except SyntaxError as exc:
        location = (
            f"line {exc.lineno}"
            if exc.lineno is not None
            else "unknown location"
        )

        return ValidationResult(
            status="invalid",
            errors=(
                f"Python syntax error at {location}: {exc.msg}",
            ),
        )

    return ValidationResult(status="valid")

def validate_source(
    source_code: str,
    language: str,
) -> ValidationResult:
    normalized_language = language.strip().lower()

    if normalized_language == "python":
        return validate_python_syntax(source_code)

    if normalized_language in {
        "javascript",
        "java",
        "c",
        "cpp",
    }:
        return ValidationResult(
            status="deferred",
            errors=(
                f"Syntax validation for {normalized_language} "
                "will be performed by its sandbox compiler "
                "or runtime.",
            ),
        )

    return ValidationResult(
        status="invalid",
        errors=("Unsupported programming language.",),
    )