# Route — triage a change request

Every ask to add, change, or remove something lands in exactly one of three
tiers. Decide by mechanical trigger, not persuasion.

## The three tiers

| Tier | Trigger | Action |
|---|---|---|
| **1 · Edit in-flight work** | The change fits a unit that is open and not yet frozen | Edit the unit, note the revision inside it, re-verify |
| **2 · New work** | The change needs a unit of its own — a new slice in the open version, a new campaign, or a patch to something shipped | Open it (`references/open.md`); patches are `kind: patch` slices citing what they fix — shipped artefacts are never edited |
| **3 · Law change** | The change touches a `LAW.md` row, a frozen `record/` entry's meaning, a public interface, or the canon | Requires an owner decision and lands at a close: route into the closing of the current unit, or open a unit whose explicit goal is the law change |

## Two asks that route sideways, not into a tier

Some asks are not changes to the system at all. Routing them into a tier
manufactures ceremony and teaches people to stop routing.

| The ask | Goes to | Not |
|---|---|---|
| "This is broken and nobody is fixing it today" | an `issues/` file (`references/issues.md`) | a slice; filing is not scheduling |
| "Write down how this is done here" | a `skills/` entry (`references/skills.md`) | a LAW row; a procedure is not a decision |

Fixing a filed issue does route as tier 2: a `kind: patch` slice whose
`patches:` field names the issue id. Editing an existing skill routes as
tier 1 — a one-line note, no ceremony. Creating a skill is the owner's call
and is normally posed at a close, not mid-flight.

## Hard triggers for tier 3 (no judgment needed)

- Any edit to what a LAW row asserts, or to "enforced by"
- Changing the canonical configuration or a standing measurement definition
- Anything that would make an existing frozen record retroactively wrong —
  which is impossible; the record gets a superseding entry instead
- A discovery from below ("this invariant cannot hold as written") routes
  the same as a request from above

## Two rules that make routing honest

1. **Factual corrections are still routed, but cheaply.** A wrong path or a
   stale name in a living document (MAP, LAW, references) is a tier-1 edit
   with a one-line note — do not manufacture ceremony for corrections, and
   do not let ceremony's cost teach people to skip routing. If the same
   living document needs "owner-authorized exceptions" repeatedly, the
   document is priced wrong: move the volatile part out of it.
2. **Work that happened outside any unit gets a unit retroactively at the
   next close — once.** The second time work bypasses the structure, the
   structure is wrong: add the missing unit kind instead of retrofitting
   forever (this is how campaigns became first-class).
