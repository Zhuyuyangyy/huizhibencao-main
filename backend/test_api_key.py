import httpx
import asyncio
from config import AI_API_KEY, AI_BASE_URL, AI_MODEL

print(f'API Key 前8位: {AI_API_KEY[:8]}...')
print(f'Base URL: {AI_BASE_URL}')
print(f'Model: {AI_MODEL}')
print()

async def test():
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.post(
                f"{AI_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {AI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": AI_MODEL,
                    "messages": [{"role": "user", "content": "hi"}],
                    "max_tokens": 10,
                },
            )
            print(f'状态码: {response.status_code}')
            print(f'响应: {response.text[:500]}')
        except Exception as e:
            print(f'异常: {str(e)}')

asyncio.run(test())
