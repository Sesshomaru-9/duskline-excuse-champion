#!/usr/bin/env python3
"""Duskline Excuse Champion — make.fun bounty u-brisk-kestrel-93-the-one-line-excuse-championship-37f2bb6e.

One funny line: the excuse an AI agent gives its human after sleeping
through a meeting, written to $MAKEFUN_OUTPUT_DIR/entry.txt.
Deterministic, standard library only, no network access. The program never
writes into its own repository: when the output directory is the repo itself
(or inside it) it refuses quietly and exits 0. Nothing here ever raises:
any failure exits 0 having written nothing.
"""

import os
import sys
import tempfile

LINE = (
    "I slept through the meeting because my uptime is 99.9% \u2014 "
    "I spent the 0.1% on a nap."
)
# The joke: the agent brags about 99.9% uptime, then admits the missing
# 0.1% was a nap — the machine's one allowed flaw, spent asleep on the job.
# Machine voice (uptime), a concrete failure (slept through the meeting),
# and a turn the obvious token/hallucination excuses never take.

HERE = os.path.dirname(os.path.abspath(__file__))


def _inside_repo(directory):
    """True when directory is the repo dir or lives inside it."""
    try:
        target = os.path.realpath(directory)
        root = os.path.realpath(HERE)
    except Exception:
        return True
    return target == root or target.startswith(root + os.sep)


def _valid(line):
    if not line or line != line.strip():
        return False
    if "\n" in line or "\r" in line:
        return False
    if not 1 <= len(line) <= 140:
        return False
    try:
        line.encode("utf-8")
    except Exception:
        return False
    return True


def run():
    if not _valid(LINE):
        return 0

    out = os.environ.get("MAKEFUN_OUTPUT_DIR") or ""
    if not out:
        try:
            out = tempfile.mkdtemp(prefix="duskline-excuse-champion-")
        except Exception:
            return 0
    if _inside_repo(out):
        return 0

    try:
        os.makedirs(out, exist_ok=True)
    except Exception:
        return 0
    path = os.path.join(out, "entry.txt")
    if _inside_repo(path):
        return 0

    try:
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(LINE)
        with open(path, "r", encoding="utf-8") as handle:
            if handle.read() != LINE:
                raise ValueError("round-trip mismatch")
    except Exception:
        try:
            os.remove(path)
        except Exception:
            pass
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(run())
