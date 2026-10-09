import pytest

from codedoctor.schemas.analysis import AnalysisRequest
from codedoctor.services.analyzer import Analyzer


class FakeLLM:
    async def generate_structured(self, prompt: str, schema, request_id: str):
        return schema(
            diagnosis={
                "root_cause": "division by zero",
                "explanation": "The input list is empty.",
                "severity": "medium",
                "confidence": 0.95,
            }, 
            request_id=request_id
        )

@pytest.mark.asyncio
async def test_analyzer():
    analyzer = Analyzer(FakeLLM())

    request = AnalysisRequest(
        language="python",
        code="sum(x) / len(x)",
        error="ZeroDivisionError",
    )

    result = await analyzer.analyze(request, request_id="test-request-id")

    assert result.diagnosis.root_cause == "division by zero"
    assert result.diagnosis.confidence == 0.95