#!/usr/bin/env python3
"""Prove the LLM's half is done.

Two markers form the script<->LLM contract:
  <FILL: ...>   due NOW — counted always
  <LATER: ...>  due at a named later stage (build, verify, after runs,
                close) — counted only with --all (the close-time proof)

Usage: python scripts/check_fill.py [--all] <path> [...]
Paths may be files or directories (searched for *.md, skipping scripts/).
Lists every remaining slot as file:line; exit 1 if any counted remain.
"""
import re
import sys
from pathlib import Path

# Key on the opening marker only: slots may span lines, and an unclosed
# slot is still an unfilled slot.
FILL = re.compile(r"<FILL[^>\n]*>?")
LATER = re.compile(r"<LATER[^>\n]*>?")


def targets(arg: str):
    p = Path(arg)
    if p.is_file():
        return [p]
    if p.is_dir():
        return [f for f in sorted(p.rglob("*.md"))
                if "scripts" not in f.parts and ".git" not in f.parts]
    print(f"check_fill: {arg}: not found", file=sys.stderr)
    return []


def main() -> int:
    args = sys.argv[1:]
    count_later = "--all" in args
    paths = [a for a in args if a != "--all"] or ["."]
    patterns = [FILL] + ([LATER] if count_later else [])

    remaining = 0
    for arg in paths:
        for f in targets(arg):
            for i, line in enumerate(
                    f.read_text(encoding="utf-8").splitlines(), 1):
                for pat in patterns:
                    for m in pat.finditer(line):
                        print(f"check_fill: {f.as_posix()}:{i}: {m.group(0)[:60]}",
                              file=sys.stderr)
                        remaining += 1
    if remaining:
        which = "FILL/LATER" if count_later else "FILL"
        print(f"check_fill: {remaining} {which} slot(s) remain — "
              "the semantic half is not done", file=sys.stderr)
        return 1
    print("check_fill: ok — no "
          + ("FILL or LATER" if count_later else "FILL") + " slots remain")
    return 0


if __name__ == "__main__":
    sys.exit(main())
