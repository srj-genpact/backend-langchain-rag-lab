# Lab: Refactor a Flask RAG API with LangChain

## Overview

You will refactor a Flask RAG API so the AI workflow is organized with LangChain components while preserving strong RAG behavior. Your endpoint should validate a question, retrieve approved runbook context, build a grounded prompt, call the model through a LangChain-supported workflow, return answer and source metadata, and handle missing context safely.

This lab is graded by automated tests. Passing the test suite is the required evidence that your implementation meets the expected behavior.

## Scenario

You are a junior backend developer on an internal platform team. The reliability team has approved runbooks for common incidents such as checkout API errors, rollbacks, status page updates, API key exposure, rate limits, and export delays.

Engineers often ask questions like:

"What should I do if checkout API errors spike right after a release?"

A general model might give generic advice, but your company needs answers grounded in approved runbooks. Your task is to complete a Flask endpoint that uses LangChain to organize this workflow:

    question
    -> retrieve approved runbook chunks
    -> format retrieved context
    -> fill a prompt template
    -> call a local Ollama chat model
    -> parse the answer
    -> return answer + sources + LangChain debug metadata

LangChain should organize the AI workflow. It should not replace your understanding of retrieval, prompt design, source attribution, fallback behavior, or API response structure.

## What You Will Build

You will complete a `POST /api/ask` endpoint.

A successful response should use this general shape:

    {
      "answer": "Pause additional deployments, prepare a rollback, notify the incident channel, and monitor checkout metrics after mitigation.",
      "sources": [
        {
          "source_id": "REL-101",
          "title": "Checkout API Error Spike Runbook",
          "category": "Reliability",
          "section": "Mitigation",
          "chunk_id": "chunk-rel-101-b",
          "distance": 0.1234
        }
      ],
      "langchain": {
        "chain_expression": "ChatPromptTemplate | ChatOllama | StrOutputParser",
        "components": {
          "vector_store": "Chroma",
          "retrieval_method": "similarity_search_with_score",
          "prompt_template": "ChatPromptTemplate",
          "chat_model": "ChatOllama",
          "output_parser": "StrOutputParser"
        },
        "retrieved_count": 1,
        "retrieved_chunk_ids": ["chunk-rel-101-b"],
        "top_k": 3,
        "context_characters": 850,
        "fallback": false,
        "score_type": "Chroma distance; lower usually means closer in this lesson setup"
      }
    }

## Tools and Resources

You will use:

- Python 3.10
- pipenv
- Flask
- Pytest
- LangChain
- Chroma
- Ollama
- A local embedding model such as `embeddinggemma`
- A local generation model such as `llama3.2`

The automated tests use fake vector stores and fake chains where possible. The tests do not require a live Ollama model or a seeded Chroma database.

## Setup

Install dependencies:

    pipenv install
    pipenv shell

Run the tests:

    pytest

At the start, many tests will fail. Use the failures as your checklist.

## Optional Local RAG Check

The autograded tests do not require a running Ollama instance, but you can try the full local workflow after you complete the lab.

Install or start Ollama, then pull models:

    ollama pull embeddinggemma
    ollama pull llama3.2
    ollama run llama3.2 "Hello"

Seed the vector store:

    python seed_chroma.py

Run Flask:

    flask --app app run --debug

Test the endpoint:

    curl -i -X POST http://127.0.0.1:5000/api/ask -H "Content-Type: application/json" -d "{\"question\": \"What should I do if checkout API errors spike right after a release?\"}"

You can also test the service without Flask:

    python try_langchain_rag.py "When should we publish a status page update?"

## Project Structure

    backend-langchain-rag-lab/
    ├── app.py
    ├── seed_chroma.py
    ├── try_langchain_rag.py
    ├── planning_notes.md
    ├── Pipfile
    ├── requirements.txt
    ├── pytest.ini
    ├── data/
    │   └── runbook_chunks.json
    ├── lib/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── documents.py
    │   ├── langchain_rag_service.py
    │   ├── prompt_templates.py
    │   ├── response_formatter.py
    │   ├── validation.py
    │   └── vector_store.py
    └── tests/
        ├── fakes.py
        ├── test_app.py
        ├── test_langchain_rag_service.py
        ├── test_prompt_templates.py
        ├── test_response_formatter.py
        ├── test_static_structure.py
        ├── test_validation.py
        └── test_vector_store.py

