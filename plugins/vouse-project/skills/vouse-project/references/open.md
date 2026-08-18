# Open — start a version or a campaign

Preconditions: the project is seeded (`MAP.md` exists — if not, run
`scripts/init.py` per SKILL.md first) and no other unit of the same kind is
open with an outstanding close (check MAP's state table; regenerate if
stale: `python scripts/regen_map.py .`).

## 1. Decide the kind first

| The owner wants to… | Open a… |
|---|---|
| Change what the system does (feature, fix, migration, delivery) | **version** containing **slices** |
| Learn how the system compares to reality (calibration, holdout, exercise, audit) | **campaign** |

A **version is not a file**: it exists as the shared `version:` field on its
slices (name them `vX.Y`), a MAP milestone row, and its LEDGER open/close
entries. If the ask mixes both kinds ("build X and prove it fits"), open
both — the campaign's freeze block states its dependency on the slice
landing first. Never fold a build step into a campaign.

**Future work the owner names but does not want started** (an intended
campaign, a later version) gets a MAP milestone row `planned (…)` and a
deferral sentence in the LEDGER entry — never an opened unit, never a
skeleton file.

## 2. Read what the project already knows

Before scoping, read MAP's two standing tables. The **issues** table says what
is already broken in the area being touched — a slice that will collide with a
known blocker is scoped differently, or scoped to fix it. The **skills** table
says which procedures are already written down, so the scoping conversation
does not re-derive them.

## 3. Grill the scope (owner conversation, not paperwork)

- **Version:** What can an actor do when this ships that they cannot today?
  Slice list, each sized to one work session with imaginable acceptance
  checks, each `kind: feature | enabling | patch`. What is explicitly out,
  and where does each deferral go? If the owner is not present, mark
  derived scope as awaiting their confirmation in the LEDGER entry — the
  `draft → ready` flip on each slice is the owner's (or their delegate's)
  act, recorded when it happens.
- **Campaign:** What question does this answer? What is the pre-registered
  comparison (bands, scored cell, reference data) — written BEFORE any
  outcome is read? What inputs must freeze (configs, seeds, data lineage —
  including how records are assigned to inputs; assignment lineage is
  first-order)? Is it one-shot?

## 4. Generate, then fill

Structure by script, semantics by you:

```
python scripts/new_unit.py --type slice --version v0.1 --slug <slug> --kind <kind>
python scripts/new_unit.py --type campaign --slug <slug> [--not-one-shot]
```

Fill the `<FILL:>` slots (for a campaign: generate the pins first —
`python scripts/pin_inputs.py --files <configs…>` — and complete the freeze
per `references/record.md`). Then prove and validate:

```
python scripts/check_fill.py work/ record/
python scripts/check_work.py work/<unit>.md
```

## 5. Register

- `python scripts/regen_map.py .` — the unit appears in MAP's state table
  (the post-commit hook also does this).
- One-line LEDGER entry: date, unit id, goal sentence, owner's words if the
  scope was their directive.

Do not auto-open the next unit at a close. Opening is deliberate.
