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

    # TODO: Import ChatOllama from langchain_ollama.
    # TODO: Return ChatOllama(model=CHAT_MODEL, temperature=0).
    raise NotImplementedError("Build the ChatOllama model wrapper.")


def build_chain():
    """Build the LangChain prompt to model to parser sequence."""

    # TODO: Import StrOutputParser from langchain_core.output_parsers.
    # TODO: Import build_rag_prompt from lib.prompt_templates.
    # TODO: Build this sequence:
    # prompt_template = build_rag_prompt()
    # llm = build_chat_model()
    # return prompt_template | llm | StrOutputParser()
    raise NotImplementedError("Build the LangChain runnable sequence.")


def has_usable_context(scored_documents):
    """Return True when retrieval produced at least one document with text."""

    # TODO: Return False for an empty list.
    # TODO: Return True only if at least one document has non-blank page_content.
    raise NotImplementedError("Check whether retrieved context is usable.")


def format_context(scored_documents):
    """Format retrieved LangChain documents into prompt-ready context text."""

    # TODO: Build a readable context block for each retrieved document.
    # Include source_id, title, category, section, chunk_id, distance, and text.
    raise NotImplementedError("Format retrieved documents into prompt context.")


def answer_question(
    question,
    *,
    vector_store=None,
    chain=None,
    top_k=DEFAULT_TOP_K,
):
    """Run the LangChain-supported RAG workflow for one validated question."""

    # TODO: Strip the question.
    # TODO: Retrieve scored documents.
    # TODO: If no usable context exists, return a safe fallback without calling the chain.
    # TODO: Format the context.
    # TODO: Build or use the provided chain.
    # TODO: Invoke the chain with {"context": context, "question": cleaned_question}.
    # TODO: Reject empty model output.
    # TODO: Format sources and LangChain debug metadata.
    # TODO: Return the success response.
    # TODO: Wrap unexpected exceptions in LangChainServiceError.
    raise NotImplementedError("Run the LangChain RAG service.")
