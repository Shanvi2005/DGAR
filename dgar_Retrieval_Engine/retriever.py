import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv # Need to load .env for the key
from google import genai
from google.genai import types 
from dgar_core.db_connector import NEO4J_DB, Neo4jConnector 
from DGAR_Retrieval_Engine.dgar_logic import get_temporal_context

load_dotenv()

try:
    CLIENT = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
except Exception as e:
    print(f" ERROR: Could not initialize Gemini Client. Details: {e}")
    CLIENT = None 

def generate_grounded_response(user_query: str) -> str:
    
    target_entity = "TechCorp" # Hardcode the main entity for testing the temporal facts

    print(f"-> Searching DGAR for: {target_entity}")

    temporal_context = get_temporal_context(target_entity)

    if "ERROR" in temporal_context or "No temporal facts" in temporal_context:
        return f"Retrieval Error: {temporal_context}"

    augmented_prompt = f"""
    You are a specialized Temporal Reasoning AI. Your goal is to answer the user's question 
    using ONLY the provided chronological history. If the answer changes over time, state the change clearly.
    
    --- CHRONOLOGICAL KNOWLEDGE GRAPH CONTEXT ---
    {temporal_context}
    ---
    
    USER QUESTION: {user_query}
    
    ANSWER: Based ONLY on the provided history, the answer is:
    """

    if CLIENT is None:
        return "LLM Generation Error: Gemini Client not initialized. Check API Key."

    try:
        response = CLIENT.models.generate_content(
            model='gemini-2.5-flash', 
            contents=[augmented_prompt],
            config=types.GenerateContentConfig(
                temperature=0.1
            )
        )
        return response.text
        
    except Exception as e:
        return f" LLM Generation Error (Gemini): {e}"

if __name__ == "__main__":
    
    temporal_query = "What was TechCorp's main product *before* Project Nova was launched, and who was the CEO in 2024?"
    
    print("\n RUNNING DGAR TEST QUERY ")
    final_answer = generate_grounded_response(temporal_query)
    
    print("\n" + "="*50)
    print("DGAR FINAL RESPONSE:")
    print(final_answer)
    print("="*50)
