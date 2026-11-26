"""Core summarization logic for the AI Text Summarizer (Skill Nexis, Week 1).

The Hugging Face model is loaded lazily, so importing this module (and running
the input-validation tests) does not require downloading anything.
"""
import re

MODEL_NAME = "sshleifer/distilbart-cnn-12-6"
LENGTH_PRESETS = {"short": 30, "medium": 60, "long": 100}  # target words
MAX_INPUT_WORDS = 20000   # reject anything larger
MIN_INPUT_WORDS = 30      # below this, summarizing is pointless
CHUNK_TOKENS = 700        # safe chunk size for a 1024-token model
TOKENS_PER_WORD = 1.6

_tokenizer = None
_model = None
_device = None


def _get_tokenizer():
    global _tokenizer
    if _tokenizer is None:
        from transformers import AutoTokenizer
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    return _tokenizer


def _get_model():
    global _model, _device
    if _model is None:
        import torch
        from transformers import AutoModelForSeq2SeqLM
        _device = "cuda" if torch.cuda.is_available() else "cpu"
        _model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(_device).eval()
    return _model


def word_count(text):
    return len(text.split())


def split_chunks(text, max_tokens=CHUNK_TOKENS):
    """Split text into sentence-aligned chunks of at most ~max_tokens tokens."""
    tok = _get_tokenizer()
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks, current, current_len = [], [], 0
    for s in sentences:
        n = len(tok.encode(s, add_special_tokens=False))
        if current and current_len + n > max_tokens:
            chunks.append(" ".join(current))
            current, current_len = [], 0
        current.append(s)
        current_len += n
    if current:
        chunks.append(" ".join(current))
    return chunks


def clean_summary(summary):
    """Fix spacing before punctuation and drop a trailing incomplete sentence."""
    s = re.sub(r"\s+([.,;:!?])", r"\1", summary.strip())
    if s and s[-1] not in ".!?":
        ends = list(re.finditer(r"[.!?](?=\s|$)", s))
        if ends:                      # keep at least one complete sentence
            s = s[:ends[-1].end()]
    return s


def _run_model(text, target_words):
    tok = _get_tokenizer()
    max_len = int(target_words * TOKENS_PER_WORD)
    min_len = max(10, int(max_len * 0.5))
    in_len = len(tok.encode(text, add_special_tokens=False))
    max_len = min(max_len, max(12, in_len - 1))   # never longer than the input
    min_len = min(min_len, max_len - 1)
    import torch
    model = _get_model()
    inputs = tok(text, return_tensors="pt", truncation=True, max_length=1024).to(_device)
    with torch.no_grad():
        ids = model.generate(**inputs, max_length=max_len, min_length=min_len,
                             num_beams=4, do_sample=False,
                             no_repeat_ngram_size=3, early_stopping=True)
    return clean_summary(tok.decode(ids[0], skip_special_tokens=True))


def resolve_length(length):
    """Turn 'short'/'medium'/'long' or an int into a target word count."""
    if isinstance(length, str):
        if length not in LENGTH_PRESETS:
            raise ValueError(f"length must be one of {list(LENGTH_PRESETS)} or an integer.")
        return LENGTH_PRESETS[length]
    return max(15, int(length))


def summarize(text, length="medium"):
    """Summarize `text`.

    length: 'short' | 'medium' | 'long' or an int (target number of words).
    Raises ValueError for empty input, over-long input, or a bad length value.
    Input shorter than MIN_INPUT_WORDS is returned unchanged.
    """
    if text is None or not text.strip():
        raise ValueError("Input is empty. Please provide some text to summarize.")
    words = word_count(text)
    if words > MAX_INPUT_WORDS:
        raise ValueError(f"Input too long ({words} words). Limit is {MAX_INPUT_WORDS}.")
    target = resolve_length(length)
    if words < MIN_INPUT_WORDS:
        return text.strip()

    chunks = split_chunks(text)
    if len(chunks) == 1:
        return _run_model(chunks[0], target)
    # map-reduce: summarize each chunk, then summarize the combined summaries
    partials = [_run_model(c, max(40, target)) for c in chunks]
    return _run_model(" ".join(partials), target)


# ---------- factual-accuracy helpers ----------
def _extract_facts(text):
    nums = {n.rstrip(".,") for n in re.findall(r"\d[\d,\.]*", text)}
    caps = set(re.findall(r"(?<![.!?]\s)(?<!^)\b[A-Z][a-z]+", text))
    return nums, caps


def auto_check(source, summary):
    """Return numbers/names in the summary that do not appear in the source.

    An empty list means every number and capitalized name is supported. This
    catches invented facts, not misleading use of real ones, so it supplements
    (never replaces) manual review.
    """
    nums, caps = _extract_facts(summary)
    src = source.replace(",", "")
    unsupported = [n for n in nums if n.replace(",", "") not in src]
    unsupported += [c for c in caps if c not in source]
    return sorted(unsupported)
