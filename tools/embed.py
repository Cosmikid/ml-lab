"""Ingest wiki/text files into a vector store for Z3PO retrieval."""

import os
import sys

import chromadb
from ollama import Client

OLLAMA_URL = "http://localhost:11434"
DB_DIR = os.path.join(os.path.dirname(__file__), "..", "checkpoints", "vector_db")


def get_client():
    return Client(host=OLLAMA_URL)


def chunk_text(text: str, max_chars: int = 800) -> list[str]:
    """Split text into chunks by paragraph, respecting max length."""
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) > max_chars and current:
            chunks.append(current.strip())
            current = para
        else:
            current = current + "\n\n" + para if current else para
    if current.strip():
        chunks.append(current.strip())
    return chunks


def embed_file(filepath: str, collection):
    """Read a file, chunk it, embed, and store."""
    with open(filepath, "r") as f:
        text = f.read()

    chunks = chunk_text(text)
    if not chunks:
        print("  (empty, skipping)")
        return 0

    # Embed via Ollama
    client = get_client()
    embeddings = []
    for chunk in chunks:
        resp = client.embeddings(model="nomic-embed-text", prompt=chunk)
        embeddings.append(resp["embedding"])

    # Store in ChromaDB
    ids = [f"{os.path.basename(filepath)}_{i}" for i in range(len(chunks))]
    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=[{"source": os.path.basename(filepath)} for _ in chunks],
    )
    return len(chunks)


def ingest(directory: str | None = None):
    """Ingest all .md, .txt, .rst files from a directory."""
    if directory is None:
        directory = os.path.join(os.path.dirname(__file__), "..", "data")

    if not os.path.exists(directory):
        print(f"No data dir at {directory}. Create it and add wiki files.")
        return

    os.makedirs(DB_DIR, exist_ok=True)
    chroma = chromadb.PersistentClient(path=DB_DIR)
    collection = chroma.get_or_create_collection("wiki")

    files = []
    for ext in (".md", ".txt", ".rst", ".html"):
        files.extend(f for f in os.listdir(directory) if f.endswith(ext))

    if not files:
        print(f"No wiki files found in {directory}")
        return

    total = 0
    for fname in sorted(files):
        path = os.path.join(directory, fname)
        print(f"  {fname}...", end=" ")
        n = embed_file(path, collection)
        print(f"{n} chunks")
        total += n

    print(f"\nDone. {total} chunks in collection '{collection.name}'.")


if __name__ == "__main__":
    ingest(sys.argv[1] if len(sys.argv) > 1 else None)
