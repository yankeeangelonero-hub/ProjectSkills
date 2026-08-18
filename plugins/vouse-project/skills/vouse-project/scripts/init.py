#!/usr/bin/env python3
"""Seed a fresh project: structure by script, semantics by the LLM.

Usage (run from the skill checkout):
    python <skill>/scripts/init.py <target-root> [--name "Project Name"]

Creates in <target-root>:
    MAP.md LEDGER.md LAW.md      from templates (FILL slots kept)
    CLAUDE.md                    standing instructions (skipped if present)
    work/  record/  issues/      unit, evidence and known-issue homes
    skills/                      portable project knowhow, tracked in git
    scripts/                     this suite's scripts + unit templates
    .claude/settings.json        guard hook wired (merged if file exists)
    .claude/hooks/guard_record.py
    .git/                        `git init` if absent, + post-commit hook

skills/ and issues/ ship with a README so they survive a fresh clone and
explain themselves to whoever opens them next.

Refuses if MAP.md already exists — seeding is one-shot; everything after
is open/close/route/record. Next step is printed: fill the slots, then
`python scripts/check_fill.py .`.
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
SCRIPTS = ["regen_map.py", "check_work.py", "check_record.py",
           "pin_inputs.py", "new_unit.py", "check_fill.py", "init.py",
           "new_issue.py", "check_issue.py", "new_skill.py"]
UNIT_TEMPLATES = ["slice.md", "campaign.md", "freeze-note.md", "finding.md",
                  "issue.md", "skill.md"]
# Directory -> the README seeded into it, so an empty directory still survives
# a clone and still explains itself.
DIR_READMES = {"skills": "skills-README.md", "issues": "issues-README.md"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--name")
    args = ap.parse_args()
    root = Path(args.target).resolve()
    if (root / "MAP.md").exists():
        print(f"init: {root} is already seeded (MAP.md exists) — refusing. "
              "Use open/close/route/record from here.", file=sys.stderr)
        return 1
    root.mkdir(parents=True, exist_ok=True)

    made = []
    for d in ("work", "record", "issues", "skills", "scripts",
              "scripts/templates", ".claude", ".claude/hooks"):
        (root / d).mkdir(parents=True, exist_ok=True)

    for t in ("MAP.md", "LEDGER.md", "LAW.md", "CLAUDE.md"):
        # CLAUDE.md is the one artefact a target repo may already own; seeding
        # over it would destroy instructions this suite knows nothing about.
        if t == "CLAUDE.md" and (root / t).exists():
            print("init: CLAUDE.md already exists - left untouched. Merge the "
                  "standing rules from the skill's templates/CLAUDE.md by "
                  "hand, or the skills and issues rules go unstated.",
                  file=sys.stderr)
            continue
        text = (SKILL / "templates" / t).read_text(encoding="utf-8")
        if args.name:
            text = text.replace("<FILL: project name>", args.name)
        (root / t).write_text(text, encoding="utf-8", newline="\n")
        made.append(t)

    for d, readme in DIR_READMES.items():
        target = root / d / "README.md"
        if not target.exists():
            shutil.copy2(SKILL / "templates" / readme, target)
            made.append(f"{d}/README.md")

    for s in SCRIPTS:
        shutil.copy2(SKILL / "scripts" / s, root / "scripts" / s)
        made.append(f"scripts/{s}")
    for t in UNIT_TEMPLATES:
        shutil.copy2(SKILL / "templates" / t, root / "scripts" / "templates" / t)
        made.append(f"scripts/templates/{t}")

    shutil.copy2(SKILL / "hooks" / "guard_record.py",
                 root / ".claude" / "hooks" / "guard_record.py")
    made.append(".claude/hooks/guard_record.py")

    settings_path = root / ".claude" / "settings.json"
    settings = {}
    if settings_path.exists():
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
    hook_entry = {"matcher": "Write|Edit", "hooks": [
        {"type": "command", "command": "python .claude/hooks/guard_record.py"}]}
    pre = settings.setdefault("hooks", {}).setdefault("PreToolUse", [])
    if not any("guard_record" in str(e) for e in pre):
        pre.append(hook_entry)
    settings_path.write_text(json.dumps(settings, indent=2) + "\n",
                             encoding="utf-8", newline="\n")
    made.append(".claude/settings.json")

    if not (root / ".git").exists():
        try:
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            made.append(".git/")
        except Exception as e:  # git optional; state it, don't fail
            print(f"init: git init skipped ({e}) — post-commit hook not "
                  "installed; MAP regeneration is manual.", file=sys.stderr)
    hook_dir = root / ".git" / "hooks"
    if hook_dir.is_dir():
        pc = hook_dir / "post-commit"
        pc.write_text((SKILL / "hooks" / "post-commit.sample")
                      .read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
        try:
            pc.chmod(0o755)
        except Exception:
            pass
        made.append(".git/hooks/post-commit")

    # Render the initial generated state table before the first commit. Without
    # this, the post-commit hook dirties a freshly seeded repository.
    subprocess.run([sys.executable, str(root / "scripts" / "regen_map.py"), "."],
                   cwd=root, check=True)

    for m in made:
        print(f"init: + {m}")
    seeded_docs = " ".join(d for d in ("MAP.md", "LEDGER.md", "CLAUDE.md")
                           if d in made)
    print(f"init: seeded. Next: fill the <FILL:> slots in {seeded_docs} "
          "(the LLM's job - semantics only), open the first unit with "
          "`python scripts/new_unit.py`, prove completion with "
          f"`python scripts/check_fill.py {seeded_docs}`, then make the first "
          "commit (the post-commit hook keeps MAP's generated tables fresh).")
    print("init: skills/ and issues/ start empty and stay that way until the "
          "work produces them. Every slice and campaign close poses the "
          "skills scan to the owner - see the close reference.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
