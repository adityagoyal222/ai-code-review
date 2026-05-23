from typing import List

from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings

from app.config import Settings


def get_vectorstore(settings: Settings) -> Chroma:
    embeddings = OllamaEmbeddings(
        base_url=settings.ollama_base_url,
        model=settings.ollama_embed_model,
    )
    return Chroma(
        persist_directory=settings.chroma_dir,
        embedding_function=embeddings,
    )


def get_retriever(settings: Settings):
    vectorstore = get_vectorstore(settings)
    return vectorstore.as_retriever(search_kwargs={"k": settings.top_k})


def format_docs(docs: List) -> str:
    formatted = []
    for doc in docs:
        source = doc.metadata.get("source", "unknown")
        chunk = doc.metadata.get("chunk", 0)
        formatted.append(f"[source:{source}#chunk{chunk}]\n{doc.page_content}")
    return "\n\n".join(formatted)
