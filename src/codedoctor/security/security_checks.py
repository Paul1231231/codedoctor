from guardrails import Guard, OnFailAction
from guardrails_ai.detect_pii import DetectPII
from guardrails_ai.prompt_injection_detector import PromptInjectionDetector


# Check untrusted user input before sending it to the LLM.
prompt_injection_guard = Guard().use(
    PromptInjectionDetector(on_fail=OnFailAction.EXCEPTION)
)

# Check text for sensitive personal information.
pii_guard = Guard().use(
    DetectPII(
        [
            "EMAIL_ADDRESS",
            "PHONE_NUMBER",
            "PERSON",
            "CREDIT_CARD",
            "IP_ADDRESS",
        ],
        on_fail=OnFailAction.EXCEPTION,
    )
)


def check_prompt_injection(text: str) -> None:
    """Raise a validation error if text appears to contain prompt injection."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Prompt must be a non-empty string.")

    prompt_injection_guard.validate(text)


def check_pii(text: str) -> None:
    """Raise a validation error if text contains configured PII types."""
    if not isinstance(text, str):
        raise TypeError("Text to check must be a string.")

    pii_guard.validate(text)


def check_user_input(text: str) -> None:
    """Run security checks before sending user input to the LLM."""
    check_prompt_injection(text)
    check_pii(text)


def check_llm_output(text: str) -> None:
    """Check LLM output before returning it to the user."""
    check_pii(text)