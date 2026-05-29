import pytest

import app as app_module
from app import create_app
from lib.langchain_rag_service import LangChainServiceError


@pytest.fixture
def client():
    flask_app = create_app()
    flask_app.config.update(TESTING=True)
    return flask_app.test_client()


def test_invalid_payload_returns_400(client):
    response = client.post("/api/ask", json={})

    assert response.status_code == 400
    body = response.get_json()
    assert body["error"] == "missing_question"
    assert "question" in body["message"].lower()


def test_successful_request_returns_service_response(client, monkeypatch):
    def fake_answer_question(question):
        assert question == "When should we publish a status page update?"
        return {
            "answer": "Publish an update for customer-facing impact.",
            "sources": [
                {
                    "source_id": "REL-120",
                    "title": "Status Page Update Guide",
                    "category": "Reliability",
                    "section": "Customer Communication",
                    "chunk_id": "chunk-rel-120-a",
                    "distance": 0.2,
                }
            ],
            "langchain": {"fallback": False},
        }

    monkeypatch.setattr(app_module, "answer_question", fake_answer_question)

    response = client.post(
        "/api/ask",
        json={"question": "When should we publish a status page update?"},
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["answer"].startswith("Publish")
    assert body["sources"][0]["source_id"] == "REL-120"
    assert body["langchain"]["fallback"] is False


def test_service_error_returns_502(client, monkeypatch):
    def fake_answer_question(question):
        raise LangChainServiceError("model unavailable")

    monkeypatch.setattr(app_module, "answer_question", fake_answer_question)

    response = client.post(
        "/api/ask",
        json={"question": "What should we do after a release spike?"},
    )

    assert response.status_code == 502
    body = response.get_json()
    assert body["error"] == "langchain_service_error"
    assert "model unavailable" in body["message"]
