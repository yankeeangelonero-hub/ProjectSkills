---
name: vouse-pm
description: >-
  Retrieve from, or capture into, the PM-continuity layer of the user's
  REDACTED — the `PM/` tree (project status, timelines, correspondence,
  meeting minutes, schedules, weekly plans, handoffs, stakeholder/client
  context). Use whenever the user wants to (a) RECALL project state — "what's
  the status of X", "where are we on X", "pull up the timeline / meeting notes
  for X", "what did the client say", "what's this week's plan" — or (b) CAPTURE
  PM continuity — "log this to the project", "update status on X", "capture
  these meeting minutes", "note this handoff", "add to the weekly plan". Trigger
  even on a bare project name (REDACTED, REDACTED, REDACTED, REDACTED, REDACTED, Airport
  Real Estate, REDACTED) or "the project tracker / PM vault / my project
  notes". Operates on `PM/` ONLY; never touches `Knowledge/`, the retired
  `Projects/` tombstone, or any dotfolder. PM companion to the `vouse-vault`
  (Knowledge) skill.
---

# Vouse PM — Project Continuity Retrieve & Capture

This skill is the bridge to **`REDACTED/PM/`**, the user's project-management
continuity layer. It operates on **one zone only — `PM/`**. It never touches
`Knowledge/` (that's the `vouse-vault` skill's zone), the retired
`Projects/` tombstone, `_System/`, or any dotfolder.

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

## Step 0 — Locate the vault (environment detection)

**Primary path — local filesystem (preferred).** In Claude Code on the user's
machine the vault is at `REDACTED-PATH\`, so the PM zone is
`REDACTED-PATH\PM\`. If that path exists, use normal file tools
(ripgrep / glob / read / write / edit). This is preferred for both retrieve and
capture — fast, and it supports in-place Status Notes appends.

**Fallback path — Google Drive connector.** If the local path is unavailable
(e.g. running in Claude.ai), use the Google Drive tools. The REDACTED root
folder id is `REDACTED-FOLDER-ID`; the `PM/` folder id is
`REDACTED-FOLDER-ID` (verify by `search_files` on
`parentId = '<parent>'` rather than trusting a stale id). In Drive mode you can
**read everything** and **create new files / copy**, but the connector
**cannot edit or append to existing files** — so the mandatory Status Notes
append is unreliable there. **Prefer Claude Code for capture.** If you must
capture in Drive mode, create the new note, then explicitly tell the user the
project's `Status Notes.md` still needs a follow-up append from a local session.

**Canonical-location guard (hard).** `PM/` is the only canonical, writable
target. If a path ever resolves to `REDACTED/Projects/` (a retired tombstone)
or to the legacy `Memory System/Projects/` tree, **stop** — those are not
canonical. Never create or edit files outside `PM/`.

## Step 1 — Decide the mode

From the user's verb: **recall / status / where are we / pull up / what did** →
RETRIEVE. **log / update / capture / record / note / add** → CAPTURE. If
genuinely ambiguous, ask one short question; otherwise proceed.

---

## RETRIEVE (recall project state)

Read **status-first**, drill only as needed, synthesise with citations.

1. **Read the index** — `PM/README.md` lists the live projects and the
   per-project folder shape. (Cross-project "this week / this sprint" questions
   go to `PM/Weekly Plans/` — ISO-week files like `2026-W24.md`.)
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
   note by PM-relative path (e.g. `PM/Acme Cargo Dashboard/Status Notes.md`).
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
   - **weekly plan** → `PM/Weekly Plans/<YYYY-Www>.md`.
   If the material is authoritative technical truth (architecture, spec, source
   state, code-facing Kanban, build notes), it does **not** belong in `PM/` —
   say so and point to the repo. See `references/pm-note-schema.md` for the
   exact frontmatter and body template per artifact.
2. **Route to the project folder.** Check `PM/README.md` and reuse an existing
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
   the artifact and its Status Notes line ship together, always. (Drive-mode
   caveat: if you cannot append in place, flag it — see Step 0.)
6. **Confirm** what you wrote and where: the note path and the Status Notes line
   you added.

---

## Hard rules

- **PM-only.** Never create or edit anything under `Knowledge/`, the retired
  `Projects/` tombstone, the legacy `Memory System/Projects/` tree, `_System/`,
  `.obsidian/`, `.claude/`, or any other dotfolder.
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
- **Drive-mode write limit.** In Drive fallback you may read, create, and copy,
  but cannot edit/append existing files — so prefer Claude Code for capture, and
  if you capture in Drive mode, flag that `Status Notes.md` still needs a local
  append.

## Reference files

- `references/pm-note-schema.md` — exact frontmatter per `type:`, the tag
  taxonomy, date fields, and body templates per artifact. Read before writing
  any note.
- `references/pm-contracts.md` — the Status-Notes-as-index contract, per-project
  folder shape, Weekly Plans naming, the new-project and archive procedures, and
  routing/dedup rules. Read before any capture.
