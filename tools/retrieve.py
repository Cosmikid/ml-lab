"""Retrieve relevant wiki chunks for Z3PO context.

Usage:
  python tools/retrieve.py "your question here"
  python tools/retrieve.py "what is attention" --top 5

The web UI can call this and inject the results as context for Z3PO.
"""
import sys
import os
import argparse
import chromadb

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "checkpoints", "vector_db")


def retrieve(query: str, top_k: int = 5) -> list[dict]:
    """Return top_k most relevant chunks for the query."""
    if not os.path.exists(DB_DIR):
        return []

    chroma = chromadb.PersistentClient(path=DB_DIR)
    collection = chroma.get_or_create_collection("wiki")

    if collection.count() == 0:
        return []

    from ollama import Client
    client = Client(host="http://localhost:11434")
    resp = client.embeddings(model="nomic-embed-text", prompt=query)

    results = collection.query(
        query_embeddings=[resp["embedding"]],
        n_results=min(top_k, collection.count()),
    )

    return [
        {
            "text": doc,
            "source": meta.get("source", "unknown"),
            "score": 1.0 - dist,
        }
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ]


def format_context(results: list[dict]) -> str:
    """Format results as a context block for Z3PO."""
    if not results:
        return "(no relevant context found)"
    blocks = []
    for i, r in enumerate(results, 1):
        blocks.append(f"[{i}] (source: {r['source']}, relevance: {r['score']:.3f})\n{r['text']}")
    return "\n\n---\n\n".join(blocks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve wiki context for Z3PO")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--top", type=int, default=5, help="Number of results")
    args = parser.parse_args()

    results = retrieve(args.query, args.top)
    print(format_context(results))
