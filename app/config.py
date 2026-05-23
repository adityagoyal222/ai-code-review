from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5-coder:7b"
    ollama_embed_model: str = "nomic-embed-text"

    chroma_dir: str = "./data/chroma"
    seed_docs_dir: str = "./data/seed_docs"
    top_k: int = 4
    max_query_chars: int = 2000


def get_settings() -> Settings:
    return Settings()
