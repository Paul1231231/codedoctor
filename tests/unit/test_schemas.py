import pytest
from pydantic import ValidationError

from codedoctor.schemas.analysis import AnalysisRequest, Diagnosis

def test_valid_analysis_request():
    request = AnalysisRequest(
        language="Python",
        code="print('Hello World')",
        error="some error",
    )
    assert request.language == "Python"

def test_empty_code_is_rejected():
    with pytest.raises(ValidationError):
        AnalysisRequest(
            language="Python",
            code="",
            error="some error",
        )

def test_confidence_out_of_bounds_is_rejected():
    with pytest.raises(ValidationError):
        Diagnosis(
            root_cause="some cause",
            explanation="some explanation",
            severity="medium",
            confidence=1.5,  # Invalid confidence
        )