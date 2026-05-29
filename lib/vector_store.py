"""Vector store and retrieval helpers."""

from lib.config import (
    CHROMA_PATH,
    COLLECTION_NAME,
    DEFAULT_TOP_K,
    EMBEDDING_MODEL,
)


def build_embeddings():
    """Build the local Ollama embeddings object used by Chroma."""

    # TODO: Import OllamaEmbeddings from langchain_ollama.
    # TODO: Return OllamaEmbeddings(model=EMBEDDING_MODEL).
    raise NotImplementedError("Build Ollama embeddings.")


def build_vector_store():
    """Build the Chroma vector store used by the RAG pipeline."""

    # TODO: Import Chroma from langchain_chroma.
    # TODO: Return a Chroma vector store configured with:
    # - collection_name=COLLECTION_NAME
    # - persist_directory=CHROMA_PATH
    # - embedding_function=build_embeddings()
    raise NotImplementedError("Build the Chroma vector store.")


def retrieve_context(question, *, vector_store=None, top_k=DEFAULT_TOP_K):
    """Retrieve scored documents for a question."""

    # TODO: Reject blank questions.
    # TODO: Use the provided vector_store or build_vector_store().
    # TODO: Call similarity_search_with_score(question, k=top_k).
    raise NotImplementedError("Retrieve context from the vector store.")
