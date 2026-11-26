"""Generate an answer using retrieved wiki context + Qwen 2.5."""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from ollama import Client
from retrieve import format_context, retrieve

OLLAMA_URL = "http://localhost:11434"
MODEL = "qwen2.5:1.5b"

SYSTEM_PROMPT = """You are Z3PO, a helpful assistant. Answer the user's question
using ONLY the context provided below. If the context doesn't contain the
answer, say so clearly. Be concise.

Context:
{context}"""


def generate(query: str, top_k: int = 5) -> str:
    """Retrieve context and generate an answer via Qwen 2.5."""
    results = retrieve(query, top_k)
    context = format_context(results)

    client = Client(host=OLLAMA_URL)
    response = client.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.format(context=context)},
            {"role": "user", "content": query},
        ],
        options={"num_ctx": 4096, "temperature": 0.1},
    )
    return response["message"]["content"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate answer from wiki context")
    parser.add_argument("query", help="Your question")
    parser.add_argument("--top", type=int, default=5, help="Number of context chunks")
    args = parser.parse_args()

    answer = generate(args.query, args.top)
    print(answer)
