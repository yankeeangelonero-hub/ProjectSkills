#!/usr/bin/env python3
"""Generate a work unit: frontmatter and file mechanics by script, semantic
slots left as <FILL:> for the LLM.

Usage (from the project root, after init):
    python scripts/new_unit.py --type slice --version v0.1 --slug temp-sensor --kind feature
    python scripts/new_unit.py --type campaign --slug sensor-accuracy [--not-one-shot]

Slices:    work/<version>-slice-<slug>.md   (id = <version>-slice-<slug>)
Campaigns: work/campaign-<date>-<slug>.md   + record/freeze-<date>-<slug>.md skeleton
Refuses to overwrite. Prints the created paths and the remaining FILL count.
"""
import argparse
import datetime
import re
import sys
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent / "templates"


def render(template: str, subs: dict) -> str:
    text = (TEMPLATES / template).read_text(encoding="utf-8")
    for k, v in subs.items():
        text = text.replace("{{" + k + "}}", v)
    return text


def write_new(path: Path, text: str) -> None:
    if path.exists():
        sys.exit(f"new_unit: {path} already exists — refusing to overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    fills = len(re.findall(r"<FILL", text))
    print(f"new_unit: + {path.as_posix()} ({fills} FILL slot(s) for the LLM)")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", required=True, choices=["slice", "campaign"])
    ap.add_argument("--slug", required=True)
    ap.add_argument("--version", help="required for slices, e.g. v0.1")
    ap.add_argument("--kind", choices=["feature", "enabling", "patch"],
                    default="feature")
    ap.add_argument("--not-one-shot", action="store_true")
    ap.add_argument("--date", help="YYYY-MM-DD (default: today)")
    args = ap.parse_args()

    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", args.slug):
        sys.exit("new_unit: slug must be lowercase kebab-case")
    date = args.date or datetime.date.today().isoformat()

    if args.type == "slice":
        if not args.version:
            sys.exit("new_unit: slices require --version (e.g. v0.1)")
        uid = f"{args.version}-slice-{args.slug}"
        write_new(Path("work") / f"{uid}.md",
                  render("slice.md", {"ID": uid, "KIND": args.kind,
                                      "DATE": date, "VERSION": args.version}))
    else:
        uid = f"campaign-{date}-{args.slug}"
        freeze = f"record/freeze-{date}-{args.slug}.md"
        write_new(Path(freeze),
                  render("freeze-note.md", {"ID": uid, "DATE": date}))
        write_new(Path("work") / f"{uid}.md",
                  render("campaign.md", {
                      "ID": uid, "DATE": date, "FREEZE": freeze,
                      "ONE_SHOT": "false" if args.not_one_shot else "true"}))

    print("new_unit: fill the slots, then validate: "
          f"python scripts/check_work.py work/{uid}.md && "
          "python scripts/check_fill.py work/ && "
          "python scripts/regen_map.py .")
    return 0


if __name__ == "__main__":
    sys.exit(main())
