"""Request validation helpers for POST /api/ask."""

from lib.config import MAX_QUESTION_LENGTH, MIN_QUESTION_LENGTH


def validate_question_payload(payload):
    """Validate the JSON body for POST /api/ask.

    Return:
        (question, None) when valid
        (None, error_dict) when invalid
    """

    # TODO: Reject non-dictionary payloads.
    # TODO: Require a "question" field.
    # TODO: Require the question to be a string.
    # TODO: Strip whitespace.
    # TODO: Reject blank questions.
    # TODO: Reject questions shorter than MIN_QUESTION_LENGTH.
    # TODO: Reject questions longer than MAX_QUESTION_LENGTH.
    # TODO: Return (question, None) when valid.
    raise NotImplementedError("Complete request validation.")
