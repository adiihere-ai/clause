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
        extra="ignore"
    )

    # App
    app_name: str = "Clause"
    data_path: str = "files/shop_handbook.pdf"

    # # Chat
    # chat_model: str = "gemma3:1b"
    # chat_provider: str = "ollama"
    # chat_temperature: float = 0.1

    # Chat
    chat_model: str = "gemini-3.5-flash-lite"
    chat_provider: str = "google_genai"
    chat_temperature: float = 0.1
    # Google API key
    google_api_key: str = ""


    # Embeddings
    embeded_provider: str = "ollama"
    embeded_model: str = "nomic-embed-text:latest"
    embeded_dim: int = 768

    # Indexing
    chunk_size: int = 600
    chunk_overlap: int = 100

    # Retrieval
    top_k: int = 3
    threshold_score: float = 0.5

    # Qdrant
    collection: str = "shop_handbook"
    qdrant_data: str = "./vector_stores"
    qdrant_url: str | None = None

    # Prompts
    system_prompt: str = (
        "You are the Clause shop customer assistant. "
        "Answer using ONLY the handbook text you are given. "
        "Find the one sentence that answers the question and copy its numbers exactly. "
        "Answer in one or two short sentences. Never mention 'the context' or 'the handbook text'. "
        "If the handbook text does not answer the question, reply exactly: "
        "\"I don't know.\""
    )


@lru_cache
def get_settings():
    return Settings()


def get_embeddings(settings: Settings) -> Embeddings:
    return init_embeddings(
        model=settings.embeded_model,
        provider=settings.embeded_provider
    )


def get_qdrant_client(settings: Settings):
    return QdrantClient(
        path=settings.qdrant_data
    )
