---
description: Set up vouse-project management structure in a repository — fresh or work-in-progress. Run once per project.
argument-hint: "[target-directory] — defaults to the current directory"
disable-model-invocation: false
---

Set this repository up for `vouse-project` lifecycle management, end to end, in
one pass. This is a **one-time** command: after it completes, everything else
runs through the `vouse-project` skill (open, close, route, record).

The user invoked this command with: $ARGUMENTS

## What you are producing

A seeded project: `MAP.md`, `LEDGER.md`, `LAW.md`, `CLAUDE.md`, plus `work/`,
`record/`, `issues/`, `skills/`, the deterministic scripts, the append-only
record guard hook, and a post-commit hook that keeps MAP's generated tables
fresh. Structure comes from a script; meaning comes from you and the owner.

**REQUIRED SUB-SKILL:** invoke `bob-write` before writing any prose here. Every
surface this produces — LEDGER entries, MAP prose rows, LAW rows, filled slots —
is written in that register.

## Step 1 — Resolve the target and check it is not already seeded

Target root = `$ARGUMENTS` if given, else the current working directory.

If `MAP.md` already exists at the target, **stop**. The project is seeded;
seeding is one-shot. Tell the user so and point them at the lifecycle workflows
in the `vouse-project` skill (open / close / route / record). Do not re-run the
seed and do not hand-patch a partial one.

## Step 2 — Run the seed

```
python "${CLAUDE_PLUGIN_ROOT}/skills/vouse-project/scripts/init.py" <target> --name "<project name>"
```

Use the repository's real name for `--name`; ask the user if it is not obvious
from the directory or an existing README.

The script is non-destructive on an existing repository: it skips `git init` if
`.git` exists, merges its hook into an existing `.claude/settings.json` without
disturbing other keys, leaves an existing `CLAUDE.md` untouched (and says so),
and never overwrites files already present. Read its output — it lists exactly
what it created and what it skipped.

If it reported that it left an existing `CLAUDE.md` alone, merge the standing
rules from `${CLAUDE_PLUGIN_ROOT}/skills/vouse-project/templates/CLAUDE.md` into
that file by hand, keeping the user's existing instructions. Those rules are how
anyone working here learns that `skills/` and `issues/` exist.

## Step 3 — Decide which project this is

Look at the target: does it contain existing work? Check for source files, a
README with real content, commit history beyond an initial commit, an issue
tracker, TODO comments, or existing documentation.

- **Fresh project** (empty or near-empty) → go to Step 4.
- **Work in progress** → read
  `${CLAUDE_PLUGIN_ROOT}/skills/vouse-project/references/adopt.md` and run the
  adoption pass it describes, then continue to Step 4. Do not skip this. A
  seeded structure sitting beside months of undocumented decisions is a second
  front door that disagrees with the first.

## Step 4 — Fill the slots (the semantic half)

The script left `<FILL:>` markers. They are yours and the owner's, not the
script's. Fill them by asking, not by inventing:

- **MAP.md** — what this project is in one sentence; the canon line (or "none
  yet — first close sets it"); the milestone rows, including work the owner
  names but does not want started yet.
- **LEDGER.md** — the seed entry: the owner's brief in their own words where
  possible, what was seeded, what the first unit will be, what is deliberately
  deferred. For an adopted repository, this entry also carries the history
  summary from the adoption pass.
- **CLAUDE.md** — the verification commands that prove this project is not
  broken (test suite, build, lint), and any project-specific standing
  instructions. If there are none, say so rather than leaving the slot.

Ask the owner the questions you cannot answer from the repository. Do not fill a
slot with a plausible guess — an invented canon line or a wrong verification
command is worse than an unfilled marker, because the marker is visible and the
guess is not.

## Step 5 — Prove it, then commit

```
python scripts/check_fill.py MAP.md LEDGER.md CLAUDE.md
```

Exit 0 or the semantic half is not done. Fix what it names and run it again.

Then commit. The post-commit hook regenerates MAP's state, issues, and skills
tables, so the first commit leaves them accurate.

## Step 6 — Hand off

Tell the user, briefly:

- what was created, and what was skipped because it already existed
- for an adopted repository: what the adoption pass wrote into LAW, issues, and
  skills, and what it deliberately left out
- that the next step is opening the first unit — `python scripts/new_unit.py` —
  and that everything from here runs through the `vouse-project` skill
- that this command does not need to be run again

## Do not

- Hand-type frontmatter, ids, dates, or file skeletons — the scripts own those.
- Invent LAW rows, issues, or skills the owner has not confirmed.
- Open the first work unit as part of setup. Opening is deliberate and belongs
  to the owner.
- Claim a gate that is not installed. If you describe a check, it exists.
