import os
import uuid

import pytest
from pydantic import BaseModel

from codedoctor.llm.client import LLMClient
from codedoctor.schemas.analysis import AnalysisResponse


pytestmark = [
    pytest.mark.integration,
    pytest.mark.llm,
]


@pytest.fixture
def llm_client() -> LLMClient:
    return LLMClient()


@pytest.mark.asyncio
async def test_generate_structured_returns_valid_schema(
    llm_client: LLMClient,
) -> None:
    request_id = str(uuid.uuid4())

    prompt = """
    Diagnose this Python error:

    Code:
    x = 1 / 0

    Error:
    ZeroDivisionError: division by zero

    Explain the root cause and suggest a fix.
    """

    result = await llm_client.generate_structured(
        prompt=prompt,
        schema=AnalysisResponse,
        request_id=request_id,
    )

    assert isinstance(result, AnalysisResponse)


@pytest.mark.asyncio
async def test_generate_structured_handles_simple_bug(
    llm_client: LLMClient,
) -> None:
    request_id = str(uuid.uuid4())

    prompt = """
    Diagnose this Python error:

    Code:
    print(user_name)

    Error:
    NameError: name 'user_name' is not defined

    Return a structured diagnosis and a suggested fix.
    """

    result = await llm_client.generate_structured(
        prompt=prompt,
        schema=AnalysisResponse,
        request_id=request_id,
    )

    assert isinstance(result, AnalysisResponse)
