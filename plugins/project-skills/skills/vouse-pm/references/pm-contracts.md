# PM Contracts

How project continuity is found and kept current. **A development that never
reaches a project's `Status Notes.md` is invisible to the next consult.** Every
capture updates Status Notes in the same change.

## The hierarchy

```
the PM tree
├── README.md                 # type: project_management_index — the front door
├── Weekly Plans/             # cross-project, ISO-week files (YYYY-Www.md)
│   └── 2026-W24.md
├── archive/                  # retired/duplicate project folders
└── <Project Name>/
    ├── Status Notes.md       # the continuity anchor  ← front door per project
    ├── Timeline.md
    ├── Schedule.md
    ├── Correspondence.md
    ├── Meeting Notes - <date> <label>.md
    ├── <Person> Handoff - <date>.md
    └── <topic>-decision-<date>.md   # planning-context decisions / research
```

A consult reads top-down: `README.md` → project `Status Notes.md` → the specific
note the question needs.

## The Status-Notes-as-index contract

Unlike the Knowledge vault (which uses per-discipline `## Files` tables), the PM
zone's index per project **is** `Status Notes.md`. Its dated running log under
**Current work focus** is the catalogue. On every capture:

1. Write the artifact file (per `pm-note-schema.md`).
2. Append a dated bullet to that project's `Status Notes.md` running log —
   what happened, what it implies, and a pointer to any new file by name.
3. Refresh `updated:` on both the artifact and Status Notes.
4. Confirm the artifact path and the Status Notes line you added.

The append is never optional. The tree is local, so an in-place edit is
always available; a capture that skips the Status Notes line is an incomplete
capture, not a deferred one.

## the PM root's README.md — the index body

Frontmatter is `type: project_management_index` (see `pm-note-schema.md`). The
body states scope and lists live projects:

```markdown
# Project Management Notes

The PM-continuity layer of the PM tree. Canonical as of 2026-06-30; supersedes the
retired `Projects/` tombstone and the legacy `Memory System/Projects/` tree.

Use this area for human/project-management continuity: timelines,
correspondence, meeting minutes, schedules, weekly plans, handoffs,
stakeholder/client context, planning history. Do **not** mirror authoritative
technical specs here — technical truth stays repo-local.

## Projects

| Project | Front door | What it is |
|---|---|---|
| **Acme Cargo Dashboard** | [Acme Cargo Dashboard/Status Notes.md](Acme%20Cargo%20Dashboard/Status%20Notes.md) | One-line description. |

## Cross-project

| Area | Location |
|---|---|
| Weekly plans | [Weekly Plans/](Weekly%20Plans) |
```

### Relative-link encoding

Catalogue links are vault-relative and **URL-encode** spaces and parentheses:
space → `%20`, `(` → `%28`, `)` → `%29`. Link text stays human-readable; only
the target is encoded.

## Routing & dedup

- **Single-file artifacts** — `Status Notes.md`, `Timeline.md`, `Schedule.md`,
  `Correspondence.md` — are canonical and unique per project. **Append/update
  them**; never create `Status Notes 2.md` or a parallel timeline.
- **Dated artifacts** — meeting notes, handoffs, decisions — are a new file each
  time, named with their date.
- Before creating any file, check the project folder for an existing file that
  should be appended instead.

## Procedure — adding to an existing project

1. Write or append the artifact in the project folder.
2. Append the dated bullet to that project's `Status Notes.md` running log.
3. If a new dated artifact was created, add it to the README's project row only
   if the README tracks per-file detail (it usually points at Status Notes —
   match what the README already does).
4. Confirm paths and the Status Notes line.

## Procedure — opening a new project

1. Create `PM/<Project Name>/`.
2. Create `Status Notes.md` (frontmatter per schema; the standing sections; an
   opening dated log bullet).
3. Add any first artifacts (Timeline, kickoff meeting notes, etc.).
4. Add a row for the project to `the PM root's README.md` `## Projects`, pointing at the new
   `Status Notes.md`.
5. Confirm all paths and rows.

Do not scaffold empty project folders speculatively — a project folder earns its
place with a real `Status Notes.md`.

## Procedure — archiving a project

1. Move the project folder into `archive/` under the PM root, optionally
   suffixing the reason/date
   (e.g. `… - duplicate archived 2026-06-16`).
2. Set `status: archived` in its `Status Notes.md` frontmatter.
3. Remove or strike its row from `the PM root's README.md` `## Projects`.

## Verify after writing

After a capture, re-read the project's `Status Notes.md` to confirm the dated
line renders, any new-file pointer resolves, and the frontmatter `updated:` date
is current.
