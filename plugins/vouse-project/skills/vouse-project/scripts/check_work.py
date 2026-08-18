#!/usr/bin/env python3
"""Validate a work unit's frontmatter and its terminal-status completeness.
Facts only, no taste.

Usage: python scripts/check_work.py work/<unit>.md [...]
Exit 1 with named reasons on any violation.

A unit at a terminal status (slice `done`, campaign `closed`) may carry no
<LATER:> slots. That is what makes the deferred sections mandatory rather
than merely requested: implementation record, verification, results,
residuals, and the skills scan are all LATER slots, so a unit cannot reach
done or closed with any of them skipped.
"""
import re
import sys
from pathlib import Path

from regen_map import frontmatter  # same flat parser

SLICE_STATUS = {"draft", "ready", "in-progress", "review", "done", "deferred",
                "superseded"}
CAMPAIGN_STATUS = {"open", "closed", "deferred"}
KINDS = {"feature", "enabling", "patch"}
TERMINAL = {"done", "closed"}
LATER = re.compile(r"<LATER[^>\n]*>?")


def later_slots(path: Path, fm: dict) -> list:
    """Terminal status with unfilled deferred sections is a false claim."""
    if fm.get("status") not in TERMINAL:
        return []
    text = path.read_text(encoding="utf-8")
    heading, open_slots = "(top of file)", []
    for line in text.splitlines():
        if line.startswith("## "):
            heading = line[3:].strip()
        if LATER.search(line):
            open_slots.append(heading)
    seen, ordered = set(), []
    for h in open_slots:
        if h not in seen:
            seen.add(h)
            ordered.append(h)
    if not ordered:
        return []
    return [f"{path.name}: status `{fm['status']}` with unfilled <LATER:> "
            f"section(s): {', '.join(ordered)}. Fill them or move the status "
            "back — the skills scan in particular is posed to the owner, not "
            "skipped."]


def check(path: Path) -> list:
    errs = []
    fm = frontmatter(path)
    if not fm:
        return [f"{path.name}: no frontmatter"]
    t = fm.get("type")
    if t == "slice":
        for k in ("id", "kind", "status", "opened", "version"):
            if not fm.get(k):
                errs.append(f"{path.name}: missing `{k}`")
        if fm.get("kind") and fm["kind"] not in KINDS:
            errs.append(f"{path.name}: kind `{fm['kind']}` not in {sorted(KINDS)}")
        if fm.get("status") and fm["status"] not in SLICE_STATUS:
            errs.append(f"{path.name}: status `{fm['status']}` not in {sorted(SLICE_STATUS)}")
        if fm.get("kind") == "patch" and not fm.get("patches"):
            errs.append(f"{path.name}: kind patch requires `patches:`")
    elif t == "campaign":
        for k in ("id", "status", "opened", "one_shot", "freeze"):
            if not fm.get(k):
                errs.append(f"{path.name}: missing `{k}`")
        if fm.get("status") and fm["status"] not in CAMPAIGN_STATUS:
            errs.append(f"{path.name}: status `{fm['status']}` not in {sorted(CAMPAIGN_STATUS)}")
        fz = fm.get("freeze", "")
        if fz and not (path.parent.parent / fz).exists():
            errs.append(f"{path.name}: freeze file `{fz}` does not exist")
    else:
        errs.append(f"{path.name}: type must be slice|campaign, got `{t}`")
        return errs
    errs += later_slots(path, fm)
    return errs


def main() -> int:
    errs = []
    for a in sys.argv[1:]:
        p = Path(a)
        errs += check(p) if p.exists() else [f"{a}: not found"]
    for e in errs:
        print(f"check_work: {e}", file=sys.stderr)
    if not errs:
        print(f"check_work: ok ({len(sys.argv) - 1} file(s))")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
