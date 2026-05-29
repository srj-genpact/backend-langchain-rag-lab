"""Document loading helpers for runbook chunks."""

from dataclasses import dataclass
import json

from lib.config import DATA_PATH


@dataclass
class SimpleDocument:
    """Fallback document shape used when LangChain is unavailable."""

    page_content: str
    metadata: dict


def load_runbook_chunks(path=DATA_PATH):
    """Load runbook chunks from JSON."""

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def chunks_to_documents(chunks):
    """Convert runbook chunk dictionaries into LangChain Document objects."""

    try:
        from langchain_core.documents import Document
    except ImportError:
        Document = SimpleDocument

    documents = []
    for chunk in chunks:
        metadata = {
            "source_id": chunk.get("source_id"),
            "title": chunk.get("title"),
            "category": chunk.get("category"),
            "section": chunk.get("section"),
            "chunk_id": chunk.get("chunk_id"),
        }
        documents.append(Document(page_content=chunk.get("text", ""), metadata=metadata))

    return documents
