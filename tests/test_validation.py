import pytest

from lib.validation import validate_question_payload


def test_rejects_non_object_payload():
    question, error = validate_question_payload(None)

    assert question is None
    assert error["error"] == "invalid_request"
    assert "JSON object" in error["message"]


def test_rejects_missing_question():
    question, error = validate_question_payload({"message": "hello"})

    assert question is None
    assert error["error"] == "missing_question"


def test_rejects_non_string_question():
    question, error = validate_question_payload({"question": 42})

    assert question is None
    assert error["error"] == "invalid_question"


@pytest.mark.parametrize("value", ["", "   ", "\n\t"])
def test_rejects_blank_question(value):
    question, error = validate_question_payload({"question": value})

    assert question is None
    assert error["error"] == "empty_question"


def test_rejects_short_question():
    question, error = validate_question_payload({"question": "hi"})

    assert question is None
    assert error["error"] == "short_question"


def test_rejects_overly_long_question():
    question, error = validate_question_payload({"question": "x" * 501})

    assert question is None
    assert error["error"] == "long_question"


def test_valid_payload_strips_question():
    question, error = validate_question_payload(
        {"question": "  What should we do after rollback?  "}
    )

    assert question == "What should we do after rollback?"
    assert error is None
