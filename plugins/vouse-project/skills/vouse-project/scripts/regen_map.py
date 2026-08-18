#!/usr/bin/env python3
"""Rebuild MAP.md's generated tables from ground truth.

Usage: python scripts/regen_map.py <project-root>

Three blocks, each derived from files on disk and each replaced between its
own markers in MAP.md:

  STATE   <- work/*.md frontmatter      (units and their status)
  ISSUES  <- issues/*.md frontmatter    (unresolved known issues)
  SKILLS  <- skills/*/SKILL.md          (portable project knowhow)

Derived state only: this script never touches prose. STATE markers are
required; ISSUES and SKILLS markers are optional so that projects seeded
before those blocks existed keep working — their absence is reported, never
silently ignored. Wire this as a git post-commit hook so no table can rot.

The SKILLS table is also the discovery mechanism: skills/ is not a path any
agent loads automatically, so a skill that is not listed in MAP is a skill
nobody will find.
"""
import re
import sys
from pathlib import Path

STATUS_ORDER = {"open": 0, "in-progress": 0, "draft": 1, "ready": 1,
                "review": 2, "done": 3, "closed": 3, "deferred": 4,
                "superseded": 5}
SEVERITY_ORDER = {"blocker": 0, "major": 1, "minor": 2}
UNRESOLVED = ("open", "mitigated")


def frontmatter(path: Path) -> dict:
    """Flat YAML frontmatter, plus folded/literal block scalars (`key: >-`).

    Enough YAML for the fields this suite writes and no more; anything richer
    belongs in prose, not frontmatter.
    """
    text = path.read_text(encoding="utf-8")
    m = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    out, folding = {}, None
    for line in m.group(1).splitlines():
        if folding and (line.startswith((" ", "\t")) or not line.strip()):
            out[folding] = (out[folding] + " " + line.strip()).strip()
            continue
        folding = None
        if ":" in line and not line.startswith((" ", "\t")):
            k, v = line.split(":", 1)
            k, v = k.strip(), v.strip()
            if v in (">", ">-", "|", "|-"):
                out[k], folding = "", k
            else:
                out[k] = v
    return out


def cell(value: str, limit: int = 110) -> str:
    """One table cell: no pipes, no newlines, first sentence, bounded."""
    v = " ".join(str(value).split()).replace("|", "/")
    first = re.split(r"(?<=[.!?])\s", v, maxsplit=1)[0]
    if len(first) > limit:
        first = first[:limit - 1].rstrip() + "…"
    return first


def unit_rows(root: Path):
    work = root / "work"
    rows = []
    for f in sorted(work.glob("*.md")) if work.is_dir() else []:
        fm = frontmatter(f)
        if not fm.get("id"):
            continue
        rows.append((fm["id"], fm.get("type", "?"), fm.get("status", "?"),
                     fm.get("opened", ""), f.name))
    rows.sort(key=lambda r: (STATUS_ORDER.get(r[2], 9), r[3]))
    if not rows:
        return ["_No work units._"], 0
    return (["| Unit | Type | Status | Opened |", "|---|---|---|---|"]
            + [f"| [{i}](work/{fn}) | {t} | {s} | {o} |"
               for i, t, s, o, fn in rows]), len(rows)


def issue_rows(root: Path):
    issues = root / "issues"
    live, resolved = [], 0
    for f in sorted(issues.glob("*.md")) if issues.is_dir() else []:
        fm = frontmatter(f)
        if not fm.get("id"):
            continue
        if fm.get("status") not in UNRESOLVED:
            resolved += 1
            continue
        live.append((fm["id"], fm.get("severity", "?"), fm.get("status", "?"),
                     fm.get("affects", ""), fm.get("opened", ""), f.name))
    live.sort(key=lambda r: (SEVERITY_ORDER.get(r[1], 9), r[4]))
    tail = [f"_{resolved} resolved issue(s) in `issues/`._"] if resolved else []
    if not live:
        return ["_No unresolved issues._"] + tail, 0
    return (["| Issue | Severity | Status | Affects | Opened |",
             "|---|---|---|---|---|"]
            + [f"| [{i}](issues/{fn}) | {sv} | {st} | {cell(af, 60)} | {op} |"
               for i, sv, st, af, op, fn in live] + tail), len(live)


def skill_rows(root: Path):
    skills = root / "skills"
    rows = []
    for f in sorted(skills.glob("*/SKILL.md")) if skills.is_dir() else []:
        fm = frontmatter(f)
        rows.append((fm.get("name") or f.parent.name,
                     cell(fm.get("description", "")), f.parent.name))
    if not rows:
        return ["_No project skills yet._"], 0
    return (["| Skill | Use when |", "|---|---|"]
            + [f"| [{n}](skills/{d}/SKILL.md) | {desc} |"
               for n, desc, d in rows]), len(rows)


def replace(text: str, tag: str, lines: list, required: bool):
    block = (f"<!-- {tag}:BEGIN -->\n"
             "<!-- run: python scripts/regen_map.py . -->\n"
             + "\n".join(lines) + f"\n<!-- {tag}:END -->")
    new, n = re.subn(rf"<!-- {tag}:BEGIN -->.*?<!-- {tag}:END -->",
                     lambda _m: block, text, flags=re.DOTALL)
    if n == 1:
        return new, None
    if n > 1:
        return text, f"{tag} markers duplicated in MAP.md"
    if required:
        return text, f"{tag} markers missing from MAP.md"
    return text, (f"{tag} markers absent — add `<!-- {tag}:BEGIN -->` / "
                  f"`<!-- {tag}:END -->` to MAP.md to track this table there")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    map_path = root / "MAP.md"
    if not map_path.exists():
        print(f"regen_map: no MAP.md at {map_path}", file=sys.stderr)
        return 1

    blocks = [("STATE", unit_rows(root), True),
              ("ISSUES", issue_rows(root), False),
              ("SKILLS", skill_rows(root), False)]
    text = map_path.read_text(encoding="utf-8")
    fatal, counts = False, []
    for tag, (lines, n), required in blocks:
        text, problem = replace(text, tag, lines, required)
        if problem:
            print(f"regen_map: {problem}", file=sys.stderr)
            fatal = fatal or required or "duplicated" in problem
        else:
            counts.append(f"{tag.lower()} {n}")
    if fatal:
        return 1
    map_path.write_text(text, encoding="utf-8", newline="\n")
    print(f"regen_map: {', '.join(counts)} row(s) -> MAP.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
