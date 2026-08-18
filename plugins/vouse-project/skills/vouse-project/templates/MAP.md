# MAP — <FILL: project name>

<!-- The one-page front door, always read first. Prose rows are hand-written;
the tables between BEGIN/END markers are generated — never edit inside them. -->

**What this project is:** <FILL: one sentence>.
**Canon / standing configuration:** <FILL: current default one-liner with LAW row + evidence link, or "none yet — first close sets it">.
**Read next on a cold start:** the top two entries of [LEDGER.md](LEDGER.md). Everything else is pull-on-demand.

## Where things live

| Question | Go here |
|---|---|
| How do I do a recurring task in this project | `skills/` (listed below) |
| Is this broken thing already known | `issues/` (unresolved ones listed below) |
| Standing rules and decisions, with what enforces each | [LAW.md](LAW.md) |
| What happened, in order | [LEDGER.md](LEDGER.md) |
| Frozen evidence (findings, freezes, amendments, lessons) | `record/` |
| Open and past work units | `work/` |
| How to behave while working here | [CLAUDE.md](CLAUDE.md) |
| <FILL: deep reference docs, or delete this row> | <FILL: path> |

## Milestones

A deferred future campaign or version lives HERE as a planned row (plus a
deferral sentence in the LEDGER) — never as an opened unit.

| Milestone | Target | Status |
|---|---|---|
| <FILL: name> | <FILL: date or "-"> | planned / open (unit ids) / shipped (unit id) / deferred (why) |

## State (generated — do not edit)

<!-- STATE:BEGIN -->
<!-- run: python scripts/regen_map.py . -->
<!-- STATE:END -->

## Known issues (generated — do not edit)

Unresolved only; resolved issues stay in `issues/` as history. File one with
`python scripts/new_issue.py`. Fixing routes as a `kind: patch` slice.

<!-- ISSUES:BEGIN -->
<!-- run: python scripts/regen_map.py . -->
<!-- ISSUES:END -->

## Project skills (generated — do not edit)

Portable knowhow in `skills/`, tracked in git and pushed with the repo. This
table is the only index — a skill missing from it is a skill nobody finds.
Add one with `python scripts/new_skill.py`.

<!-- SKILLS:BEGIN -->
<!-- run: python scripts/regen_map.py . -->
<!-- SKILLS:END -->
