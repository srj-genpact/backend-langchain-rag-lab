"""Run the LangChain RAG service from the command line."""

import json
import sys

from lib.langchain_rag_service import answer_question


def main():
    """Ask one question from the command line."""

    question = " ".join(sys.argv[1:]).strip()
    if not question:
        question = "What should I do if checkout API errors spike right after a release?"

    response = answer_question(question)
    print(json.dumps(response, indent=2))


if __name__ == "__main__":
    main()