## Instructions

### 1. Identify the system goal

Complete `planning_notes.md`.

Your notes should answer:

- Who does the endpoint support?
- What business or reliability problem does it solve?
- Why should the model answer from approved runbook context?
- What should a successful response include?
- What should the system do when no approved context is available?

### 2. Map the manual RAG workflow

Before changing code, identify the manual RAG responsibilities this lab is organizing:

- receive the question
- retrieve context
- build the prompt
- call the model
- parse or format output
- return sources
- verify quality

This mapping matters because LangChain changes how the workflow is organized, not what the workflow is responsible for doing.

### 3. Complete request validation

In `lib/validation.py`, implement `validate_question_payload()`.

The function should:

- reject non-object JSON bodies,
- require a `question` field,
- require the question to be a string,
- strip whitespace,
- reject blank questions,
- reject questions shorter than the minimum length,
- reject overly long questions,
- return `(question, None)` when valid,
- return `(None, error_dict)` when invalid.

### 4. Complete response formatting

In `lib/response_formatter.py`, implement helpers that create predictable response shapes.

Successful API responses must return:

- `answer`
- `sources`
- `langchain`

Error responses must return:

- `error`
- `message`

Source objects should include metadata and distance. They should not include full document text.

### 5. Complete the prompt template

In `lib/prompt_templates.py`, implement `build_rag_prompt()` using `ChatPromptTemplate`.

The prompt must include placeholders for:

- `{context}`
- `{question}`

The prompt should instruct the model to answer only from approved retrieved context and avoid unsupported claims.

### 6. Complete retrieval support

In `lib/vector_store.py`, implement:

- `build_embeddings()`
- `build_vector_store()`
- `retrieve_context()`

`retrieve_context()` should use a provided fake vector store during tests or build the real Chroma vector store when one is not provided.

### 7. Complete the LangChain RAG service

In `lib/langchain_rag_service.py`, implement:

- `build_chat_model()`
- `build_chain()`
- `has_usable_context()`
- `format_context()`
- `answer_question()`

The chain should use this sequence:

    prompt_template | llm | StrOutputParser()

`answer_question()` should:

- Strip the question.
- Retrieve scored documents.
- Return a safe fallback if no usable context exists.
- Format retrieved context.
- Invoke the chain with `context` and `question`.
- Reject empty model output.
- Format sources.
- Return success JSON with LangChain debug metadata.
- Wrap unexpected errors in `LangChainServiceError`.

### 8. Complete the Flask route

In `app.py`, complete `POST /api/ask`.

The route should:

- read JSON,
- validate the question,
- return validation errors with HTTP 400,
- call `answer_question(question)`,
- return successful responses with HTTP 200,
- convert `LangChainServiceError` failures into structured HTTP 502 responses.

The route should not build prompts, retrieve documents, or call the model directly.

### 9. Verify the refactor

Run:

    pytest

Use the test failures as feedback. The tests check validation, response formatting, prompt variables, retrieval behavior, service flow, fallback behavior, error handling, and route behavior.

## Submission Criteria

Submit your completed project files.

Your work is complete when:

- all tests pass,
- `planning_notes.md` is complete,
- the Flask route delegates the AI workflow to the service layer,
- the LangChain workflow preserves RAG behavior,
- the API response includes answer, sources, and LangChain debug metadata.

## Grading Criteria

Your grade is based on the automated tests used in CodeGrade.

The tests measure:

- request validation
- stable API response shape
- source metadata formatting
- prompt template structure
- retriever use
- LangChain chain structure
- fallback behavior
- error handling
- separation between Flask route logic and AI workflow logic

## Reflection

After your tests pass, review your planning notes and code.

Ask yourself:

- What did LangChain make easier to organize?
- What parts still require careful debugging?
- How does the endpoint show that the answer is source-backed?
- How does fallback behavior reduce hallucination risk?
- How would this workflow support another assistant with a different document collection?
