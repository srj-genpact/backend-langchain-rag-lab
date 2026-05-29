"""Configuration values for the LangChain RAG lab."""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "runbook_chunks.json"
CHROMA_PATH = os.getenv("CHROMA_PATH", str(BASE_DIR / "chroma_db"))
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "reliability_runbooks")

EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "embeddinggemma")
CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "llama3.2")

DEFAULT_TOP_K = int(os.getenv("RAG_TOP_K", "3"))
MIN_QUESTION_LENGTH = 3
MAX_QUESTION_LENGTH = 500
