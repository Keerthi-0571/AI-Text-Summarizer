# Model and Prompts

**Model.** `sshleifer/distilbart-cnn-12-6` is a distilled version of BART, a
sequence-to-sequence transformer. An encoder reads the passage and a decoder
writes a new summary one token at a time. It was fine-tuned on CNN/DailyMail
news articles.

**Prompts.** This is a task-specific summarizer, not a chat model, so it takes
no natural-language instruction. The "prompt" is the input text plus decoding
settings:
- `min_length` / `max_length`: derived from the requested summary length
  (about 1.6 tokens per word).
- `num_beams=4`, `do_sample=False`: deterministic beam-search output, which suits factual tasks.

**Post-processing.** Summaries are cleaned: spacing before punctuation is fixed and a trailing incomplete sentence (caused by the length cap) is removed.

**Long input.** The model reads about 1,024 tokens at once. Longer text is split
into sentence-aligned chunks of about 700 tokens, each chunk is summarized, and
the partial summaries are summarized again (map-reduce).

**Limitations.**
- Trained on news; quality may drop on legal, technical or conversational text.
- Abstractive models can paraphrase numbers or merge facts incorrectly.
- The automatic check only finds numbers/names absent from the source. It
  cannot detect a real fact used misleadingly, so manual review is required.

**Possible improvements.** Try `facebook/bart-large-cnn`, or an LLM API with an
explicit instruction such as "Summarize in 2 sentences. Use only facts in the
text."
