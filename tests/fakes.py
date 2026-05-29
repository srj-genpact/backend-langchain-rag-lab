"""Fakes used by the automated tests."""


class FakeDocument:
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata or {}


class FakeVectorStore:
    def __init__(self, scored_documents):
        self.scored_documents = scored_documents
        self.calls = []

    def similarity_search_with_score(self, query, k=3):
        self.calls.append({"query": query, "k": k})
        return self.scored_documents[:k]


class BrokenVectorStore:
    def similarity_search_with_score(self, query, k=3):
        raise RuntimeError("vector store unavailable")


class FakeChain:
    def __init__(self, answer="Use the approved runbook steps."):
        self.answer = answer
        self.payloads = []

    def invoke(self, payload):
        self.payloads.append(payload)
        return self.answer
