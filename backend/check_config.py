from config import AI_API_KEY, AI_BASE_URL, AI_MODEL, AI_PROVIDER_LABEL, DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL, OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL

print('=== DeepSeek Config ===')
print(f'DEEPSEEK_API_KEY: {DEEPSEEK_API_KEY[:8]}...' if DEEPSEEK_API_KEY else 'DEEPSEEK_API_KEY: (empty)')
print(f'DEEPSEEK_BASE_URL: {DEEPSEEK_BASE_URL}')
print(f'DEEPSEEK_MODEL: {DEEPSEEK_MODEL}')
print()

print('=== OpenAI Config ===')
print(f'OPENAI_API_KEY: {OPENAI_API_KEY[:8]}...' if OPENAI_API_KEY else 'OPENAI_API_KEY: (empty)')
print(f'OPENAI_BASE_URL: {OPENAI_BASE_URL}')
print(f'OPENAI_MODEL: {OPENAI_MODEL}')
print()

print('=== Final AI Config ===')
print(f'AI_API_KEY: {AI_API_KEY[:8]}...' if AI_API_KEY else 'AI_API_KEY: (empty)')
print(f'AI_BASE_URL: {AI_BASE_URL}')
print(f'AI_MODEL: {AI_MODEL}')
print(f'AI_PROVIDER_LABEL: {AI_PROVIDER_LABEL}')
