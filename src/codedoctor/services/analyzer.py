import json

from click import prompt

from codedoctor.llm.client import LLMClient
from codedoctor.llm.prompts import SYSTEM_PROMPT
from codedoctor.schemas.analysis import AnalysisRequest, AnalysisResponse

class Analyzer:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    async def analyze(
        self,
        request: AnalysisRequest,
        request_id: str,
    ) -> AnalysisResponse:
        prompt = f"""
{SYSTEM_PROMPT}

Programming Language: {request.language}

Code:
```{request.language}
{request.code}
Error:
{request.error}
Stack Trace:
{request.stack_trace or "Not provided"}

Return ONLY valid JSON with this structure:
{{
  "diagnosis": {{
    "root_cause": "...",
    "explanation": "...",
    "severity": "low | medium | high | critical",
    "confidence": 0.0
  }}
}}
"""
        return await self.llm.generate_structured(
            prompt,
            AnalysisResponse,
            request_id=request_id,
        )