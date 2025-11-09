from dgar_core.db_connector import NEO4J_DB
from datetime import datetime

def get_temporal_context(entity_name: str) -> str:
    
    if NEO4J_DB is None:
        return "ERROR: Database connection failed."

    cypher_query = """
    MATCH (s)-[r]->(o)
    WHERE s.name = $name OR o.name = $name
    AND r.timestamp IS NOT NULL
    RETURN s.name AS source, 
           type(r) AS relationship, 
           o.name AS target, 
           toString(r.timestamp) AS date
    ORDER BY r.timestamp ASC
    """
    
    parameters = {"name": entity_name}
    
    results = NEO4J_DB.execute_query(cypher_query, parameters)

    if not results:
        return f"No temporal facts found for {entity_name}."

    context_lines = [f"Chronological History for {entity_name}:"]
    
    for row in results:

        subject = row['source']
        target = row['target']
        
        
        context_lines.append(
            f"[{row['date']}] {subject} --{row['relationship']}--> {target}"
        )
        
    return "\n".join(context_lines)
