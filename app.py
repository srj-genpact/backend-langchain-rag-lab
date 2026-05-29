"""Flask API for the LangChain RAG lab."""

from flask import Flask, jsonify, request

from lib.langchain_rag_service import LangChainServiceError, answer_question
from lib.response_formatter import format_error_response
from lib.validation import validate_question_payload


def create_app():
    """Create and configure the Flask application."""

    app = Flask(__name__)

    @app.post("/api/ask")
    def ask():
        """Accept a question and return a source-backed LangChain RAG response."""

        # TODO: Get the JSON body with request.get_json(silent=True).
        # TODO: Validate the question with validate_question_payload().
        # TODO: Return validation errors as JSON with HTTP 400.
        # TODO: Call answer_question(question) for valid requests.
        # TODO: Return successful responses as JSON with HTTP 200.
        # TODO: Convert LangChainServiceError into a structured HTTP 502 response.
        raise NotImplementedError("Complete the POST /api/ask route.")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
