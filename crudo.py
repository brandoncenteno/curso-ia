import os
import httpx
from dotenv import load_dotenv

load_dotenv()

r = httpx.post(
    "https://api.anthropic.com/v1/messages",
    headers={
        "Authorization": f"Bearer {os.environ['ANTHROPIC_API_KEY']}",
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    },
    json={
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 200,
        "messages": [{"role": "user", "content": "Hola Claude, preséntate en una línea."}],
    },
    timeout=30,
)
print("Código HTTP:", r.status_code)
print(r.json())