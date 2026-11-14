from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from langchain.embeddings import init_embeddings
from langchain_core.embeddings import Embeddings
from qdrant_client import QdrantClient


ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="RAG_",
        env_file=ENV_FILE,
        extra="ignore",
    )

    app_name: str = "Clause"
    data_path: str = "files/shop_handbook.pdf"

    chat_model: str = "gemini-3.5-flash-lite"
    chat_provider: str = "google_genai"
    chat_temperature: float = 0.1
    google_api_key: str = ""

    embeded_provider: str = "ollama"
    embeded_model: str = "nomic-embed-text:latest"
    embeded_dim: int = 768

    chunk_size: int = 600
    chunk_overlap: int = 100

    top_k: int = 3
    threshold_score: float = 0.5

    collection: str = "shop_handbook"
    qdrant_data: str = "./vector_stores"
    qdrant_url: str | None = None

    system_prompt: str = (
        "You are the Clause shop customer assistant. "
        "Answer using ONLY the handbook text you are given. "
        "Find the one sentence that answers the question and copy its numbers exactly. "
        "Answer in one or two short sentences. Never mention 'the context' or 'the handbook text'. "
        "If the handbook text does not answer the question, reply exactly: "
        "\"I don't know.\""
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_embeddings(settings: Settings) -> Embeddings:
    return init_embeddings(
        model=settings.embeded_model,
        provider=settings.embeded_provider,
    )


def get_qdrant_client(settings: Settings) -> QdrantClient:
    return QdrantClient(path=settings.qdrant_data)
