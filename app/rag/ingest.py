import argparse
import os
import shutil
from typing import Dict, List

from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import Settings, get_settings


def load_seed_docs(seed_dir: str) -> List:
    loaders = [
        DirectoryLoader(seed_dir, glob="**/*.md", loader_cls=TextLoader),
        DirectoryLoader(seed_dir, glob="**/*.txt", loader_cls=TextLoader),
    ]

    documents = []
    for loader in loaders:
        documents.extend(loader.load())

    for doc in documents:
        source = doc.metadata.get("source")
        if source:
            doc.metadata["source"] = os.path.relpath(source, seed_dir)

    return documents


def split_docs(documents: List) -> List:
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = splitter.split_documents(documents)

    for idx, doc in enumerate(chunks):
        doc.metadata["chunk"] = idx

    return chunks


def run_ingest(settings: Settings, reset: bool = False) -> Dict[str, object]:
    if reset and os.path.isdir(settings.chroma_dir):
        shutil.rmtree(settings.chroma_dir)

    documents = load_seed_docs(settings.seed_docs_dir)
    chunks = split_docs(documents)

    embeddings = OllamaEmbeddings(
        base_url=settings.ollama_base_url,
        model=settings.ollama_embed_model,
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=settings.chroma_dir,
    )
    # Chroma persists automatically when persist_directory is set.

    return {
        "documents": len(documents),
        "chunks": len(chunks),
        "persist_dir": settings.chroma_dir,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest seed docs into Chroma")
    parser.add_argument("--reset", action="store_true", help="Clear existing store")
    args = parser.parse_args()

    settings = get_settings()
    result = run_ingest(settings, reset=args.reset)
    print(result)


if __name__ == "__main__":
    main()
