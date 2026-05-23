# AI Code Review Assistant (PoC)

GenAI-powered proof-of-concept that implements tool-calling agent architecture, a RAG pipeline, and prompt engineering for grounded code reviews using local Ollama models.

## Why this exists
- Demonstrate a local, grounded code review flow using domain-specific docs
- Provide a lightweight API + UI for end-to-end reviews
- Keep the system reproducible and easy to run on a developer machine

## Quick start
0) Recommended Python version

Use Python 3.11 for best dependency compatibility.

1) Install dependencies
```
pip install -r requirements.txt
```

2) Start Ollama and pull models
```
ollama pull qwen2.5-coder:7b
ollama pull nomic-embed-text
```

3) Copy environment config
```
cp .env.example .env
```

4) Ingest seed docs
```
python -m app.rag.ingest --reset
```

5) Run the API
```
uvicorn app.main:app --reload
```

6) Open the UI in a browser at http://localhost:8000

## Architecture
- FastAPI service exposes /ingest and /review endpoints
- Deterministic tool router triggers the retrieve_docs tool for grounding
- Chroma local vector store persists embeddings
- Ollama LLM generates review output grounded in retrieved docs
- Minimal HTML UI posts code to the review endpoint and renders Markdown

## Prompting approach
- Uses a strict grounding policy: reviews must cite retrieved docs
- Includes a structured review format with findings, risks, and suggested fixes
- Iterated to reduce hallucinations by emphasizing citations and uncertainty notes

## Evaluation
Run a small regression check on predefined cases:
```
python -m eval.run_eval
```

## Configuration
Edit .env to adjust:
- model names
- vector store location
- top-k retrieval
- max query length for embeddings

## Notes
- This is a local-only PoC and not intended for production use
- Replace seed docs with your domain docs for better grounding
