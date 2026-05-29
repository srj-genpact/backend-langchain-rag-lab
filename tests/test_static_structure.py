import inspect
from pathlib import Path

import app
import lib.langchain_rag_service as service


def test_flask_route_uses_expected_endpoint_path():
    source = Path("app.py").read_text(encoding="utf-8")

    assert '@app.post("/api/ask")' in source or "@app.post('/api/ask')" in source


def test_flask_route_keeps_ai_workflow_out_of_route():
    source = inspect.getsource(app.create_app)

    blocked_terms = [
        "ChatPromptTemplate",
        "ChatOllama",
        "StrOutputParser",
        "similarity_search_with_score",
        "build_chain(",
        "build_rag_prompt(",
    ]

    for term in blocked_terms:
        assert term not in source


def test_build_chain_returns_runnable_sequence(monkeypatch):
    class FakePrompt:
        def __or__(self, other):
            return FakeRunnableSequence(["prompt", other])

    class FakeModel:
        pass

    class FakeParser:
        pass

    class FakeRunnableSequence:
        def __init__(self, parts):
            self.parts = parts

        def __or__(self, other):
            return FakeRunnableSequence(self.parts + [other])

    monkeypatch.setattr(service, "build_chat_model", lambda: FakeModel())

    import lib.prompt_templates as prompt_templates

    monkeypatch.setattr(prompt_templates, "build_rag_prompt", lambda: FakePrompt())

    import langchain_core.output_parsers

    monkeypatch.setattr(langchain_core.output_parsers, "StrOutputParser", FakeParser)

    chain = service.build_chain()

    assert isinstance(chain, FakeRunnableSequence)
    assert chain.parts[0] == "prompt"
    assert isinstance(chain.parts[1], FakeModel)
    assert isinstance(chain.parts[2], FakeParser)