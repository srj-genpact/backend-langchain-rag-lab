from lib.response_formatter import (
    CHAIN_EXPRESSION,
    COMPONENTS,
    FALLBACK_ANSWER,
    format_error_response,
    format_fallback_response,
    format_langchain_debug,
    format_sources,
    format_success_response,
)
from tests.fakes import FakeDocument


def sample_scored_documents():
    return [
        (
            FakeDocument(
                "Pause deployments and prepare rollback.",
                {
                    "source_id": "REL-101",
                    "title": "Checkout API Error Spike Runbook",
                    "category": "Reliability",
                    "section": "Mitigation",
                    "chunk_id": "chunk-rel-101-b",
                },
            ),
            0.123456,
        )
    ]


def test_format_sources_returns_metadata_without_document_text():
    sources = format_sources(sample_scored_documents())

    assert sources == [
        {
            "source_id": "REL-101",
            "title": "Checkout API Error Spike Runbook",
            "category": "Reliability",
            "section": "Mitigation",
            "chunk_id": "chunk-rel-101-b",
            "distance": 0.1235,
        }
    ]
    assert "page_content" not in sources[0]
    assert "text" not in sources[0]


def test_format_sources_uses_defaults_for_missing_metadata():
    sources = format_sources([(FakeDocument("Some text", {}), 0.9)])

    assert sources[0]["source_id"] == "unknown"
    assert sources[0]["title"] == "Untitled"
    assert sources[0]["category"] == "Uncategorized"
    assert sources[0]["section"] == "Unspecified"
    assert sources[0]["chunk_id"] == "unknown"
    assert sources[0]["distance"] == 0.9


def test_format_langchain_debug_returns_expected_metadata():
    context = "Context text"
    debug = format_langchain_debug(
        sample_scored_documents(),
        context=context,
        top_k=3,
        fallback=False,
    )

    assert debug["chain_expression"] == CHAIN_EXPRESSION
    assert debug["components"] == COMPONENTS
    assert debug["retrieved_count"] == 1
    assert debug["retrieved_chunk_ids"] == ["chunk-rel-101-b"]
    assert debug["top_k"] == 3
    assert debug["context_characters"] == len(context)
    assert debug["fallback"] is False
    assert "distance" in debug["score_type"].lower()


def test_format_success_response_returns_stable_shape():
    sources = format_sources(sample_scored_documents())
    debug = format_langchain_debug(sample_scored_documents(), "abc", 3, False)

    response = format_success_response("  Follow the runbook.  ", sources, debug)

    assert response["answer"] == "Follow the runbook."
    assert response["sources"] == sources
    assert response["langchain"] == debug
    assert set(response.keys()) == {"answer", "sources", "langchain"}


def test_format_fallback_response_returns_safe_answer_and_empty_sources():
    debug = format_langchain_debug([], "", 3, True)

    response = format_fallback_response(debug)

    assert response["answer"] == FALLBACK_ANSWER
    assert response["sources"] == []
    assert response["langchain"]["fallback"] is True


def test_format_error_response_returns_error_shape():
    response = format_error_response("invalid_request", "Request body must be JSON.")

    assert response == {
        "error": "invalid_request",
        "message": "Request body must be JSON.",
    }
