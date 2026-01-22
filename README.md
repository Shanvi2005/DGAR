# DGAR: Directed Graph-Augmented Retrieval

### A Temporal Retrieval-Augmented Generation (T-RAG) System

DGAR is a **Temporal Retrieval-Augmented Generation (T-RAG)** framework that reduces Large Language Model (LLM) hallucinations by enforcing **chronological fact grounding** using a **directed, time-stamped knowledge graph**.

Instead of asking the LLM to reason about timelines implicitly, DGAR **pushes temporal reasoning into the retrieval layer**, ensuring that answers are generated only from **time-ordered, verified facts**.

---

## 1. Problem & Motivation

### 1.1 Temporal Drift in Standard RAG

Most RAG systems retrieve documents based on **semantic similarity**, not **time validity**. As a result, LLMs often merge facts from different periods, leading to **timeline hallucinations**.

**Example failure:**

> *Who was TechCorp’s CEO before 2024?*

A baseline LLM or standard RAG pipeline may combine historical and future facts and hallucinate a single, incorrect answer.

---

### 1.2 DGAR Objective: Chronological Grounding

DGAR eliminates temporal ambiguity by enforcing:

* **Directed Graph ETL** — Extracts entities and relationships with explicit timestamps
* **Temporal Graph Retrieval** — Retrieves and orders facts chronologically *before* generation
* **Grounded Generation** — LLM answers strictly using time-sorted graph context

---

## 2. System Overview

### 2.1 High-Level Architecture

```
Raw Text Corpus
        ↓
LLM-based Structured Extraction
        ↓
Temporal Knowledge Graph (Neo4j)
        ↓
Chronologically Ordered Retrieval
        ↓
Grounded LLM Generation
```

---

### 2.2 Core Components

| Component         | Technology         | Purpose                                                      |
| ----------------- | ------------------ | ------------------------------------------------------------ |
| Knowledge Graph   | Neo4j (Dockerized) | Stores entities and **time-stamped, directed relationships** |
| Extraction Engine | Local LLM (Ollama) | Converts raw text into structured JSON triplets              |
| Validation Layer  | Python             | Filters malformed or implausible LLM outputs                 |
| Retrieval Engine  | Python + Neo4j     | Performs **temporal traversal and sorting**                  |
| Generator         | Local LLM (Ollama) | Generates answers **strictly grounded** in retrieved facts   |

---

## 3. Knowledge Representation

Each fact is stored as a **directed relationship with a timestamp**:

```
(Person) -[APPOINTED {timestamp}]-> (Company)
```

This design allows multiple historical states to coexist without overwriting each other.

---

## 4. Core Temporal Retrieval Logic

DGAR retrieves facts involving a queried entity and orders them **chronologically**:

```cypher
MATCH (s)-[r]->(o)
WHERE (s.name = $entity OR o.name = $entity)
  AND r.timestamp IS NOT NULL
RETURN
  s.name AS source,
  type(r) AS relationship,
  o.name AS target,
  toString(r.timestamp) AS date
ORDER BY r.timestamp ASC;
```

This guarantees that the LLM always receives a **linear, time-consistent history**.

---

## 5. Grounded Generation

The retrieved temporal context is injected into a **constrained prompt** that:

* Forbids use of external knowledge
* Allows explicit acknowledgement of missing information
* Prevents timeline reconstruction by the model

If sufficient information does not exist, the system **fails safely** instead of hallucinating.

---

## 6. Verification Example

**Query**

> *What was TechCorp’s main product before Project Nova, and who was the CEO in 2024?*

**DGAR Output**

> Based on time-stamped graph data:
>
> * Before Project Nova (2024-03-15), TechCorp’s main product was **ProductX**
> * **Marcus Jones** became CEO on **2025-02-10**
> * **No CEO is listed for 2024**

---

## 7. Repository Structure

```
DGAR/
├── data/
│   └── temporal_corpus.txt
├── dgar_core/
│   ├── db_connector.py
│   ├── extractor.py
│   └── validator.py
├── dgar_Retrieval_Engine/
│   └── dgar_logic.py
├── llm_interface/
│   └── generator.py
├── docker-compose.yml
├── main_ingestion.py
└── README.md
```

---

## 8. Deployment

### Prerequisites

* Python ≥ 3.9
* Docker Desktop
* Ollama

### Steps

```bash
git clone https://github.com/Shanvi2005/DGAR.git
cd DGAR

docker-compose up -d        # Start Neo4j
python main_ingestion.py    # Build temporal knowledge graph
```

---

## 9. Key Design Decisions

* Temporal reasoning is handled **before generation**, not inside the LLM
* All relationships require explicit timestamps
* LLM outputs are validated and sanitized before ingestion
* System prioritizes **correctness and transparency** over forced answers

---

## 10. Limitations & Future Work

* Quantitative evaluation against baseline RAG
* Temporal conflict detection for overlapping facts
* Vector + graph hybrid retrieval
* Support for time ranges (before / after / during)
* Automated extraction quality scoring

---

## 11. License

MIT License © 2025 Shanvi
