"""LangChain-supported RAG workflow service."""

from lib.config import CHAT_MODEL, DEFAULT_TOP_K
from lib.response_formatter import (
    format_fallback_response,
    format_langchain_debug,
    format_sources,
    format_success_response,
)
from lib.vector_store import retrieve_context


class LangChainServiceError(Exception):
    """Raised when the LangChain RAG service cannot complete a request."""


def build_chat_model():
    """Build the local chat model wrapper."""
    from langchain_ollama import ChatOllama

    return ChatOllama(model=CHAT_MODEL, temperature=0)


def build_chain():
    """Build the LangChain prompt to model to parser sequence."""
    from langchain_core.output_parsers import StrOutputParser
    from lib.prompt_templates import build_rag_prompt

    prompt_template = build_rag_prompt()
    llm = build_chat_model()
    return prompt_template | llm | StrOutputParser()


def has_usable_context(scored_documents):
    """Return True when retrieval produced at least one document with text."""
    if not scored_documents:
        return False
    for doc, _ in scored_documents:
        if doc.page_content and doc.page_content.strip():
            return True
    return False


def format_context(scored_documents):
    """Format retrieved LangChain documents into prompt-ready context text."""
    blocks = []
    for i, (doc, score) in enumerate(scored_documents, 1):
        metadata = doc.metadata or {}
        source_id = metadata.get("source_id") or "unknown"
        title = metadata.get("title") or "Untitled"
        category = metadata.get("category") or "Uncategorized"
        section = metadata.get("section") or "Unspecified"
        chunk_id = metadata.get("chunk_id") or "unknown"
        distance = f"{score:.4f}" if score is not None else "0.0000"

        block = (
            f"[Context {i}]\n"
            f"Source ID: {source_id}\n"
            f"Title: {title}\n"
            f"Category: {category}\n"
            f"Section: {section}\n"
            f"Chunk ID: {chunk_id}\n"
            f"Distance: {distance}\n"
            f"Text: {doc.page_content}"
        )
        blocks.append(block)
    return "\n\n".join(blocks)


def answer_question(
    question,
    *,
    vector_store=None,
    chain=None,
    top_k=DEFAULT_TOP_K,
):
    """Run the LangChain-supported RAG workflow for one validated question."""
    try:
        cleaned_question = question.strip() if question else ""

        # Retrieve scored documents
        try:
            scored_documents = retrieve_context(
                cleaned_question, vector_store=vector_store, top_k=top_k
            )
        except Exception as e:
            raise LangChainServiceError(f"Vector store unavailable: {str(e)}") from e

        # If no usable context exists, return a safe fallback without calling the chain
        if not has_usable_context(scored_documents):
            debug = format_langchain_debug(scored_documents, "", top_k, True)
            return format_fallback_response(debug)

        # Format the context
        context = format_context(scored_documents)

        # Build or use the provided chain
        if chain is None:
            chain = build_chain()

        # Invoke the chain
        try:
            answer = chain.invoke(
                {"context": context, "question": cleaned_question}
            )
        except Exception as e:
            raise LangChainServiceError(f"Chain invocation failed: {str(e)}") from e

        # Reject empty model output
        if not answer or not answer.strip():
            raise LangChainServiceError("Received an empty answer from the model.")

        # Format sources and LangChain debug metadata
        sources = format_sources(scored_documents)
        debug = format_langchain_debug(scored_documents, context, top_k, False)

        # Return the success response
        return format_success_response(answer, sources, debug)

    except LangChainServiceError:
        raise
    except Exception as e:
        raise LangChainServiceError(str(e)) from e
