"""Response formatting helpers for the LangChain RAG API."""

CHAIN_EXPRESSION = "ChatPromptTemplate | ChatOllama | StrOutputParser"

COMPONENTS = {
    "vector_store": "Chroma",
    "retrieval_method": "similarity_search_with_score",
    "prompt_template": "ChatPromptTemplate",
    "chat_model": "ChatOllama",
    "output_parser": "StrOutputParser",
}

SCORE_TYPE = "Chroma distance; lower usually means closer in this lesson setup"

FALLBACK_ANSWER = (
    "I do not have enough approved runbook context to answer that reliably."
)


def format_sources(scored_documents):
    """Format retrieved documents as source metadata for the API response."""
    sources = []
    for doc, score in scored_documents:
        metadata = doc.metadata or {}
        source_dict = {
            "source_id": metadata.get("source_id") or "unknown",
            "title": metadata.get("title") or "Untitled",
            "category": metadata.get("category") or "Uncategorized",
            "section": metadata.get("section") or "Unspecified",
            "chunk_id": metadata.get("chunk_id") or "unknown",
            "distance": round(score, 4) if score is not None else 0.0,
        }
        sources.append(source_dict)
    return sources


def format_langchain_debug(scored_documents, context, top_k, fallback):
    """Return LangChain debug metadata for inspectability."""
    chunk_ids = []
    for doc, _ in scored_documents:
        metadata = doc.metadata or {}
        chunk_ids.append(metadata.get("chunk_id") or "unknown")

    return {
        "chain_expression": CHAIN_EXPRESSION,
        "components": COMPONENTS,
        "retrieved_count": len(scored_documents),
        "retrieved_chunk_ids": chunk_ids,
        "top_k": top_k,
        "context_characters": len(context) if context else 0,
        "fallback": fallback,
        "score_type": SCORE_TYPE,
    }


def format_success_response(answer, sources, debug):
    """Format a successful RAG response."""
    return {
        "answer": answer.strip() if answer else "",
        "sources": sources,
        "langchain": debug,
    }


def format_fallback_response(debug):
    """Format a safe response when no usable context is available."""
    debug["fallback"] = True
    return {
        "answer": FALLBACK_ANSWER,
        "sources": [],
        "langchain": debug,
    }


def format_error_response(error, message):
    """Format an API error response."""
    return {
        "error": error,
        "message": message,
    }
