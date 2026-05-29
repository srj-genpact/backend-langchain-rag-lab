"""Seed the local Chroma collection with reliability runbook chunks."""

from lib.documents import chunks_to_documents, load_runbook_chunks
from lib.vector_store import build_vector_store


def main():
    """Load runbook chunks and add them to Chroma."""

    chunks = load_runbook_chunks()
    documents = chunks_to_documents(chunks)
    vector_store = build_vector_store()
    vector_store.add_documents(documents)
    print(f"Seeded {len(documents)} runbook chunks into Chroma.")


if __name__ == "__main__":
    main()
