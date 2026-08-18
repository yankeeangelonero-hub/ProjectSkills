# Project skills

Portable knowhow for this project. One directory per skill, each containing a
`SKILL.md` with `name` and `description` frontmatter. This directory is tracked
in git, so the knowledge travels with the repository and is pushed with every
commit — which is the point. This is what would otherwise live in one person's
head.

Create one with `python scripts/new_skill.py --slug <slug>` from the project
root. Do not hand-write the directory or frontmatter.

Nothing loads these automatically. MAP's generated skills table is the index —
run `python scripts/regen_map.py .` after adding or renaming one, or it will
not be found.

**What belongs here:** a procedure that recurs, that a competent newcomer would
get wrong, and that is specific to this project.

**What does not:** standing decisions (they are `LAW.md` rows), frozen evidence
(`record/`), known defects (`issues/`), and general engineering knowledge.

Skills are living documents — edit them the moment reality contradicts them.
They carry no evidential weight, so a correction is an edit, not a supersession.
