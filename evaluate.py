"""Run the summarizer on the five examples and write evaluation files.

Outputs:
    results/summaries.json     - input, summary and automatic check per example
    results/evaluation.md      - table to complete with your manual verdicts
"""
import json
from pathlib import Path

from summarizer import summarize, auto_check
from summarizer.core import word_count

ROOT = Path(__file__).parent
examples = json.loads((ROOT / "data" / "examples.json").read_text(encoding="utf-8"))

results = []
for e in examples:
    summary = summarize(e["text"], length="short")
    unsupported = auto_check(e["text"], summary)
    results.append({
        "id": e["id"], "topic": e["topic"],
        "source_words": word_count(e["text"]),
        "summary": summary, "summary_words": word_count(summary),
        "unsupported_facts": unsupported,
        "auto_flag": "CHECK" if unsupported else "OK",
    })
    print(f"[{e['id']}] {e['topic']}: {summary}\n    auto check: {results[-1]['auto_flag']} {unsupported}\n")

out = ROOT / "results"
out.mkdir(exist_ok=True)
(out / "summaries.json").write_text(json.dumps(results, indent=2), encoding="utf-8")

lines = ["# Evaluation results", "",
         "Complete the last three columns after reading each summary against its source.",
         "Verdict: Accurate / Minor issue / Inaccurate.", "",
         "| # | Topic | Words (src > summary) | Auto check | Verdict | Key facts kept | Errors / notes |",
         "|---|-------|-----------------------|------------|---------|----------------|----------------|"]
for r in results:
    flag = r["auto_flag"] + ("" if not r["unsupported_facts"] else f" ({', '.join(r['unsupported_facts'])})")
    lines.append(f"| {r['id']} | {r['topic']} | {r['source_words']} > {r['summary_words']} | {flag} | TODO | TODO | TODO |")
(out / "evaluation.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("Wrote results/summaries.json and results/evaluation.md")
