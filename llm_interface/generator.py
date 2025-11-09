def generate_grounded_response(G, entity, user_query, client: OpenAI):

    dgar_context = adaptive_temporal_replay(G, entity)
    
    if not dgar_context:
        return "ERROR: Entity not found in the Knowledge Graph. Cannot ground response."
        
    augmented_prompt = f"""
    You are an expert fact-checker. Use the following verified Knowledge Graph context 
    to answer the user's question. Do not use any external knowledge. 
    If the context is insufficient, state that clearly.
    
    --- KG CONTEXT ---
    {dgar_context}
    ---
    
    USER QUESTION: {user_query}
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": augmented_prompt}]
    )
    
    return response.choices[0].message.content
