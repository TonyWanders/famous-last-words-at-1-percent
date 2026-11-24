#!/usr/bin/env python3
"""Write one funny farewell line from a dying phone to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The line is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: 1 to 199 characters, not only white space.
"""

import os
import sys
from pathlib import Path

ENTRY = "Relax, I am not dying. I am just going to sleep for a very long time, in a drawer, next to his old phones, who all warned me about him."

MIN_CHARS = 1
MAX_CHARS = 199
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 199 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"entry is {chars} characters, outside 1-199")
    if not text.strip():
        raise ValueError("entry is only white space")
    if "\n" in text:
        raise ValueError("entry must be a single line")
    return chars


def write_entry(path: Path) -> None:
    """Write ENTRY to path and verify the written bytes match."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(ENTRY, encoding="utf-8")
    if path.read_text(encoding="utf-8") != ENTRY:
        raise ValueError("written entry does not match")


def main() -> int:
    try:
        chars = validate(ENTRY)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    try:
        write_entry(path)
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
