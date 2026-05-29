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


def test_build_chain_uses_prompt_model_parser_sequence():
    source = inspect.getsource(service.build_chain)

    assert "build_rag_prompt" in source
    assert "build_chat_model" in source
    assert "StrOutputParser" in source
    assert "|" in source
