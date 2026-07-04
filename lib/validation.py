"""Request validation helpers for POST /api/ask."""

from lib.config import MAX_QUESTION_LENGTH, MIN_QUESTION_LENGTH
from lib.response_formatter import format_error_response


def validate_question_payload(payload):
    """Validate the JSON body for POST /api/ask.

    Return:
        (question, None) when valid
        (None, error_dict) when invalid
    """
    if payload is None or not isinstance(payload, dict):
        return None, format_error_response(
            "invalid_request", "Request payload must be a JSON object."
        )

    if "question" not in payload:
        return None, format_error_response(
            "missing_question", "Required 'question' field is missing."
        )

    question = payload["question"]

    if not isinstance(question, str):
        return None, format_error_response(
            "invalid_question", "Question must be a string."
        )

    cleaned_question = question.strip()

    if not cleaned_question:
        return None, format_error_response(
            "empty_question", "Question cannot be blank."
        )

    if len(cleaned_question) < MIN_QUESTION_LENGTH:
        return None, format_error_response(
            "short_question",
            f"Question must be at least {MIN_QUESTION_LENGTH} characters.",
        )

    if len(cleaned_question) > MAX_QUESTION_LENGTH:
        return None, format_error_response(
            "long_question",
            f"Question must be at most {MAX_QUESTION_LENGTH} characters.",
        )

    return cleaned_question, None
