import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1"

def generate_grounded_response(temporal_context: str, user_query: str) -> str:
    if not temporal_context:
        return "ERROR: No grounded context available to answer the question."

    prompt = f"""
You are a fact-checking assistant.

RULES:
- Use ONLY the information in the context below
- Do NOT use prior knowledge
- If the answer cannot be determined, say so clearly

--- TEMPORAL KNOWLEDGE GRAPH CONTEXT ---
{temporal_context}
---

QUESTION:
{user_query}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()["response"].strip()
    except Exception as e:
        return f"[Generation Error] {e}"
