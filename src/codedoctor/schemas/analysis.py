from pydantic import BaseModel, Field

from typing import Literal


class AnalysisRequest(BaseModel):
    """
    Represents a request for code analysis.

    Attributes:
        language (str): The programming language of the source code.
        code (str): The source code to be analyzed.
        error (str): An error message related to the analysis request.
        stack_trace (str | None): The stack trace of the error, if available.
        diagnosis (Diagnosis): The diagnosis of the error.
    """
    language: str = Field(
        min_length=1,
        max_length=50,
        description="The programming language of the source code.",
    )
    code: str = Field(
        min_length=1,
        max_length=10000,
        description="The source code to be analyzed.",
    )
    error: str = Field(
        min_length=1,
        max_length = 5000,
        description="An error message related to the analysis request.",
    )
    stack_trace: str | None = Field(
        default=None,
        description="The stack trace of the error, if available.",
    )

class Diagnosis(BaseModel):
    """
    Represents a diagnosis of an error in the source code.
    """
    root_cause: str
    explanation: str

    severity: Literal["low", "medium", "high", "critical"]

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

class AnalysisResponse(BaseModel):
    request_id: str
    diagnosis: Diagnosis