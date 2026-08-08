import os
from dotenv import load_dotenv

load_dotenv()

def _client():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return None
    from openai import OpenAI
    return OpenAI(api_key=key)

def ask(prompt, system=None):
    client = _client()
    if client is None:
        return None
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(model=model, messages=messages, temperature=0.2)
    return response.choices[0].message.content.strip()
