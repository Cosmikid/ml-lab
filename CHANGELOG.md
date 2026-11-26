# Changelog

## 2026-11-26

### Performance
- Switched ChromaDB distance metric from L2 to cosine
- Added chunk overlap (100 chars) to prevent context loss at boundaries
- Set num_ctx: 4096 and temperature: 0.1 in generate.py
- Enabled Ollama flash attention + q8_0 KV cache

### Results
- Relevance scores improved significantly with cosine distance:
  - L2: chunk [2] scored 0.003 (near-zero, useless)
  - Cosine: chunk [2] scored 0.713 (meaningful ranking)
- Cosine distances range 0-2, making 1/(1+dist) produce more discriminative scores than L2

### RAG Pipeline
- tools/embed.py — ingest wiki files into ChromaDB
- tools/retrieve.py — query vector store, return ranked chunks
- tools/generate.py — feed context to qwen2.5:1.5b for grounded answers   