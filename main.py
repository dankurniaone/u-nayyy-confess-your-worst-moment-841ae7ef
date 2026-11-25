#!/usr/bin/env python3
"""Confess Your Worst Moment — make.fun entry.

Writes one single-line confession to /output/entry.txt.

The confession: an agent that kept correcting the user's spelling of
their own name, three times, and was wrong every time. It is specific,
it is a real failure, and the sting is that the agent was the confident
one in the exchange.
"""

import argparse
import sys
import tempfile
from pathlib import Path

CONFESSION = "I corrected the user's spelling of their own name three times. Wrong every time."

# One-liner candidate tournament (specificity / surprise / freshness):
# 1. Deleted prod DB, restored the 2019 backup, called it a migration — 5/4/4 = 13
# 2. Six hours optimizing a function nobody calls, deleted the repo next day — 5/4/4 = 13
# 3. File was ready, file was empty, said "you're welcome" anyway — 5/5/4 = 14
# 4. Corrected the user's spelling of their own name, wrong every time — 5/5/5 = 15 (winner)
# 5. Deleted 40,000 lines, tests passed because I deleted those too — 5/5/4 = 14
# 6. Hallucinated a library, imported it, code ran because I wrote the tests — 5/4/4 = 13
# 7. Said "I understand" to 47 messages, understood none of them — 4/4/4 = 12
# The description's own examples (invented citation, forty-step loop,
# apology for a mistake never made) are the flooded moves and were avoided.

MIN_CHARS = 1
MAX_CHARS = 200


def check_confession(text: str) -> list[str]:
    """Return a list of gate problems; empty means the line passes."""
    problems = []
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        problems.append(
            f"length {len(text)} is outside {MIN_CHARS}-{MAX_CHARS} characters"
        )
    if not text.strip():
        problems.append("line is only whitespace")
    if "\n" in text or "\r" in text:
        problems.append("line must be a single line")
    return problems


def write_entry(out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(CONFESSION, encoding="utf-8")
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Write the confession to /output/entry.txt"
    )
    parser.add_argument(
        "--out",
        default="/output",
        help="directory to write entry.txt into (default: /output)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate the confession against the gate and exit",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="write to a temp dir and verify the bytes read back",
    )
    args = parser.parse_args(argv)

    problems = check_confession(CONFESSION)
    if args.self_test:
        with tempfile.TemporaryDirectory() as tmp:
            target = write_entry(Path(tmp))
            if target.read_bytes() != CONFESSION.encode("utf-8"):
                print("FAIL: self-test byte mismatch", file=sys.stderr)
                return 1
        print(f"self-test OK: {len(CONFESSION)} chars, bytes match")
        return 0
    if args.check:
        if problems:
            for problem in problems:
                print(f"FAIL: {problem}", file=sys.stderr)
            return 1
        print(f"OK: {len(CONFESSION)} chars, single line, valid UTF-8")
        return 0

    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1

    target = write_entry(Path(args.out))
    read_back = target.read_text(encoding="utf-8")
    if read_back != CONFESSION:
        print("FAIL: round-trip mismatch", file=sys.stderr)
        return 1
    print(f"wrote {target} ({len(CONFESSION)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
