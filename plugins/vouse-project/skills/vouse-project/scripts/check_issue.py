#!/usr/bin/env python3
"""Validate a known-issue file's frontmatter. Facts only, no taste.

Usage: python scripts/check_issue.py issues/<file>.md [...]
- Filename must be issue-YYYY-MM-DD-<slug>.md.
- Required fields: id, type, status, severity, opened, affects.
- status fixed|mitigated requires `fixed_by:` (the unit id that did it, or
  for mitigated, the workaround's owner reference).
- status duplicate requires `duplicate_of:` naming an existing issue file.
- status wontfix requires `reason:`.
issues/README.md is the directory's own explainer, not an issue: it is
reported as skipped, never as a violation.
Exit 1 with named reasons on any violation.
"""
import re
import sys
from pathlib import Path

from regen_map import frontmatter

NAME = re.compile(r"^issue-\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*\.md$")
STATUS = {"open", "mitigated", "fixed", "wontfix", "duplicate"}
SEVERITY = {"blocker", "major", "minor"}


def check(path: Path) -> list:
    errs = []
    if not NAME.match(path.name):
        errs.append(f"{path.name}: name must be issue-YYYY-MM-DD-<slug>.md")
    fm = frontmatter(path)
    if not fm:
        return errs + [f"{path.name}: no frontmatter"]
    if fm.get("type") != "issue":
        errs.append(f"{path.name}: type must be `issue`, got `{fm.get('type')}`")
    for k in ("id", "status", "severity", "opened", "affects"):
        if not fm.get(k):
            errs.append(f"{path.name}: missing `{k}`")
    st, sev = fm.get("status"), fm.get("severity")
    if st and st not in STATUS:
        errs.append(f"{path.name}: status `{st}` not in {sorted(STATUS)}")
    if sev and sev not in SEVERITY:
        errs.append(f"{path.name}: severity `{sev}` not in {sorted(SEVERITY)}")
    if st in ("fixed", "mitigated") and not fm.get("fixed_by"):
        errs.append(f"{path.name}: status `{st}` requires `fixed_by:` "
                    "(the unit id that did it)")
    if st == "wontfix" and not fm.get("reason"):
        errs.append(f"{path.name}: status wontfix requires `reason:`")
    if st == "duplicate":
        dup = fm.get("duplicate_of")
        if not dup:
            errs.append(f"{path.name}: status duplicate requires `duplicate_of:`")
        elif not (path.parent / dup).exists():
            errs.append(f"{path.name}: duplicate_of `{dup}` does not exist in "
                        f"{path.parent.as_posix()}")
    return errs


def main() -> int:
    errs, checked, skipped = [], 0, 0
    for a in sys.argv[1:]:
        p = Path(a)
        if p.name.lower() == "readme.md":
            skipped += 1
            continue
        if not p.exists():
            errs.append(f"{a}: not found")
            continue
        checked += 1
        errs += check(p)
    for e in errs:
        print(f"check_issue: {e}", file=sys.stderr)
    if not errs:
        tail = f", {skipped} README skipped" if skipped else ""
        print(f"check_issue: ok ({checked} file(s){tail})")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
