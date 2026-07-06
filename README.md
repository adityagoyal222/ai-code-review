# AI Code Review Assistant 🔍

A GenAI proof-of-concept that performs **grounded, citation-backed code reviews** using a local tool-calling agent, a RAG pipeline over your own documentation, and locally-hosted LLMs via Ollama — no cloud API calls, fully reproducible on a dev machine.

## Why this exists

Most AI code review demos hallucinate suggestions with no grounding in actual project standards. This PoC forces every review to **cite retrieved documentation**, keeping feedback traceable and auditable — a lightweight blueprint for how tool-calling + RAG can make LLM output trustworthy enough for real dev workflows.

## How it works

- **FastAPI** service exposing `/ingest` (index your docs) and `/review` (submit code for review)
- A **deterministic tool router** triggers the `retrieve_docs` tool automatically to ground each review
- **Chroma** persists embeddings locally — no external vector DB needed
- **Ollama** (Qwen2.5-Coder 7B + Nomic-Embed-Text) generates review output strictly grounded in retrieved docs
- A minimal HTML UI posts code to `/review` and renders the Markdown response

## Prompting approach

- Strict grounding policy — reviews must cite the docs they're based on
- Structured output format: **findings → risks → suggested fixes**
- Iterated specifically to reduce hallucination, with explicit uncertainty notes when evidence is thin

## Quick start

```bash
# 1. Python 3.11 recommended
pip install -r requirements.txt

# 2. Pull local models
ollama pull qwen2.5-coder:7b
ollama pull nomic-embed-text

# 3. Configure
cp .env.example .env

# 4. Ingest your domain docs
python -m app.rag.ingest --reset

# 5. Run
uvicorn app.main:app --reload
```

Open **http://localhost:8000** to use the UI.

## Evaluation

A small regression suite checks output quality on predefined cases:

```bash
python -m eval.run_eval
```

## Configuration

Edit `.env` to adjust model names, vector store location, retrieval top-k, and max embedding query length.

## Status

Local-only proof-of-concept — not production-hardened. Swap in your own domain docs under `data/seed_docs/` for better-grounded reviews.
