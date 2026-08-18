# Close — finish a version or campaign

A close is the moment owner utterances become durable record. Everything
below either happens at close or silently never happens.

## Closing a single slice

A slice reaching `done` is a close in miniature and carries two of the steps
below in full: the **skills scan** (step 2 — posed to the owner, recorded in
the unit) and **issue reconciliation** (step 3). `check_work.py` refuses
`status: done` while any `<LATER:>` slot remains, so a slice cannot be called
done with its scan unanswered. The rest of the checklist waits for the
version close.

## Preconditions

Every slice in a closing version is `done` or `superseded` — or the owner
explicitly defers it. Deferral is stated, never silent: the unit file, the
LEDGER entry, and MAP all name what moved forward and why (e.g. "blocked on
external clearance"). A campaign closes when its runs are complete and its
finding is frozen — including when the result is a miss; a clean miss closes
a campaign as legitimately as a hit.

## The checklist (all of it, every time)

1. **Reconcile work units.** Walk each unit in the closing scope: done /
   superseded / deferred-with-reason. Update frontmatter; run
   `python scripts/check_work.py` on each touched file, and prove every
   deferred-stage section got written:
   `python scripts/check_fill.py --all work/<unit>.md` (LATER slots must be
   filled by now — a unit closing with a LATER slot skipped its build,
   verify, results, residuals, or skills-scan half). `check_work.py` refuses
   a slice at `done` or a campaign at `closed` while any LATER slot remains,
   so this step cannot be passed by assertion.
2. **Run the skills scan — mandatory, and posed to the owner.** This
   happens at every slice close and again at the version or campaign close.
   It is not optional and it is not answered on the owner's behalf.

   Pose it in these words, with the specifics filled in:

   > "This slice taught us X, Y, Z. Should any of it become a project skill
   > in `skills/`, or update an existing one?"

   Name the candidates concretely — the thing you had to work out, the step
   that surprised you, the correction a reviewer made twice, the command
   sequence nobody would guess. A scan that asks "anything to add?" gets
   "no"; a scan that names three candidates gets a decision.

   Record their answer verbatim in the unit's `## Skills scan` section: the
   slug created or edited, or their explicit "nothing portable here" and the
   reason. A recorded no is a result. An unfilled slot is a skipped step,
   and the script fails the close on it.

   Acting on a yes: `python scripts/new_skill.py --slug <slug>` for a new
   one, a plain edit for an existing one, then `python scripts/regen_map.py .`
   so it reaches MAP's table. Full guidance: `references/skills.md`.

3. **Reconcile known issues.** Every issue the closing scope touched gets
   its status and `fixed_by` set (`python scripts/check_issue.py issues/*.md`),
   every defect discovered during the work gets filed rather than mentioned,
   and anything still open stays visible in MAP's table. A close that leaves
   a discovered defect unfiled has converted a known issue into an unknown
   one. See `references/issues.md`.

4. **Grill permanent decisions.** For each decision made in this unit's
   lifetime, ask the owner: one-off, or standing? Standing decisions land as
   a `LAW.md` row (decided-when / evidence link / enforced-by) — and if
   "enforced by" is a script or hook that does not exist yet, either write it
   now or the row says `convention` honestly. Canon changes (default
   configuration, standing definitions) are LAW rows too.
5. **Freeze the evidence.** Any result the close relies on gets a `record/`
   finding (see `references/record.md`) — the close cites it, never restates
   it.
6. **Write the LEDGER entry.** Dated, prose, cold-readable, in the bob
   register (REQUIRED SUB-SKILL: `bob-write`): what shipped or what was
   learned, what was deferred and why, the owner's approval in their own
   words. This is the one document a human reads later — write it for
   them, not for the process.
7. **Regenerate MAP** (`python scripts/regen_map.py .`, which rebuilds the
   state, issues, and skills tables together) and update its prose
   rows (canon, open work, milestones) by hand — prose is human-written,
   tables are generated, never the reverse.
8. **Flip the unit** to `closed` with a date. It is now frozen; corrections
   route as new work (`references/route.md`), never as edits.

## What this checklist deliberately drops

No board walk (no board — MAP's table is generated), no separate roadmap
graph validation (milestones live as a MAP table + LEDGER history), no
journey audit unless actor-facing behaviour changed in the closing scope
(then it is a slice-level verification concern, cite the test record).

## Red flags

- "The chat has it" — the chat is not a record. LEDGER or it didn't happen.
- A deferral that appears in conversation but not in the unit file.
- A LAW row whose "enforced by" names a gate that isn't installed.
- A skills scan answered by the agent, or answered "no" without naming what
  was considered. The question exists to be refused knowingly.
- A defect discovered during the work that appears in the LEDGER prose but
  never got an `issues/` file.
- Closing a campaign by re-running it because the result missed. One shot
  means one shot; a corrected re-run is a NEW campaign with its own freeze.
