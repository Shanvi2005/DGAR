from google import genai
from google.genai import types
import json
import os
try:
    CLIENT = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
except Exception as e:
    print(f" GEMINI CLIENT ERROR: Could not initialize client. {e}")
    CLIENT = None 
def extract_triplets(text_chunk: str) -> list:
    if CLIENT is None:
        return []
    
    output_schema_instructions = """
    [
      {
        "subject": "Entity name (e.g., Sarah Chen)",
        "subject_type": "Label (e.g., Person, Company)",
        "relationship": "Directed relationship (e.g., WORKS_AT, FOUNDED)",
        "object": "Entity name or value (e.g., TechCorp, Seattle)",
        "object_type": "Label (e.g., Company, Location)",
        "timestamp": "YYYY-MM-DD"
      }
    ]
    """
    
    system_prompt = (
        "You are a meticulous knowledge graph extractor. "
        "Your task is to analyze the text and extract all self-contained, directed, temporal facts. "
        "The response MUST be a single, parsable JSON list adhering strictly to this schema: "
        f"{output_schema_instructions}"
        "Every fact MUST include a YYYY-MM-DD 'timestamp'. Do not include any explanations or commentary."
    )
    
    try:
        response = CLIENT.models.generate_content(
            model='gemini-2.5-flash', # Fast, capable model
            contents=[system_prompt, f"DOCUMENT: {text_chunk}"],
            config=types.GenerateContentConfig(
                response_mime_type="application/json", 
            )
        )
        
        raw_json_string = response.text.strip()

        content = json.loads(raw_json_string)
        
        if isinstance(content, list):
            return content
        return content.get('triplets', content.get('facts', []))
        
    except Exception as e:
        print(f" GEMINI API CALL FAILED: {e}")
        return []
