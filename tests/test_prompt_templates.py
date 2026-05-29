from lib.prompt_templates import build_rag_prompt


def test_prompt_template_exposes_context_and_question_variables():
    prompt = build_rag_prompt()

    input_variables = set(getattr(prompt, "input_variables", []))

    assert {"context", "question"}.issubset(input_variables)


def test_prompt_template_formats_context_and_question():
    prompt = build_rag_prompt()

    messages = prompt.format_messages(
        context="Rollback guidance from REL-102.",
        question="When should we rollback?",
    )
    rendered = "\n".join(getattr(message, "content", str(message)) for message in messages)

    assert "Rollback guidance from REL-102." in rendered
    assert "When should we rollback?" in rendered
    assert "approved" in rendered.lower()
    assert "context" in rendered.lower()
