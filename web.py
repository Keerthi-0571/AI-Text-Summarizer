"""Web interface for the AI Text Summarizer.

Run:  python web.py     then open  http://127.0.0.1:5000
"""
import json
import threading
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from summarizer import summarize
from summarizer import core

app = Flask(__name__)
ROOT = Path(__file__).parent
_lock = threading.Lock()          # the model handles one request at a time


def _load_examples():
    path = ROOT / "data" / "examples.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


@app.get("/")
def index():
    return render_template("index.html", max_words=core.MAX_INPUT_WORDS)


@app.get("/api/examples")
def examples():
    return jsonify([{"id": e["id"], "topic": e["topic"], "text": e["text"]}
                    for e in _load_examples()])


@app.post("/api/summarize")
def api_summarize():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    length = data.get("length", "medium")
    if isinstance(length, str) and length.isdigit():
        length = int(length)
    if isinstance(length, int) and not 15 <= length <= 300:
        return jsonify(error="Custom length must be between 15 and 300 words."), 400
    try:
        with _lock:
            summary = summarize(text, length)
    except ValueError as e:
        return jsonify(error=str(e)), 400
    except Exception as e:                       # model or download problems
        return jsonify(error=f"Could not summarize: {e}"), 500
    return jsonify(summary=summary,
                   input_words=core.word_count(text),
                   summary_words=core.word_count(summary))


if __name__ == "__main__":
    # Load the model in the background so the first request is faster.
    threading.Thread(target=core._get_model, daemon=True).start()
    app.run(host="127.0.0.1", port=5000, debug=False)
