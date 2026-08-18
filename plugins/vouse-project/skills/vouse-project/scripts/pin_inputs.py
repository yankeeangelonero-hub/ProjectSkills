#!/usr/bin/env python3
"""Emit the sha256 pin table for a freeze note. A freeze without pins is not
a freeze.

Usage: python scripts/pin_inputs.py --files <path> [<path> ...] [--out <file>]
Prints (or appends to --out) a markdown table: File | sha256 | Bytes.
"""
import argparse
import hashlib
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--files", nargs="+", required=True)
    ap.add_argument("--out")
    args = ap.parse_args()

    rows, missing = [], []
    for f in args.files:
        p = Path(f)
        if not p.is_file():
            missing.append(f)
            continue
        data = p.read_bytes()
        rows.append(f"| `{p.as_posix()}` | `{hashlib.sha256(data).hexdigest()}` | {len(data)} |")
    if missing:
        for m in missing:
            print(f"pin_inputs: missing {m}", file=sys.stderr)
        return 1

    table = "| File | sha256 | Bytes |\n|---|---|---|\n" + "\n".join(rows) + "\n"
    if args.out:
        with open(args.out, "a", encoding="utf-8", newline="\n") as fh:
            fh.write(table)
        print(f"pin_inputs: {len(rows)} pin(s) -> {args.out}")
    else:
        print(table, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
