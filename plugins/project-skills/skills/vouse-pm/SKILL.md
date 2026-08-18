---
name: vouse-pm
description: >-
  Retrieve from, or capture into, the local PM-continuity tree (project
  status, timelines, correspondence, meeting minutes, schedules, weekly
  plans, handoffs, stakeholder/client context). Use whenever the user wants to (a) RECALL project state — "what's
  the status of X", "where are we on X", "pull up the timeline / meeting notes
  for X", "what did the client say", "what's this week's plan" — or (b) CAPTURE
  PM continuity — "log this to the project", "update status on X", "capture
  these meeting minutes", "note this handoff", "add to the weekly plan".
  Trigger on a bare project name or client codename matching a folder in the
  PM tree, and on "the project tracker / my project notes". Operates on the
  PM tree ONLY; never touches research or knowledge folders, a project's
  source repository, or any dotfolder. PM companion to the `vouse-vault`
  (knowledge) skill.
---

# Vouse PM — Project Continuity Retrieve & Capture

This skill is the bridge to the user's **local PM tree**, their
project-management continuity layer. It operates on **that tree only**. It
never touches research or knowledge folders (that is the `vouse-vault` skill's
zone), a project's source repository, or any dotfolder.

The organising principle: **`Status Notes.md` is the index.** Each project
folder carries a `Status Notes.md` whose dated running log is the front door —
current priority, work focus, confirmed inputs, blockers, and a chronological
trail. You retrieve **status-first** (read Status Notes, then drill), and you
capture **status-first** (write the artifact *and* append a dated line to
Status Notes in the same change). A development that never reaches Status Notes
is effectively invisible to the next consult — keeping that log current is the
whole contract.

**Scope boundary (hard).** PM continuity only: timelines, correspondence,
meeting minutes, schedules, weekly plans, handoffs, stakeholder/client context,
planning history, and the planning-context research/decision notes that inform
them. **Authoritative technical truth stays repo-local** — architecture,
implementation notes, source state, code-facing Kanban/handoffs, build context,
and technical pitfalls live in each project's repo, not here.

## Step 0 — Locate the PM tree (resolve once, then remember)

This skill hardcodes no path. Different people run it on different machines,
so resolve the PM root in this order and stop at the first hit:

1. A `pm_root:` line in the project's `CLAUDE.md`, or in the user's
   `~/.claude/CLAUDE.md`.
2. A `PM/` directory at the root of the current repository, or one level above
   it.
3. Ask the user once — "where does your PM tree live?" — and offer to record
   the answer as a `pm_root:` line in `~/.claude/CLAUDE.md`, so the question is
   asked once per machine rather than once per session.

Everything is local. Use normal file tools (ripgrep / glob / read / write /
edit). There is no remote or connector mode, which is what makes the Status
Notes append below always possible, and therefore always mandatory.

**Canonical-location guard (hard).** The resolved PM root is the only writable
target. If a path resolves outside it — a project's source repository, a
research folder, a knowledge base — **stop**. Never create or edit files
outside the PM tree.

## Step 1 — Decide the mode

From the user's verb: **recall / status / where are we / pull up / what did** →
RETRIEVE. **log / update / capture / record / note / add** → CAPTURE. If
genuinely ambiguous, ask one short question; otherwise proceed.

---

## RETRIEVE (recall project state)

Read **status-first**, drill only as needed, synthesise with citations.

1. **Read the index** — the PM root's `README.md` lists the live projects and
   the per-project folder shape. (Cross-project "this week / this sprint"
   questions go to `Weekly Plans/` — ISO-week files like `2026-W24.md`.)
2. **Pick the matching project folder.** Honour any **sensitivity flag** on a
   note or folder (see Hard rules) — do not echo commercially sensitive client
   or contract detail outside the vault without flagging it.
3. **Read that project's `Status Notes.md` first.** It is the continuity anchor:
   current priority, work focus, delivery target/posture, confirmed inputs,
   blockers/open questions, and a dated running log that summarises everything
   else. Most questions are answered here.
