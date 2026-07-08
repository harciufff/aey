# Neuro-Symbolic GraphRAG Assistant (Core Engine)

A modular Python implementation exploring the convergence of **Connectionist (Neural)** and **Symbolic (Logical)** Artificial Intelligence. This framework builds a structure-centric GraphRAG knowledge base inspired by Luhmann's Zettelkasten methodology, completely bypassing the token bloat and scalability limits of traditional text-centric wiki setups.

This repository contains the **Core CLI Engine**, featuring localized background ingestion and an interactive terminal-based reasoning chat loop.

## Architectural Vision & Core Innovation
Most AI knowledge assistants (including standard LLM Wikis) are **Text-Centric**: they dump raw markdown files into a vector store. When scaled to thousands of notes, this approach triggers context-window exhaustion, high API costs, and semantic drift (duplication).

This project shifts the paradigm to a **Structure-Centric** model:
* **Neural Component (System 1 - Intuition):** Google Gemini handles unstructured raw web data parsing and semantic intent translation.
* **Symbolic Component (System 2 - Logic):** Neo4j acts as a deterministic relational memory. Knowledge is stored as mathematical nodes and strict, typed semantic edges (`EXTENDS`, `CONTRADICTS`, `SUPPORTS`).

### The Neuro-Symbolic Inference Advantage
When a user asks a multi-hop question, the system uses embedding vectors to pinpoint the exact core entity inside Neo4j, then mathematically traverses the adjacent graph topology. The LLM is forced to reason **only** over the extracted deterministic facts. If a connection doesn't logically exist in the graph database, the engine enforces a hard constraint, outputting an anti-hallucination guardrail response: *"I don't have enough information in the knowledge graph."*

## Infrastructure Stack
* **Orchestration:** LangChain Ecosystem (Custom Vector & Graph Information Retrieval)
* **LLM Engine:** Google Gemini API (`langchain-google-genai`)
* **Embedding Model:** `models/gemini-embedding-001` (Optimized for textual semantic searches)
* **Data Scraper:** Crawl4AI (Asynchronous, headless browser extraction engine)
* **Graph Database:** Neo4j DBMS (Local transactional Bolt protocol)

## Project Structure & Modules
* `main.py` - Single execution entry point. Orchestrates the pipeline via CLI flags.
* `config.py` - Central configuration manager. Loads environments and enforces allowed semantic relations.
* `database.py` - Manages Neo4j transactional driver lifecycles and provides a safe graph reset routine.
* `crawler.py` - Non-blocking asynchronous scraper utilizing Crawl4AI to target remote documentation.
* `ingestion.py` - Extracts entity-relationship triples using LangChain's `LLMGraphTransformer`.
* `search.py` - Custom GraphRAG hybrid retrieval engine combining vector similarity and neighbor traversal.

## Setup and Execution

### 1. Environment Configuration
Create a `.env` file in the root directory:
```text
GOOGLE_API_KEY=your_gemini_api_key_here
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_secure_password
SITI_DA_SCANSIONARE= https://karpathy.github.io/2026/02/12/microgpt/      # Websites to scan
```

### 2. Run Ingestion Flow (Nightly Auto-Learning Mode)
To spin up the async crawler, ingest web targets, extract triple constraints, and compile the local Neo4j topology, execute:
```bash
python3 main.py --cron
```

### 3. Run Interactive Chat Flow (Reasoning Mode)
To launch the interactive, terminal-based query engine and talk directly to your graph geometry without hallucination risks, run:
```bash
python3 main.py
```

## Verification Queries (Neo4j Browser)
To inspect the structural network compiled by the neural translator, log into `http://localhost:7474` and execute:
```cypher
// Visualize the top connected semantic entities and relationships
MATCH (a)-[r]->(b) RETURN a, r, b LIMIT 50
```
