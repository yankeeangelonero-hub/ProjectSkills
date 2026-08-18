# <FILL: project name> — working agreement

Standing instructions for anyone (human or agent) working in this repository.
This file carries **behaviour**; [MAP.md](MAP.md) carries **state**. Never
restate state here — point at it.

## Start here

Read [MAP.md](MAP.md), then the top two entries of [LEDGER.md](LEDGER.md).
Everything else is pull-on-demand.

## Standing rules

- **Before doing a recurring task, check the skills table in [MAP.md](MAP.md)
  and read the matching file under `skills/`.** These are this project's
  portable knowhow — the things a competent newcomer would otherwise get wrong.
  Nothing loads them for you; looking is your job. If one covers what you are
  about to do, follow it.
- **When a skill turns out to be wrong or incomplete, fix it in the same
  session.** Skills are living documents; a stale skill is worse than none.
- **Every slice, version, and campaign close poses the skills scan to the
  owner**, in these words: "This work taught us X, Y, Z. Should any of it
  become a project skill, or update an existing one?" Name the candidates
  concretely. Record their answer — including an explicit "nothing portable
  here" — in the unit's `## Skills scan` section. Never answer it on their
  behalf. `check_work.py` refuses `done` / `closed` while that slot is
  unfilled, so this is a gate, not a suggestion.
- **When you explain the same project-specific procedure a third time, write
  it as a skill** (`python scripts/new_skill.py --slug <slug>`, then
  `regen_map` so it reaches the index), and tell the owner it exists.
- **Before debugging, check `issues/`.** A known bug may already have a
  recorded workaround. When you hit a new one that is not being fixed right
  now, file it: `python scripts/new_issue.py --slug <slug> --severity <sev>`.
- **`record/` is append-only.** Corrections are new dated files with
  `supersedes:` — never edits. A hook enforces this.
- **Generated blocks are generated.** Anything between `BEGIN`/`END` markers
  in MAP.md comes from `python scripts/regen_map.py .`. Never hand-edit inside.
- **Lifecycle work runs through the `vouse-project` skill** — opening and
  closing versions and campaigns, routing change requests, recording findings.

## Verification

<FILL: the commands that prove this project is not broken — test suite, build,
lint — one per line with what each covers. If there are none yet, say so.>

## Project-specific instructions

<FILL: standing instructions unique to this project — environment quirks,
things never to touch, review conventions. Delete this section if there are
none; do not leave it empty.>
