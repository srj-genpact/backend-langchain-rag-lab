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

    # TODO: Return a list of dictionaries.
    # Each dictionary should include source_id, title, category, section,
    # chunk_id, and distance.
    # Do not include full document text in the source list.
    raise NotImplementedError("Format source metadata.")


def format_langchain_debug(scored_documents, context, top_k, fallback):
    """Return LangChain debug metadata for inspectability."""

    # TODO: Return chain expression, component names, retrieved count,
    # retrieved chunk IDs, top_k, context length, fallback status, and score type.
    raise NotImplementedError("Format LangChain debug metadata.")


def format_success_response(answer, sources, debug):
    """Format a successful RAG response."""

    # TODO: Return a dictionary with answer, sources, and langchain.
    raise NotImplementedError("Format a success response.")


def format_fallback_response(debug):
    """Format a safe response when no usable context is available."""

    # TODO: Return a response with FALLBACK_ANSWER, empty sources, and debug.
    raise NotImplementedError("Format a fallback response.")


def format_error_response(error, message):
    """Format an API error response."""

    # TODO: Return a dictionary with error and message.
    raise NotImplementedError("Format an error response.")
