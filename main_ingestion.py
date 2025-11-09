from dotenv import load_dotenv
import os 
from dgar_core.db_connector import NEO4J_DB
from dgar_core.db_connector import NEO4J_DB, Neo4jConnector
from dgar_core.extractor import extract_triplets
import os
import re
from datetime import datetime

CORPUS_FILE = "./data/temporal_corpus.txt"

def ingest_triplet(triplet: dict):

    try:
        rel_type = re.sub(r'[^A-Z_]', '', triplet['relationship'].upper().replace(' ', '_'))

        cypher_query = f"""
        MERGE (s:{triplet['subject_type']} {{name: $s_name}})
        MERGE (o:{triplet['object_type']} {{name: $o_name}})
        CREATE (s)-[r:{rel_type} {{
            timestamp: date($timestamp)
        }}]->(o)
        """
        
        parameters = {
            "s_name": triplet['subject'],
            "o_name": triplet['object'],
            "timestamp": triplet['timestamp']
        }
        
        if isinstance(NEO4J_DB, Neo4jConnector):
             NEO4J_DB._execute_write_query(cypher_query, parameters)
        
    except KeyError as e:
        print(f" Skipping triplet (Missing key): {e}. Data: {triplet}")
    except Exception as e:
        print(f" Skipping triplet (Cypher/DB error): {e}. Data: {triplet}")

def run_ingestion_pipeline():
    if NEO4J_DB is None:
        print(" Cannot run ingestion: Database connection failed.")
        return

    NEO4J_DB.clear_database()

    if not os.path.exists(CORPUS_FILE):
        print(f" ERROR: Corpus file not found at {CORPUS_FILE}. Please create it.")
        return
        
    with open(CORPUS_FILE, 'r') as f:
        corpus_text = f.read()
    
    print("Starting LLM-based Knowledge Extraction (Sending to OpenAI API)...")
    triplets = extract_triplets(corpus_text)
    
    print(f" Extracted {len(triplets)} total candidate triplets.")

    if not triplets:
        print("No triplets extracted. Check API key or corpus content.")
        return

    print(" Starting Neo4j Ingestion...")
    
    for t in triplets:
        ingest_triplet(t)

    print("\n Phase 2: Ingestion complete! Graph is ready.")


if __name__ == "__main__":
    run_ingestion_pipeline()
