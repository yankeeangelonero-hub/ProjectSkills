#!/usr/bin/env python3
"""Validate a record/ file before commit: naming, append-only, supersession.

Usage: python scripts/check_record.py record/<file>.md [...]
- Filename must be <kind>-YYYY-MM-DD-<slug>.md, kind in
  finding|freeze|amendment|lesson.
- If frontmatter has `supersedes:`, the target must exist in record/.
(Append-only enforcement at write time is the guard hook's job; this script
is the commit-time backstop.)
"""
import re
import sys
from pathlib import Path

from regen_map import frontmatter

NAME = re.compile(r"^(finding|freeze|amendment|lesson)-\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*\.md$")


def main() -> int:
    errs = []
    for a in sys.argv[1:]:
        p = Path(a)
        if not p.exists():
            errs.append(f"{a}: not found")
            continue
        if not NAME.match(p.name):
            errs.append(f"{p.name}: name must be <finding|freeze|amendment|lesson>-YYYY-MM-DD-<slug>.md")
        sup = frontmatter(p).get("supersedes")
        if sup and not (p.parent / sup).exists():
            errs.append(f"{p.name}: supersedes `{sup}` which does not exist in {p.parent}")
    for e in errs:
        print(f"check_record: {e}", file=sys.stderr)
    if not errs:
        print(f"check_record: ok ({len(sys.argv) - 1} file(s))")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
