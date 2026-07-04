# Planning Notes: LangChain RAG API

Complete each section before submitting. Replace every TODO with your own notes.

## 1. System Goal

- User or role: Internal Platform Engineers and On-call Developers.
- Business problem: Quick guidance during reliability incidents based strictly on approved internal runbooks rather than general model knowledge to prevent hallucinations.
- Approved knowledge source: Reliability runbooks stored in `data/runbook_chunks.json` and indexed in a local Chroma vector database.
- Endpoint route: `POST /api/ask`

## 2. Manual RAG Workflow Map

Name the manual RAG steps this LangChain version is organizing.

- Receive question: Accept incoming client query and validate the payload.
- Retrieve context: Query the vector store for the top K runbook chunks matching the question.
- Build prompt: Format the prompt containing system instructions, retrieved context, and the user's question.
- Call model: Pass the formatted prompt to the local LLM wrapper.
- Parse or format output: Clean and format the model's text output.
- Return sources: Compile the metadata of the retrieved documents (IDs, titles, category, section, distance) and return it with the answer.
- Verify quality: Check context availability, prevent model execution if context is missing, and handle empty answers or service errors.

## 3. LangChain Component Mapping

Map the manual workflow to LangChain-supported pieces.

- Prompt string maps to: `ChatPromptTemplate`
- Chroma search logic maps to: `Chroma` vector store using `OllamaEmbeddings`
- Direct model call maps to: `ChatOllama`
- Function-to-function workflow maps to: LCEL (LangChain Expression Language) runnable sequence via the `|` operator
- Manual output cleanup maps to: `StrOutputParser`
- Manual testing maps to: Command-line execution (`try_langchain_rag.py`) and pytest suite

## 4. Response Contract

List the fields a successful response should include.

- `answer` (formatted string containing response text)
- `sources` (list of metadata dictionaries for retrieved context chunks)
- `langchain` (metadata dictionary for inspectability and debug metrics)

## 5. Fallback Behavior

Explain what the system should do when no approved context is available.

If no usable context (documents with non-blank page content) is retrieved from the vector store, the system must immediately return a safe, pre-configured fallback response ("I do not have enough approved runbook context to answer that reliably.") and bypass the LLM chain invocation entirely to prevent hallucinations.

## 6. Verification Plan

List at least four checks you should run before trusting the refactor.

- Run the full automated unit test suite using `pytest` to verify all 31 test assertions pass.
- Execute `python seed_chroma.py` to ensure the vector store initializes and indexes documents correctly.
- Run `python try_langchain_rag.py` to manually check command-line RAG generation.
- Start the Flask app, make valid/invalid request queries via curl, and inspect the JSON response structures and HTTP status codes (200, 400, 502).

## 7. Reflection

Explain what LangChain simplified and what may be harder to inspect.

LangChain simplifies chaining steps like prompt formatting, model invocation, and parsing into a unified, readable pipeline using LCEL. This makes the code modular and easy to extend. However, this high-level abstraction can make it harder to inspect the final rendered prompt, debug internal communication errors, or trace intermediate states without installing extra observability tools like LangSmith.
