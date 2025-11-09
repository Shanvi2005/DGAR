**<span style="text-decoration:underline;">DGAR: Directed Graph-Augmented Retrieval (Temporal RAG System)</span>**

A Temporal Retrieval-Augmented Generation (T-RAG) framework using a Directed Knowledge Graph (DGAR) to reduce LLM hallucination and temporal drift through chronological fact grounding.


<table>
  <tr>
   <td>Status
   </td>
   <td>Data Scale
   </td>
   <td>Deployment
   </td>
   <td>License
   </td>
  </tr>
  <tr>
   <td>Operational
   </td>
   <td>9 time-stamped entities
   </td>
   <td>Dockerized (Neo4j + Gemini API)
   </td>
   <td>MIT
   </td>
  </tr>
</table>


**<span style="text-decoration:underline;">1. Problem and Motivation</span>**

**<span style="text-decoration:underline;">1.1 Issue: Temporal Drift in LLMs</span>**

Standard RAG pipelines rely on semantic embeddings. They fail to reason over time-sensitive or evolving information.

Example failure:

“Who was TechCorp’s CEO before 2024?”

A baseline LLM often merges outdated and new facts, hallucinating a single timeline.

**<span style="text-decoration:underline;">1.2 DGAR Objective: Chronological Grounding</span>**

DGAR enforces temporal consistency through:



* <span style="text-decoration:underline;">Directed Graph ETL</span>: Extracts entities and relations with precise timestamps.
* <span style="text-decoration:underline;">Temporal Retrieval</span>: Orders multi-hop relations chronologically before generation.
* <span style="text-decoration:underline;">Grounded Response</span>: LLM answers only using time-sorted graph context, reducing ambiguity.

**<span style="text-decoration:underline;">2. System Design Overview</span>**

**<span style="text-decoration:underline;">2.1 Architecture Diagram</span>**

Raw Corpus → Extraction Engine → Temporal KG (Neo4j)

                    ↓

              Retrieval Engine

                    ↓

           Chronologically Ordered Context

                    ↓

                 LLM (Gemini)

**<span style="text-decoration:underline;">2.2 Module and Data Flow</span>**


<table>
  <tr>
   <td>Component
   </td>
   <td>Technology
   </td>
   <td>Path
   </td>
   <td>Function
   </td>
  </tr>
  <tr>
   <td>Knowledge Graph
   </td>
   <td>Neo4j(Docker)
   </td>
   <td>N/A
   </td>
   <td>Stores entities (`Person`, `Company`) and timestamped edges (`APPOINTED`, `FOUNDED`).
   </td>
  </tr>
  <tr>
   <td>Extraction Engine
   </td>
   <td>Gemini 2.5 Flash 
   </td>
   <td>Knowledge_Graph_ETL/extractor.py
   </td>
   <td>Converts text corpus → JSON triplets (`[Subject, Type, Relation, Object, Type, Timestamp]`).
   </td>
  </tr>
  <tr>
   <td>Retrieval Engine
   </td>
   <td>Python, Neo4j Driver
   </td>
   <td>DGAR_Retrieval_Engine/dgar_logic.py
   </td>
   <td>Performs temporal traversal and sorts results (`ORDER BY timestamp ASC`).
   </td>
  </tr>
  <tr>
   <td>Generator 
   </td>
   <td> Gemini 2.5 Flash
   </td>
   <td>DGAR_Retrieval_Engine/retriever.py
   </td>
   <td>Produces a final grounded answer from ordered facts.
   </td>
  </tr>
</table>


**<span style="text-decoration:underline;">3. Core Retrieval Logic (Cypher Query)</span>**

// Chronologically constrained entity retrieval

MATCH (s)-[r]->(o)

WHERE (s.name = $entity OR o.name = $entity)

  AND EXISTS(r.timestamp)

RETURN s.name AS source,

       type(r) AS relation,

       o.name AS target,

       toString(r.timestamp) AS date

ORDER BY r.timestamp ASC;

**<span style="text-decoration:underline;">4. Deployment</span>**

Prerequisites: Docker Desktop, Python ≥3.9

**Steps:**

git clone https://github.com/Shanvi2005/DGAR.git

cd DGAR-Project

cp .env.example .env  # Add GEMINI_API_KEY

docker-compose up -d  # Launch Neo4j container

python Knowledge_Graph_ETL/extractor.py  # Run data ingestion

python DGAR_Retrieval_Engine/retriever.py  # Test retrieval and generation

**<span style="text-decoration:underline;">5. Verification Example</span>**

**Query:**

What was TechCorp's main product before Project Nova, and who was the CEO in 2024?

**DGAR Output:**

Based only on time-stamped graph data: Before Project Nova (2024-03-15), TechCorp's main product was ProductX. Marcus Jones became CEO on 2025-02-10. No CEO listed for 2024.

**<span style="text-decoration:underline;">6. Planned Enhancements</span>**

Quantitative evaluation: accuracy vs. baseline RAG

Temporal conflict detection for overlapping timestamps

Vector + Graph hybrid retrieval

Integration with LangChain for modular testing

Auto-validation of extracted triplets

**<span style="text-decoration:underline;">7. Repository Structure</span>**

DGAR-Project/

├── Knowledge_Graph_ETL/

│   └── extractor.py

├── DGAR_Retrieval_Engine/

│   ├── dgar_logic.py

│   └── retriever.py

├── docker-compose.yml

├── .env.example

└── README.md

**<span style="text-decoration:underline;">8. License</span>**

MIT License © 2025 Shanvi
