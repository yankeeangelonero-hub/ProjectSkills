# Skills — portable knowhow that leaves with the repository, not the person

`skills/` holds one directory per skill, each a `SKILL.md` with `name` and
`description` frontmatter. The directory is tracked in git at the project
root, so the knowledge is pushed with every commit and arrives with the clone.
This is the answer to knowhow that otherwise lives in one person's head and
leaves when they do.

Nothing loads these automatically. MAP's generated skills table is the index;
a skill absent from that table is a skill nobody finds. Run
`python scripts/regen_map.py .` after adding, renaming, or retiring one.

## What is a skill, and what is not

A skill is a **procedure** that recurs, that a competent newcomer gets wrong,
and that is specific to this project. The three conditions are conjunctive.

| Content | Home | Why not a skill |
|---|---|---|
| "Always use the pinned solver version" | `LAW.md` row | It is a decision, not a procedure; it needs *enforced by* |
| "The 2025-11 comparison missed 4 of 24 cases" | `record/finding-…` | It is evidence; it is frozen, skills are living |
| "The exporter drops the last frame" | `issues/` | It is a defect awaiting a fix, not a way of working |
| "How to write a Python decorator" | nowhere | General knowledge, not project-specific |
| "Run `make dev` before tests" | skill, if it recurs and surprises | Meets all three conditions |

A skill that only restates a script's `--help` output is not a skill. Point at
the script instead, or write down the part the `--help` does not say: which
flag combination is correct here, and what the failure looks like.

## When to write one

Two triggers, both mandatory:

1. **The third explanation.** The same project-specific procedure explained
   twice is a coincidence. The third time, it is a missing skill. Write it
   before answering the third time.
2. **Every slice and campaign close.** The `## Skills scan` section is a
   `<LATER:>` slot in both unit templates, and `check_work.py` refuses `done`
   or `closed` while it is unfilled. See `references/close.md` for the exact
   question posed to the owner and what counts as an answer.

Both triggers are proposals, not unilateral acts. The owner decides whether
knowhow is standing; you draft it, they confirm. Their answer goes in the
scan slot verbatim, including "nothing portable here" and its reason — a
recorded no is a result, an absent answer is a skipped step.

## Writing one

```
python scripts/new_skill.py --slug <slug> [--title "Human title"]
python scripts/check_fill.py skills/<slug>/SKILL.md
python scripts/regen_map.py .
```

The script owns the directory and the frontmatter. You own the slots.

The `description` is the trigger, written in the reader's words, not yours:
what situation brings someone here. It is the only text most readers see,
because it is what MAP's table shows. "Use when regenerating the mesh after a
geometry change" finds its reader; "Mesh notes" does not.

The `What goes wrong` section is why the skill exists. A procedure with no
recorded failures is documentation; a procedure with the newcomer's actual
error beside its signal and its fix is a skill. If nothing has gone wrong yet,
write "not yet observed" and add rows as it does.

## Updating and retiring

Skills are **living documents**. They carry no evidential weight, so a
correction is an edit, not a supersession — the opposite of `record/`, and the
distinction matters: the guard hook blocks record edits and permits these.

- **Contradicted by reality** — edit it in the same session, while the correct
  procedure is still in front of you. A skill that describes what used to work
  is the lying-board failure in a new costume: it is read, believed, and wrong.
- **Now enforced by a script or hook** — delete the prose and point at the
  gate. Enforcement outranks instruction; a skill that duplicates a gate rots
  the moment the gate changes.
- **Subsystem removed** — delete the skill in the same slice that removes the
  subsystem, and say so in the LEDGER entry. Deleted skills are not archived;
  git holds the history.

Editing an existing skill is a tier-1 change (`references/route.md`) — a one
line note in the unit, no ceremony. Creating one is the owner's call. Deleting
one is stated in the LEDGER.

## Red flags

- A skill written but never added to MAP's table — unlisted is unfindable
- A skill whose `What goes wrong` section is empty after months of use
- Explaining a procedure in chat for the third time instead of writing it
- A skill and a LAW row asserting the same thing — the LAW row wins, the skill
  cites it
- A skills scan answered by the agent instead of the owner
