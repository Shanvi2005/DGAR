from neo4j import GraphDatabase

from neo4j.exceptions import ServiceUnavailable
from dotenv import load_dotenv
import os

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

class Neo4jConnector:
    
    def __init__(self):
        if not all([URI, USERNAME, PASSWORD]):
            raise ValueError("NEO4J credentials not fully set in .env file.")
        
        try:
            self.driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
            self.driver.verify_connectivity()
            print("Neo4j Connection Driver Initialized.")
        except ServiceUnavailable as e:
            print(f"ERROR: Neo4j service unavailable. Is Docker running? {e}")
            raise

    def close(self):
        self.driver.close()

    def _execute_read_query(self, query, parameters=None, db="neo4j"):
        with self.driver.session(database=db) as session:
            return session.execute_read(lambda tx: tx.run(query, parameters).data())

    def _execute_write_query(self, query, parameters=None, db="neo4j"):
        with self.driver.session(database=db) as session:
            # Explicitly use execute_write for write queries
            return session.execute_write(lambda tx: tx.run(query, parameters).data())

    def execute_query(self, query, parameters=None, db="neo4j"):  
        query_start = query.strip().lower()
        
        is_write_query = query_start.startswith(
            ('create', 'merge', 'set', 'delete', 'detach', 'remove')
        )

        if is_write_query:
            return self._execute_write_query(query, parameters, db)
        else:
            return self._execute_read_query(query, parameters, db)

    def clear_database(self):
        self._execute_write_query("MATCH (n) DETACH DELETE n")
        print("Neo4j Database cleared.")

try:
    NEO4J_DB = Neo4jConnector()
except Exception:
    NEO4J_DB = None 
