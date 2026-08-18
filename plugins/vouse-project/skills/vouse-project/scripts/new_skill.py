#!/usr/bin/env python3
"""Generate a project skill: directory and frontmatter by script, semantic
slots left as <FILL:> for the LLM.

Usage (from the project root, after init):
    python scripts/new_skill.py --slug regenerate-mesh [--title "Regenerate the mesh"]

Creates skills/<slug>/SKILL.md at the project root — a tracked, visible
directory, so the knowhow is pushed with every commit and travels with the
repository. Nothing loads it automatically: MAP's generated SKILLS table is
how anyone finds it, so run regen_map after creating one.
Refuses to overwrite: an existing skill is corrected by editing it.
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
    ap.add_argument("--title", help="human title (default: slug in words)")
    ap.add_argument("--date", help="YYYY-MM-DD (default: today)")
    args = ap.parse_args()

    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", args.slug):
        sys.exit("new_skill: slug must be lowercase kebab-case")
    date = args.date or datetime.date.today().isoformat()
    title = args.title or args.slug.replace("-", " ").capitalize()

    path = Path("skills") / args.slug / "SKILL.md"
    if path.exists():
        sys.exit(f"new_skill: {path.as_posix()} already exists — a skill that "
                 "is wrong or incomplete is edited, not regenerated")
    text = (TEMPLATES / "skill.md").read_text(encoding="utf-8")
    for k, v in {"SLUG": args.slug, "TITLE": title, "DATE": date}.items():
        text = text.replace("{{" + k + "}}", v)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")

    fills = len(re.findall(r"<FILL", text))
    print(f"new_skill: + {path.as_posix()} ({fills} FILL slot(s) for the LLM)")
    print("new_skill: fill the slots, then: "
          f"python scripts/check_fill.py {path.as_posix()} && "
          "python scripts/regen_map.py . "
          "(the MAP table is the only index — unlisted is unfindable)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