4. **Drill only into the notes the query needs** — `Timeline.md`, `Schedule.md`,
   `Correspondence.md`, `Meeting Notes - <date>.md`, handoff/decision/research
   notes — read those bodies.
5. **Synthesise** in your own words. **Cite every claim** back to the specific
   note by PM-relative path (e.g. `<pm_root>/Acme Cargo Dashboard/Status Notes.md`).
   When reproducing exact dates, figures, names, or commitments, copy them
   precisely — these notes exist because reconstructing client commitments from
   memory is risky.
6. **If nothing matches:** say so plainly, name the project(s)/notes you
   actually checked, and offer to capture a new note or open a new project
   folder.

End a retrieval with a short **Sources** list of the note paths you used.

---

## CAPTURE (record PM continuity)

1. **Classify the artifact** (drives filename, frontmatter `type:`, and routing):
   - **status update** → append to / refresh `Status Notes.md`
     (`type: project_status_notes`).
   - **timeline / milestone change** → `Timeline.md` (`type: project_timeline`).
   - **schedule / calendar** → `Schedule.md`.
   - **meeting minutes** → `Meeting Notes - <YYYY-MM-DD> <label>.md`.
   - **correspondence** (client/stakeholder exchange) → `Correspondence.md`.
   - **handoff / dispatch** → `<Person> Handoff - <YYYY-MM-DD>.md`.
   - **planning-context decision or research** → a dated kebab-case note
     (e.g. `timeline-decision-2026-06-16.md`).
   - **weekly plan** → `Weekly Plans/<YYYY-Www>.md`.
   If the material is authoritative technical truth (architecture, spec, source
   state, code-facing Kanban, build notes), it does **not** belong in the PM
   tree — say so and point to the owning repository. See `references/pm-note-schema.md` for the
   exact frontmatter and body template per artifact.
2. **Route to the project folder.** Check the PM root's `README.md` and reuse an existing
   project folder if one fits. Open a new project folder only when none does
   (see `references/pm-contracts.md` for the new-project procedure).
3. **Dedup check.** For status/timeline/schedule/correspondence, the project
   already has a canonical single file — **append/update it**, do not create a
   parallel `Status Notes 2.md`. Only dated artifacts (meetings, handoffs,
   decisions) are new files each time.
4. **Write the note** with conforming frontmatter and body (see
   `references/pm-note-schema.md`). Refresh the file's `updated:` date.
5. **Append to Status Notes in the same change (MANDATORY).** Add a dated bullet
   to the project's `Status Notes.md` running log summarising what happened and
   pointing to any new file. This is the PM analogue of the catalogue contract:
   the artifact and its Status Notes line ship together, always.
6. **Confirm** what you wrote and where: the note path and the Status Notes line
   you added.

---

## Hard rules

- **PM-only.** Never create or edit anything outside the resolved PM root — not
  in a knowledge or research folder, not in a project's source repository, and
  not in `.claude/` or any other dotfolder.
- **Status Notes contract is mandatory** on every capture — the artifact and its
  dated Status Notes line ship together.
- **PM/technical boundary.** No authoritative specs, architecture, source state,
  code-facing Kanban, or build notes — those stay repo-local. Planning-context
  research and decision notes are fine; authoritative implementation truth is
  not.
- **Commercial sensitivity (soft flag).** PM notes carry client names,
  stakeholder identities, pricing, and scope/contract terms. When surfacing
  these outside the vault, flag them as commercially sensitive rather than
  echoing freely; never paste contract figures into an external destination
  without the user's explicit say-so.
- **Follow the CURRENT schema.** New notes always carry full frontmatter
  (`schema_version: 1`) and live in a project folder or `Weekly Plans/`.

## Reference files

- `references/pm-note-schema.md` — exact frontmatter per `type:`, the tag
  taxonomy, date fields, and body templates per artifact. Read before writing
  any note.
- `references/pm-contracts.md` — the Status-Notes-as-index contract, per-project
  folder shape, Weekly Plans naming, the new-project and archive procedures, and
  routing/dedup rules. Read before any capture.
