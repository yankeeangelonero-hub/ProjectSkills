# Issues — the known-defect tracker

`issues/` holds one file per known bug or limitation:
`issue-YYYY-MM-DD-<slug>.md`. Unresolved issues appear in MAP's generated
table; resolved ones stay in the directory as history and drop out of the
table. Filing is cheap and expected; the tracker exists so that the same
defect is diagnosed once.

## What is an issue

An issue is a **defect in something already shipped or in use**. It is not a
task, not a question, and not a result.

| Ask | Home |
|---|---|
| "This is broken and I am not fixing it right now" | `issues/` |
| "Build this" / "Fix this now" | a slice (`references/open.md`) |
| "Does the system match reality?" | a campaign |
| "Here is what the measurement showed" | `record/finding-…` |
| "Never do this again, and here is the gate" | `LAW.md` row |

Filing an issue is not scheduling a fix. Fixing routes as a `kind: patch`
slice whose `patches:` field names the issue id — the issue is the report, the
slice is the work. The two are never the same file.

## Filing

```
python scripts/new_issue.py --slug <slug> --severity blocker|major|minor \
    [--affects <component or path>]
python scripts/check_issue.py issues/<file>.md
python scripts/check_fill.py issues/<file>.md
python scripts/regen_map.py .
```

Severity is about impact, not effort: **blocker** stops work or produces wrong
published output; **major** has a workaround but costs real time; **minor** is
noise that someone will otherwise re-diagnose.

The **Workaround** section is why the file earns its place. Write it even when
it is ugly, and write "none known" when there is none — an issue with an empty
workaround section is indistinguishable from one nobody has thought about.

**Root cause** and **Resolution** are `<LATER:>` slots. Until root cause is
filled, the file is a symptom record and callers must treat it as one: a guess
written into that section as if diagnosed is worse than a blank.

## Living, not frozen

Issues are edited in place — status, workaround, and diagnosis change as
understanding does. This is the opposite of `record/`, and deliberate: a
frozen record is evidence about a moment, an issue is a claim about the
present. The guard hook does not cover `issues/`.

Statuses, and what `check_issue.py` requires of each:

| Status | Means | Required |
|---|---|---|
| `open` | Reproduced, no workaround in use | — |
| `mitigated` | A workaround is in use; the defect remains | `fixed_by:` |
| `fixed` | Gone, with a check that proves it | `fixed_by:` (the unit id) |
| `wontfix` | A decision not to fix it | `reason:` |
| `duplicate` | Another file owns it | `duplicate_of:` (must exist) |

`fixed` without a `fixed_by` unit id is a claim with no evidence, so the
script refuses it. If a defect disappeared and nobody knows which change did
it, that is `open` with a note, not `fixed`.

## At open and at close

- **At open** — read MAP's issues table before scoping. A slice that will
  collide with a known blocker is scoped differently, or scoped to fix it.
- **At close** — reconcile every issue the closing scope touched: fixed ones
  get their status and `fixed_by`, new ones discovered during the work get
  filed rather than mentioned, and anything left open stays visible in MAP.
  A close that quietly leaves a discovered defect unfiled has converted a
  known issue into an unknown one.

## Red flags

- A defect described in chat or a commit message and nowhere else
- `fixed` with no unit id, or with a unit that never mentions it
- An issue file that has become the fix's design document — that is a slice
- A tracker where nothing is ever closed: unresolved counts that only grow
  mean the table is being written and not read
- Filing an issue as a substitute for telling the owner something is blocking
