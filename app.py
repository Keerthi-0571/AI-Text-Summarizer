"""Command-line interface for the AI Text Summarizer.

Examples:
    python app.py --file article.txt --length short
    python app.py --text "Long text here..." --length 50
    echo "Long text..." | python app.py --length long
"""
import argparse
import sys

from summarizer import summarize


def parse_length(value):
    return int(value) if value.isdigit() else value


def main():
    p = argparse.ArgumentParser(description="Summarize text with a pretrained model.")
    src = p.add_mutually_exclusive_group()
    src.add_argument("--text", help="text to summarize")
    src.add_argument("--file", help="path to a .txt file to summarize")
    p.add_argument("--length", default="medium", type=parse_length,
                   help="short | medium | long | number of words (default: medium)")
    args = p.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    elif args.text is not None:
        text = args.text
    else:
        text = sys.stdin.read()

    try:
        print(summarize(text, args.length))
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
