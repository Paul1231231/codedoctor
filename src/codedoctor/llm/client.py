from typing import Type, TypeVar

from pydantic import BaseModel
from openai import AsyncOpenAI

from codedoctor.core.config import settings


T = TypeVar("T", bound=BaseModel)


class LLMClient:

    def __init__(self) -> None:
        self.client = AsyncOpenAI(
            api_key=settings.model_api_key,
            base_url=settings.model_api_url,
        )

    async def generate_structured(
        self,
        prompt: str,
        schema: Type[T],
    ) -> T:

        response = await self.client.chat.completions.parse(
            model=settings.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            response_format=schema,
            temperature=0,
        )

        parsed = response.choices[0].message.parsed

        if parsed is None:
            raise ValueError(
                "LLM returned no structured response"
            )

        return parsed