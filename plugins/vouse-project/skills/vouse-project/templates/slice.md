---
id: {{ID}}
type: slice
kind: {{KIND}}
status: draft
opened: {{DATE}}
version: {{VERSION}}
---

# Slice — <FILL: name>

**Builds:** <FILL: what the system can do after this that it cannot today, one paragraph.>

## Acceptance checks

Each check carries all five fields or the slice is not ready to build.
Evidence artefact = a file path, or "Verification section transcript".

| # | Setup | Action | Observable signal | Expected value | Evidence artefact |
|---|---|---|---|---|---|
| 1 | <FILL> | <FILL> | <FILL> | <FILL> | <FILL> |

## Implementation record

<LATER: filled at build time — what was done, decisions, deviations, dated notes.>

## Verification

<LATER: filled at verify time — each check run, what was actually observed,
chronological. A slice without this section verified cannot be done.>

## Skills scan (mandatory before this slice is done)

<LATER: filled when the slice is closed. Pose to the owner, in these words:
"This slice taught us X, Y, Z. Should any of it become a project skill in
`skills/`, or update an existing one?" Record their answer here — the skill
slug created or edited, or their explicit "nothing portable here" and why.
An unfilled slot means the scan did not happen, and `check_fill --all`
fails the close.>
