from typing import Dict, List

from app.config import Settings
from app.rag.retriever import format_docs, get_retriever


def plan_tools(_: str) -> List[str]:
    # Deterministic tool planning keeps the PoC stable for local models.
    return ["retrieve_docs"]


def run_tools(settings: Settings, code: str) -> Dict[str, str]:
    retriever = get_retriever(settings)
    query = code[: settings.max_query_chars]
    docs = retriever.get_relevant_documents(query)
    return {"context": format_docs(docs)}
