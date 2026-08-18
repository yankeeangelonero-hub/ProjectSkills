# PM Note Schema

Every PM note is **frontmatter-first**: a YAML block, then `# Title`, then body.
Dates are ISO `YYYY-MM-DD`. `project:` is the human project name (quoted when it
contains a colon). The schema below is the **current** convention, drawn from
live notes in the `PM/` tree.

## Shared fields (all PM notes)

```yaml
type: <project_status_notes|project_timeline|project_meeting_notes|project_correspondence|project_handoff|project_decision|project_schedule|project_weekly_plan|project_management_index>
schema_version: 1
status: <active|draft|archived>
project: "Acme: Cargo Dashboard"
updated: 2026-06-29
tags: [memory/projects, <project-slug>, <facet>]
```

- `<project-slug>` is the kebab-cased project name (e.g. `acme-cargo-dashboard`).
- `<facet>` tags mirror the artifact: `status`, `timeline`, `meeting`,
  `correspondence`, `handoff`, `decision`, `schedule`, `weekly-plan`.
- Keep tags lowercase, slash-namespaced where hierarchical, and minimal — mirror
  sibling notes in the same project rather than inventing new namespaces.
- `Weekly Plans/` notes use `project:` omitted or `project: "(cross-project)"`.

---

## type: project_status_notes  (the continuity anchor)

One per project. The most important file. Its body is a set of standing
sections plus a dated running log.

```yaml
---
type: project_status_notes
schema_version: 1
status: active
project: "Acme: Cargo Dashboard"
updated: 2026-06-29
tags: [memory/projects, acme-cargo-dashboard, status, timeline]
---

# Acme: Cargo Dashboard — Status Notes

## Current priority
<one short paragraph: what matters most right now>

## Current work focus
- <bullet>
- <bullet, with dated log entries interleaved, newest context near top>
- 2026-06-29: <dated event — what happened, what it implies>

## Delivery target
- <milestone / window / target date lines>

## Delivery posture
- <scope boundaries, what is in/out, what must ship next>

## Confirmed inputs
- 2026-06-12: <confirmed fact, source>

## Blockers / open questions
- <open item to resolve, with owner if known>

## PM notes
This file captures project-management status only. Authoritative technical
detail lives in the project repo.
```

The dated bullets under **Current work focus** are the running log — every
capture appends one. Newest entries are added in date order within the section.

## type: project_timeline

```yaml
---
type: project_timeline
schema_version: 1
status: draft
project: "Acme: Cargo Dashboard"
updated: 2026-06-29
tags: [memory/projects, acme-cargo-dashboard, timeline]
---

# <Project> — Timeline

## Confirmed timeline need
- <why a timeline is needed, what the client expects>

## Immediate milestone

| Milestone | Target | Notes |
|---|---|---|
| <name> | 2026-07-13 tentative | <what's expected> |

## <assumptions / implications sections as needed>
```

## type: project_meeting_notes

Filename `Meeting Notes - <YYYY-MM-DD> <label>.md` (e.g.
`Meeting Notes - 2026-06-29 Kickoff.md`).

```yaml
---
type: project_meeting_notes
schema_version: 1
status: active
project: "Acme: Cargo Dashboard"
updated: 2026-06-29
tags: [memory/projects, acme-cargo-dashboard, meeting]
---

# <Project> — <Label> Meeting, 2026-06-29

- **Attendees:** <names/roles>
- **Decisions:** <what was agreed>
- **Client requests:** <what they asked for>
- **Action items:** <owner → task → due>
- **Next meeting:** <date / expected materials>
```

## type: project_correspondence

One `Correspondence.md` per project — a dated log of client/stakeholder
exchanges. Append entries; do not split into many files.

```yaml
---
type: project_correspondence
schema_version: 1
status: active
project: "Acme: Cargo Dashboard"
updated: 2026-06-29
tags: [memory/projects, acme-cargo-dashboard, correspondence]
---

# <Project> — Correspondence

- 2026-06-29: <who ↔ who, channel, substance, any commitment made>
```

## type: project_handoff

Filename `<Person> Handoff - <YYYY-MM-DD>.md` (e.g.
`Alex Handoff - 2026-06-29.md`).

```yaml
---
type: project_handoff
schema_version: 1
status: active
project: "Acme: Cargo Dashboard"
updated: 2026-06-29
tags: [memory/projects, acme-cargo-dashboard, handoff]
---

# <Project> — Handoff to <Person>, 2026-06-29

- **Context they need:** ...
- **Current state:** ...
- **Open items / watch-outs:** ...
- **Pointers:** <links to Status Notes, repo, relevant notes>
```

## type: project_decision  /  planning-context research

A dated kebab-case note capturing a planning decision or research that informs
PM (not authoritative technical truth). Filename like
`timeline-decision-2026-06-16.md`, `base-vs-expanded-scope-definition-2026-06-16.md`.

```yaml
---
type: project_decision
schema_version: 1
status: active
project: "Globex: Route Planner"
updated: 2026-06-16
tags: [memory/projects, globex-route-planner, decision]
---

# <Decision / topic title>

> <one-line summary of the decision or finding, and the date>

<body — options considered, what was chosen, why, implications>
```

## type: project_weekly_plan

Filename `Weekly Plans/<YYYY-Www>.md` (ISO week, e.g. `2026-W24.md`).

```yaml
---
type: project_weekly_plan
schema_version: 1
status: active
updated: 2026-06-12
tags: [memory/projects, weekly-plan]
---

# Week 2026-W24

## Focus
- <cross-project priorities for the week>

## Per project
- **<Project>:** <what to push this week>
```

## type: project_management_index  (the PM root's README.md)

The `the PM root's README.md` is itself a `project_management_index` note — the front door
listing live projects and the folder shape. See `pm-contracts.md` for the body.

```yaml
---
type: project_management_index
schema_version: 1
status: active
tags: [memory/projects, project-management]
---
```
