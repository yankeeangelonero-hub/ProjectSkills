---
name: vouse-project
description: >-
  Use when managing a project's lifecycle state: seeding a fresh project's
  management structure, starting or finishing a body of work ("open a
  version", "start a campaign", "close this version"), recording results
  that must not be edited later (findings, freeze notes, amendments,
  lessons), triaging a change request ("where does this fix go?"),
  promoting a decision to standing law or canon, capturing project knowhow
  as a portable skill other people inherit, filing or reconciling a known
  bug, or when a session starts cold and needs project state ("where are
  we?"). Also use when project
  state documents look stale, contradictory, or hand-maintained — boards
  showing zero items, changelogs that skip events, decisions living only
  in chat.
---

# vouse-project — lifecycle management on a fixed set of artefacts

## Overview

A project is a small fixed set of documents plus work units. Skills judge; scripts execute;
hooks enforce. State is derived from ground truth or it does not exist.

**Scaffold-then-fill (the division of labour).** Every artefact this suite
produces is made in two halves: a **script generates the structure** —
files, directories, frontmatter, ids, dates, tables, pin blocks — leaving
explicit slots; the **LLM fills only the slots** — scope, acceptance
values, meaning, prose; and `check_fill` **proves the semantic half is
done**. Two slot markers: `<FILL: …>` is due now (counted always);
`<LATER: …>` is due at the named later stage — build, verify, after runs,
close — and is counted only by `check_fill --all`, the close-time proof.
Never delete a LATER marker except by filling it. If you are typing
frontmatter, an id, a date, or a file skeleton by hand, stop — a script
owns that; your work starts at the first slot.

**Register.** Every prose surface this suite produces — LEDGER entries,
findings and other `record/` files, MAP prose rows, filled unit slots — is
written in the bob specification register: flat, declarative,
condition-first, exact, one term per concept, failure case beside the happy
case, no evaluative language. **REQUIRED SUB-SKILL:** `bob-write` (sibling
skill in this repo). Bold structural labels that templates ship (e.g.
`**Builds:**`) are field names, not emphasis, and stay.

**The artefact model (one fact, one home, one writer):**

| Artefact | What | Writer |
|---|---|---|
| `MAP.md` | One-page front door: canon, open work, milestones (including deferred future work as planned rows), plus the generated issue and skill indexes. Read first, always. | `regen_map.py` (three generated tables) + seed/open/close workflows (prose rows) |
| `CLAUDE.md` | Standing instructions for anyone working here — behaviour, never state. Points at MAP; never restates it. | seed workflow, then tier-1 edits |
| `LEDGER.md` | Append-only dated narrative — one entry per event (seed, open, close, canon change). | close/record workflows |
| `LAW.md` | Invariants + standing decisions. Every row: *decided when / evidence / enforced by*. "Enforced by" names a real test, script, or hook — or says `convention`. | close workflow (via route) |
| `record/` | Frozen evidence: `finding-`, `freeze-`, `amendment-`, `lesson-` files. Append-only; corrections are new dated files with `supersedes:`. | record workflow, gated by hook |
| `issues/` | Known defects in what already ships: one living file each, status and workaround edited in place. Unresolved ones surface in MAP. | `new_issue.py` (structure) + open/close/route workflows |
| `skills/` | Portable project knowhow, tracked in git at the project root so it travels with the clone. Living documents; nothing loads them automatically, so MAP's table is the index. | `new_skill.py` (structure) + the close-time skills scan |
| `work/` | Work units: **slices** (build work — change the system) and **campaigns** (evidence work — measure it against reality). A **version is not a file** — it exists as the `version:` field on its slices (`vX.Y` convention), a MAP milestone row, and LEDGER entries. | `new_unit.py` (structure) + open/close workflows (slots) |

**Slice vs campaign** — the litmus test: *could this work "fail" and still be
a success?* A campaign, yes (a clean miss is publishable knowledge; inputs
freeze at start). A slice, no (acceptance checks known in advance must pass;
artefacts freeze at the end). Never build inside a campaign — that is tuning
the instrument mid-measurement.

## Workflows (read the one you need)

- **Set up a project** — run `/vouse-project:init` and follow it. It is the
  one-time entry point and it handles both cases: a fresh directory, and a
  repository that already has work (which additionally runs the adoption pass,
  `references/adopt.md`). Invoked directly rather than through this skill,
  it seeds, adopts, fills, and proves in one pass.
  To do it by hand instead:
  `python "${CLAUDE_PLUGIN_ROOT}/skills/vouse-project/scripts/init.py" <root> --name "X"`
  (structure, scripts, hooks, git — all installed by script), then fill the
  MAP / LEDGER / CLAUDE.md slots and prove it:
  `python scripts/check_fill.py MAP.md LEDGER.md CLAUDE.md`. `skills/` and
  `issues/` are seeded empty on purpose — they fill as the work produces
  them, not before. Then open the first unit (below).
- **Adopt a repository that already has work** — `references/adopt.md`: survey
  what exists, propose the LAW rows, issues, and skills the project already has
  but has not written down, and write only what the owner confirms.
- **Cold start** — read `MAP.md`, then the top two `LEDGER.md` entries. Stop.
  Everything else is pull-on-demand. `CLAUDE.md` is already loaded.
- **Open** a version or campaign → `references/open.md`
- **Close** one → `references/close.md`
- **Route** a change request → `references/route.md`
- **Record** a finding / freeze / amendment / lesson → `references/record.md`
- **Capture knowhow** as a project skill, or update one → `references/skills.md`
- **File or reconcile** a known bug → `references/issues.md`
- Why this design, and the production failures it answers → `references/rationale.md`

## Scripts and hooks (the deterministic layer)

After init, everything runs from the project root. Scripts assert facts and
generate structure; they never encode taste or write semantics.

| Tool | Does |
|---|---|
| `/vouse-project:init [dir]` | The one-time setup command: runs the seed with a resolved plugin path, runs the adoption pass on a repository that already has work, fills the slots with the owner, proves it, and hands off. Refuses on an already-seeded root. |
| `scripts/init.py <root> [--name]` | One-shot seed: artefacts from templates (MAP / LEDGER / LAW / CLAUDE.md), `work/` `record/` `issues/` `skills/`, scripts + templates installed, guard hook wired into `.claude/settings.json`, `git init` + post-commit MAP regeneration. Refuses on an already-seeded root; leaves an existing CLAUDE.md untouched and says so. |
| `scripts/new_unit.py --type slice\|campaign …` | Generates the unit file (and, for campaigns, the freeze-note skeleton) with frontmatter/ids/dates done and `<FILL:>` slots for the LLM. Refuses to overwrite. |
| `scripts/new_skill.py --slug <slug>` | Generates `skills/<slug>/SKILL.md` with frontmatter done and slots for the LLM. Refuses to overwrite — a wrong skill is edited, not regenerated. |
| `scripts/new_issue.py --slug <slug> --severity …` | Generates `issues/issue-<date>-<slug>.md`. Refuses to overwrite. |
| `scripts/check_issue.py <file…>` | Validates an issue: naming, status/severity enums, `fixed_by` on fixed/mitigated, `duplicate_of` target exists. |
| `scripts/check_fill.py <paths>` | Proves the semantic half: lists every remaining `<FILL:>` slot; exit 1 if any. |
| `scripts/check_work.py <file…>` | Validates a work unit's frontmatter (type, status enum, required fields, freeze existence) **and refuses a slice at `done` or a campaign at `closed` while any `<LATER:>` slot remains** — which is what makes the close-time skills scan mandatory rather than requested. |
| `scripts/check_record.py <file…>` | Validates a record file: naming, `supersedes:` target exists. |
| `scripts/regen_map.py .` | Rebuilds MAP's three generated tables — state from `work/`, unresolved issues from `issues/`, the skill index from `skills/*/SKILL.md`. Runs from the post-commit hook; run manually after any status change, new issue, or new skill. |
| `hooks/guard_record.py` | PreToolUse hook: blocks edits to existing `record/` files (new files pass). Installed by init. |

**Nothing is claimed that isn't wired.** If a gate in this file is not
installed in the project's settings, install it or strike the claim.

## Red flags — stop and re-read the relevant reference

- Typing frontmatter, ids, dates, or file skeletons by hand — `new_unit.py` / `init.py` own structure; you own slots
- Declaring seeding or a unit "done" without a clean `check_fill` run
- Writing prose into a state table, or hand-editing a generated block
- Editing a file under `record/` ("just fixing a typo" included)
- A campaign whose configuration changed after its first result was read
- A close that skips the LEDGER entry ("the chat has it")
- Seeding a repository that already has work and leaving `LAW.md`, `issues/`, and `skills/` empty — the decisions and defects existed before the structure did (`references/adopt.md`)
- Writing an adopted LAW row, issue, or skill the owner has not confirmed
- A board, changelog, or index that a human no longer trusts — regenerate or delete it, never leave it lying
- Closing a slice, version, or campaign without posing the skills scan to the owner — `check_work.py` will refuse the status flip, and the refusal is the point
- Answering the skills scan yourself, or answering it "no" without naming what was considered
- Explaining the same project-specific procedure a third time instead of writing a skill
- A skill that exists but is absent from MAP's table — nothing loads `skills/` automatically, so unlisted is unfindable
- Editing a `skills/` file as if it were frozen, or a `record/` file as if it were living — the first is a required edit, the second is blocked by a hook
- A defect that lives in chat, a commit message, or a code comment instead of `issues/`
- An issue marked `fixed` with no unit id that fixed it
