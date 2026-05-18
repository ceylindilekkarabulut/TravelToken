from openai import AsyncOpenAI
from app.config import settings

_client = AsyncOpenAI(api_key=settings.openai_api_key)


async def chat_completion(prompt: str, model: str = "gpt-4o-mini") -> str:
    response = await _client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
    )
    return response.choices[0].message.content or ""
