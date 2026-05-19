import asyncio
import httpx
import sys
sys.path.insert(0, '.')
from config import AI_API_KEY, AI_BASE_URL, AI_MODEL

print(f'Key: {AI_API_KEY[:8]}...')
print(f'URL: {AI_BASE_URL}')
print(f'Model: {AI_MODEL}')

async def test():
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            f'{AI_BASE_URL}/chat/completions',
            headers={
                'Authorization': f'Bearer {AI_API_KEY}',
                'Content-Type': 'application/json',
            },
            json={
                'model': AI_MODEL,
                'messages': [{'role': 'user', 'content': 'hi'}],
                'max_tokens': 10,
            },
        )
        print(f'Status: {r.status_code}')
        print(f'Body: {r.text[:300]}')

asyncio.run(test())
