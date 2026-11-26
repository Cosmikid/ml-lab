"""Z3PO RAG Web UI."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "tools"))

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from generate import generate
from pydantic import BaseModel

app = FastAPI(title="Z3PO RAG")


class Question(BaseModel):
    query: str


@app.post("/ask")
def ask(req: Question):
    answer = generate(req.query)
    return {"answer": answer}


@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Z3PO</title>
    <style>
      body { font-family: sans-serif; max-width: 700px; margin: 40px auto; padding: 0 20px; }
      h1 { font-size: 1.5rem; }
      #chat { border: 1px solid #ddd; border-radius: 8px; padding: 16px; min-height: 200px; margin-bottom: 12px; }
      .msg { margin-bottom: 12px; }
      .user { color: #0066cc; }
      .bot { color: #333; }
      input { width: 70%; padding: 8px; font-size: 1rem; }
      button { padding: 8px 16px; font-size: 1rem; cursor: pointer; }
    </style>
    </head>
    <body>
      <h1>Z3PO</h1>
      <div id="chat"></div>
      <div>
        <input id="q" placeholder="Ask a question..." autofocus>
        <button onclick="ask()">Ask</button>
      </div>
      <script>
        const chat = document.getElementById('chat');
        const input = document.getElementById('q');
        input.addEventListener('keydown', e => { if (e.key === 'Enter') ask(); });
        async function ask() {
          const q = input.value.trim();
          if (!q) return;
          input.value = '';
          chat.innerHTML += `<div class="msg user"><b>You:</b> ${q}</div>`;
          chat.innerHTML += `<div class="msg bot" id="loading"><i>Thinking...</i></div>`;
          chat.scrollTop = chat.scrollHeight;
          try {
            const r = await fetch('/ask', {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({query: q})
            });
            const data = await r.json();
            document.getElementById('loading').innerHTML =
            `<b>Z3PO:</b> ${data.answer.replace(/\\n/g, '<br>')}`;   ;
          } catch (e) {
            document.getElementById('loading').innerHTML = '<i>Error: ' + e.message + '</i>';
          }
          chat.scrollTop = chat.scrollHeight;
        }
      </script>
    </body>
    </html>
    """


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
