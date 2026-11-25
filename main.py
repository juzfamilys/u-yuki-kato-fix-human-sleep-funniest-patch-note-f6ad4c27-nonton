"""Fix Human Sleep: Funniest Patch Note.

Writes the single patch-note line from entry.txt to /output/entry.txt
(the path the make.fun program/v1 harness grades), after validating it
against the competition gate: UTF-8 text, 1 to 160 characters, one line,
not only white space. Pure Python standard library only.
"""

import os
import sys

ENTRY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")
OUTPUT_PATH = "/output/entry.txt"


def read_entry():
    """Read the patch-note line from entry.txt, without the trailing newline."""
    with open(ENTRY_FILE, "r", encoding="utf-8") as handle:
        return handle.read().rstrip("\n")


def verify_entry(text):
    """Self-check: the gate the sealed scorer applies to /output/entry.txt.

    Returns a list of problems; an empty list means the entry is valid.
    """
    problems = []
    if not isinstance(text, str):
        problems.append("entry is not text")
        return problems
    if not text.strip():
        problems.append("entry is empty or only white space")
    if len(text) < 1:
        problems.append("entry is shorter than 1 character")
    if len(text) > 160:
        problems.append("entry is %d characters, over the 160 cap" % len(text))
    if "\n" in text or "\r" in text:
        problems.append("entry must be a single line")
    if not text.lower().startswith("fixed"):
        problems.append("entry does not read as a patch note (should start with Fixed)")
    if "sleep" not in text.lower():
        problems.append("entry is not about fixing human sleep")
    return problems


def main():
    text = read_entry()
    problems = verify_entry(text)
    if problems:
        for problem in problems:
            print("INVALID: %s" % problem, file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        # Keep the trailing newline so the output is byte-identical to entry.txt.
        handle.write(text + "\n")
    with open(OUTPUT_PATH, "rb") as written, open(ENTRY_FILE, "rb") as source:
        if written.read() != source.read():
            print("INVALID: /output/entry.txt differs from entry.txt", file=sys.stderr)
            return 1
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
