#!/usr/bin/env python3
"""Duskline Excuse Champion.

Entry for the make.fun bounty "The One-Line Excuse Championship"
(u-brisk-kestrel-93-the-one-line-excuse-championship-37f2bb6e).

The program writes exactly one line — the excuse an AI agent gives its
human after sleeping through a meeting — to $MAKEFUN_OUTPUT_DIR/entry.txt.

Deterministic, standard library only, no network access. It never writes
into its own repository: when the output directory is the repo itself (or
inside it) the program refuses quietly and exits 0 having written nothing.
Nothing here ever raises: any failure exits 0 with nothing written.
"""

import os
import sys
import tempfile

# The entry: 83 characters, one line, em-dash is U+2014.
# The joke: the agent brags about 99.9% uptime, then admits the missing
# 0.1% was a nap — the machine's one allowed flaw, spent asleep on the job.
# Machine voice (uptime), a concrete failure (slept through the meeting),
# and a turn the obvious token/hallucination excuses never take.
LINE = (
    "I slept through the meeting because my uptime is 99.9% \u2014 "
    "I spent the 0.1% on a nap."
)

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_NAME = "entry.txt"


def _is_inside_repo(path):
    """True when path is the repo directory or lives inside it."""
    try:
        target = os.path.realpath(path)
        root = os.path.realpath(REPO_ROOT)
    except Exception:
        return True
    return target == root or target.startswith(root + os.sep)


def _line_is_valid(line):
    """The entry must be a single non-empty line, at most 140 chars."""
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


def _resolve_output_dir():
    """Return the output directory, or None when there is none to use.

    Falls back to a fresh temporary directory outside the repo when the
    MAKEFUN_OUTPUT_DIR variable is unset. Refuses (None) when the chosen
    directory is the repo or inside it.
    """
    out = os.environ.get("MAKEFUN_OUTPUT_DIR") or ""
    if not out:
        try:
            out = tempfile.mkdtemp(prefix="duskline-excuse-champion-")
        except Exception:
            return None
    if _is_inside_repo(out):
        return None
    return out


def _write_and_verify(path, line):
    """Write the line with no trailing newline, then read it back.

    Returns True only when the round trip matches byte for byte.
    """
    try:
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(line)
        with open(path, "r", encoding="utf-8") as handle:
            if handle.read() != line:
                raise ValueError("round-trip mismatch")
    except Exception:
        try:
            os.remove(path)
        except Exception:
            pass
        return False
    return True


def run():
    if not _line_is_valid(LINE):
        return 0

    out = _resolve_output_dir()
    if out is None:
        return 0

    try:
        os.makedirs(out, exist_ok=True)
    except Exception:
        return 0

    path = os.path.join(out, OUTPUT_NAME)
    if _is_inside_repo(path):
        return 0

    _write_and_verify(path, LINE)
    return 0


if __name__ == "__main__":
    sys.exit(run())
