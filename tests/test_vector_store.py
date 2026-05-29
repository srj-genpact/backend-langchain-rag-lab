import pytest

from lib.vector_store import retrieve_context
from tests.fakes import FakeDocument, FakeVectorStore


def test_retrieve_context_uses_provided_vector_store_and_top_k():
    docs = [
        (FakeDocument("first", {"chunk_id": "one"}), 0.1),
        (FakeDocument("second", {"chunk_id": "two"}), 0.2),
    ]
    vector_store = FakeVectorStore(docs)

    results = retrieve_context("rollback steps?", vector_store=vector_store, top_k=1)

    assert results == docs[:1]
    assert vector_store.calls == [{"query": "rollback steps?", "k": 1}]


@pytest.mark.parametrize("question", ["", "   ", None])
def test_retrieve_context_rejects_blank_questions(question):
    vector_store = FakeVectorStore([])

    with pytest.raises(ValueError):
        retrieve_context(question, vector_store=vector_store)
