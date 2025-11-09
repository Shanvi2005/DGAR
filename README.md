DGAR: Directed Graph-Augmented Retrieval (Temporal RAG System)
A Temporal Retrieval-Augmented Generation (T-RAG) framework using a Directed Knowledge Graph (DGAR) to reduce LLM hallucination and temporal drift through chronological fact grounding.
StatusData ScaleDeploymentLicenseOperational9 time-stamped entitiesDockerized (Neo4j + Gemini API)MIT

1. Problem and Motivation
1.1 Issue: Temporal Drift in LLMs
Standard RAG pipelines rely on semantic embeddings. They fail to reason over time-sensitive or evolving information.
Example failure:

“Who was TechCorp’s CEO before 2024?”
A baseline LLM often merges outdated and new facts, hallucinating a single timeline.

1.2 DGAR Objective: Chronological Grounding
DGAR enforces temporal consistency through:


Directed Graph ETL: Extracts entities and relations with precise timestamps.


Temporal Retrieval: Orders multi-hop relations chronologically before generation.


Grounded Response: LLM answers only using time-sorted graph context, reducing ambiguity.



2. System Design Overview
2.1 Architecture Diagram
Raw Corpus → Extraction Engine → Temporal KG (Neo4j)
                    ↓
              Retrieval Engine
                    ↓
           Chronologically Ordered Context
                    ↓
                 LLM (Gemini)

2.2 Module and Data Flow
ComponentTechnologyPathFunctionKnowledge GraphNeo4j (Docker)N/AStores entities (Person, Company) and timestamped edges (APPOINTED, FOUNDED).Extraction EngineGemini 2.5 FlashKnowledge_Graph_ETL/extractor.pyConverts text corpus → JSON triplets ([Subject, Type, Relation, Object, Type, Timestamp]).Retrieval EnginePython, Neo4j DriverDGAR_Retrieval_Engine/dgar_logic.pyPerforms temporal traversal and sorts results (ORDER BY timestamp ASC).GeneratorGemini 2.5 FlashDGAR_Retrieval_Engine/retriever.pyProduces final grounded answer from ordered facts.

3. Core Retrieval Logic (Cypher Query)
// Chronologically constrained entity retrieval
MATCH (s)-[r]->(o)
WHERE (s.name = $entity OR o.name = $entity)
  AND EXISTS(r.timestamp)
RETURN s.name AS source,
       type(r) AS relation,
       o.name AS target,
       toString(r.timestamp) AS date
ORDER BY r.timestamp ASC;


4. Deployment
Prerequisites: Docker Desktop, Python ≥3.9
Steps:
git clone https://github.com/yourusername/DGAR-Project.git
cd DGAR-Project
cp .env.example .env  # Add GEMINI_API_KEY
docker-compose up -d  # Launch Neo4j container
python Knowledge_Graph_ETL/extractor.py  # Run data ingestion
python DGAR_Retrieval_Engine/retriever.py  # Test retrieval and generation


5. Verification Example
Query:
What was TechCorp's main product before Project Nova, and who was the CEO in 2024?
DGAR Output:

Based only on time-stamped graph data: Before Project Nova (2024-03-15), TechCorp's main product was ProductX. Marcus Jones became CEO on 2025-02-10. No CEO listed for 2024.


6. Planned Enhancements


Quantitative evaluation: accuracy vs. baseline RAG


Temporal conflict detection for overlapping timestamps


Vector + Graph hybrid retrieval


Integration with LangChain for modular testing


Auto-validation of extracted triplets



7. Repository Structure
DGAR-Project/
├── Knowledge_Graph_ETL/
│   └── extractor.py
├── DGAR_Retrieval_Engine/
│   ├── dgar_logic.py
│   └── retriever.py
├── docker-compose.yml
├── .env.example
└── README.md


8. License
MIT License © 2025 Shanvi
