import pytest

from lib.langchain_rag_service import (
    LangChainServiceError,
    answer_question,
    format_context,
    has_usable_context,
)
from tests.fakes import BrokenVectorStore, FakeChain, FakeDocument, FakeVectorStore


def scored_documents():
    return [
        (
            FakeDocument(
                "Pause additional deployments and prepare rollback.",
                {
                    "source_id": "REL-101",
                    "title": "Checkout API Error Spike Runbook",
                    "category": "Reliability",
                    "section": "Mitigation",
                    "chunk_id": "chunk-rel-101-b",
                },
            ),
            0.12,
        ),
        (
            FakeDocument(
                "Assign an incident lead before rollback.",
                {
                    "source_id": "REL-102",
                    "title": "Rollback Coordination Runbook",
                    "category": "Reliability",
                    "section": "Rollback Steps",
                    "chunk_id": "chunk-rel-102-a",
                },
            ),
            0.18,
        ),
    ]


def test_has_usable_context_requires_at_least_one_document_with_text():
    assert has_usable_context([]) is False
    assert has_usable_context([(FakeDocument("   ", {}), 0.1)]) is False
    assert has_usable_context([(FakeDocument("Use the runbook.", {}), 0.1)]) is True


def test_format_context_includes_metadata_and_document_text():
    context = format_context(scored_documents())

    assert "[Context 1]" in context
    assert "Source ID: REL-101" in context
    assert "Title: Checkout API Error Spike Runbook" in context
    assert "Category: Reliability" in context
    assert "Section: Mitigation" in context
    assert "Chunk ID: chunk-rel-101-b" in context
    assert "Distance: 0.1200" in context
    assert "Pause additional deployments" in context


def test_answer_question_invokes_chain_with_context_and_question():
    vector_store = FakeVectorStore(scored_documents())
    chain = FakeChain("Pause deployments, notify the incident channel, and prepare rollback.")

    response = answer_question(
        "  What should I do if checkout API errors spike?  ",
        vector_store=vector_store,
        chain=chain,
        top_k=2,
    )

    assert vector_store.calls == [
        {"query": "What should I do if checkout API errors spike?", "k": 2}
    ]
    assert len(chain.payloads) == 1

    payload = chain.payloads[0]
    assert payload["question"] == "What should I do if checkout API errors spike?"
    assert "Checkout API Error Spike Runbook" in payload["context"]
    assert "Rollback Coordination Runbook" in payload["context"]

    assert response["answer"].startswith("Pause deployments")
    assert response["sources"][0]["source_id"] == "REL-101"
    assert response["langchain"]["fallback"] is False
    assert response["langchain"]["retrieved_count"] == 2
    assert response["langchain"]["retrieved_chunk_ids"] == [
        "chunk-rel-101-b",
        "chunk-rel-102-a",
    ]


def test_answer_question_returns_fallback_without_calling_chain():
    vector_store = FakeVectorStore([])
    chain = FakeChain("This should not be called.")

    response = answer_question(
        "What is the office lunch policy?",
        vector_store=vector_store,
        chain=chain,
        top_k=3,
    )

    assert chain.payloads == []
    assert response["sources"] == []
    assert response["langchain"]["fallback"] is True
    assert "not have enough approved runbook context" in response["answer"]


def test_answer_question_rejects_empty_model_output():
    vector_store = FakeVectorStore(scored_documents())
    chain = FakeChain("   ")

    with pytest.raises(LangChainServiceError) as exc_info:
        answer_question(
            "What should we do after a release spike?",
            vector_store=vector_store,
            chain=chain,
        )

    assert "empty answer" in str(exc_info.value).lower()


def test_answer_question_wraps_unexpected_errors():
    with pytest.raises(LangChainServiceError) as exc_info:
        answer_question(
            "What should we do after a release spike?",
            vector_store=BrokenVectorStore(),
            chain=FakeChain(),
        )

    assert "vector store unavailable" in str(exc_info.value)
