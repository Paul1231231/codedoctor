from typing import Type, TypeVar
import logging
from pydantic import BaseModel
from openai import AsyncOpenAI

from codedoctor.core.config import settings

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)


class LLMClient:

    def __init__(self) -> None:
        self.client = AsyncOpenAI(
            api_key=settings.litellm_api_key,
            base_url=settings.litellm_api_url,
            timeout=30,
        )

    async def generate_structured(
        self,
        prompt: str,
        schema: Type[T],
        request_id: str,
    ) -> T:

        raw_response = (
            await self.client.chat.completions.with_raw_response.parse(
                model=settings.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                response_format=schema,
                temperature=0,
                extra_body={
                    "metadata": {
                        "request_id": request_id,
                        "feature": "code_analysis",
                    }
                },
            )
        )

        response = raw_response.parse()
        usage = response.usage

        cost_header = raw_response.headers.get(
            "x-litellm-response-cost"
        )
        call_id = raw_response.headers.get("x-litellm-call-id")

        logger.info(
            "llm_request_completed",
            extra={
                "request_id": request_id,
                "litellm_call_id": call_id,
                "model": response.model,
                "input_tokens": (
                    usage.prompt_tokens if usage else None
                ),
                "output_tokens": (
                    usage.completion_tokens if usage else None
                ),
                "cost_usd": (
                    float(cost_header)
                    if cost_header is not None
                    else None
                ),
            },
        )

        parsed = response.choices[0].message.parsed

        if parsed is None:
            raise ValueError(
                "LLM returned no structured response"
            )

        return parsed