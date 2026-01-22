import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1"

SYSTEM_PROMPT = """
You are a knowledge graph extractor.
Extract ONLY time-stamped, directed facts.
Return STRICT JSON only. No explanations.

Schema:
[
  {
    "subject": "string",
    "subject_type": "Person | Company | Product | Location | Other",
    "relationship": "UPPERCASE_UNDERSCORE",
    "object": "string",
    "object_type": "Person | Company | Product | Location | Other",
    "timestamp": "YYYY-MM-DD"
  }
]
"""

def extract_triplets(text: str) -> list:
    payload = {
        "model": MODEL_NAME,
        "prompt": f"{SYSTEM_PROMPT}\n\nDOCUMENT:\n{text}",
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()

        raw_output = response.json().get("response", "").strip()
        if raw_output.startswith("```"):
                raw_output = raw_output.strip("`")
                if raw_output.lower().startswith("json"):
                      raw_output = raw_output[4:].strip()
        print("\n--- RAW LLM OUTPUT START ---")
        print(raw_output)
        print("--- RAW LLM OUTPUT END ---\n")
        return json.loads(raw_output)

    except Exception as e:
        print(f"[Extractor Error] {e}")
        return []
