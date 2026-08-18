#!/usr/bin/env python3
"""Generate a known-issue file: frontmatter by script, semantic slots left as
<FILL:> for the LLM.

Usage (from the project root, after init):
    python scripts/new_issue.py --slug map-table-drift --severity major \
        [--affects scripts/regen_map.py]

Creates issues/issue-<date>-<slug>.md. Refuses to overwrite. Unlike record/,
issues are living documents: status, workaround and diagnosis are edited in
place as they change.
"""
import argparse
import datetime
import re
import sys
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent / "templates"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True, help="lowercase kebab-case")
    ap.add_argument("--severity", required=True,
                    choices=["blocker", "major", "minor"])
    ap.add_argument("--affects", default="<FILL: component, file, or area>")
    ap.add_argument("--date", help="YYYY-MM-DD (default: today)")
    args = ap.parse_args()

    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", args.slug):
        sys.exit("new_issue: slug must be lowercase kebab-case")
    date = args.date or datetime.date.today().isoformat()
    uid = f"issue-{date}-{args.slug}"

    path = Path("issues") / f"{uid}.md"
    if path.exists():
        sys.exit(f"new_issue: {path.as_posix()} already exists — refusing to "
                 "overwrite")
    text = (TEMPLATES / "issue.md").read_text(encoding="utf-8")
    for k, v in {"ID": uid, "SEVERITY": args.severity, "DATE": date,
                 "AFFECTS": args.affects}.items():
        text = text.replace("{{" + k + "}}", v)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")

    fills = len(re.findall(r"<FILL", text))
    print(f"new_issue: + {path.as_posix()} ({fills} FILL slot(s) for the LLM)")
    print("new_issue: fill the slots, then: "
          f"python scripts/check_issue.py {path.as_posix()} && "
          f"python scripts/check_fill.py {path.as_posix()} && "
          "python scripts/regen_map.py .")
    return 0


if __name__ == "__main__":
    sys.exit(main())
