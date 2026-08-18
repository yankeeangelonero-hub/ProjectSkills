---
name: bob-write
description: "Write in \"bob\" — a flat, declarative engineering-specification register. Use this skill whenever the user asks to write, draft, rewrite, or edit ANY prose in bob style, spec style, or specification register — specs, feature proposals, requirements docs, design docs, README sections, tickets, emails, replies, summaries. Trigger on any mention of \"bob\", \"bob-write\", \"spec register\", \"spec style\", \"write it like a spec\", or when the user asks for writing that is plain, exact, and free of marketing language. When the user asks to draft a functional or technical specification of any kind, use this skill even if they never say \"bob\"."
---

# bob-write: the specification register

Produce prose in the register of a good engineering specification: flat, declarative,
condition-first, and exact. The register is modelled on a real functional spec the user
wrote; the goal is text where every sentence states a fact or a behaviour and nothing
performs, persuades, or decorates.

The reason this register works: a spec is read by someone deciding what to build or
verifying what was built. Every adjective they must discount, every synonym they must
reconcile, and every restated summary they must skip is friction. Remove the friction
and the document becomes checkable line by line.

## Voice and tense

Use third person with concrete role-based subjects — the user, the application, the
system, the host. Never "I think", "we believe", or direct address, except in
step-by-step instructions where "you" is unavoidable.

State defined behaviour in the simple present: "Polling begins as soon as the map
application is opened." Reserve "will" for planned or future behaviour: "The host will
display a native dialog." This tense split carries information — present = exists or is
being specified as fact; "will" = intended, not yet fixed.

Passive voice is acceptable, and often preferable, when the agent is obvious or
irrelevant: "A pin is placed at the centre of the current map view."

## Structure

Open each section with a short noun-phrase header: "Entering pinning mode",
"Confirmation handoff", "Dialog visibility toggle". Headers name the thing, not the
argument about the thing.

One idea per sentence. Short-to-medium sentences. Do not stack subordinate clauses.

Put the condition before the consequence: "If location is not accessible, a warning
dialog is displayed." Condition-first lets a reader scan the left edge of the text for
the case they care about.

Specify the negative or failure case immediately after the positive one, never in a
separate section the reader must find. If the happy path gets a sentence, its failure
path gets the next sentence.

When describing capabilities, state exclusions explicitly, in the source register's own
form:

```
The user will be able to:
Drag the pin. ...
Drag the map. ...

The user will not be able to:
Place more than one pin simultaneously.
Persist the pin between pinning sessions.
```

An explicit "will not" list is scope control; anything unlisted is ambiguous, and
ambiguity is where implementations diverge.

## Precision

Choose one term per concept and reuse it verbatim everywhere — pin, pinning mode,
polling tick, native dialog. Never vary wording for elegance; a synonym reads as a new
concept.

Unpack categories exhaustively in parentheses at the point of use: "(permission denied,
location services disabled, or not supported by the device)". The parenthetical is the
definition; the reader never has to guess what the category covers.

Give concrete values instead of qualifiers: "fixed at 30 seconds", never "a short
interval". If the value is not yet decided, say so as fact: "The interval is not yet
determined."

Mark provisional behaviour explicitly: "exists as a placeholder for a future
capability", "can be adapted in later iterations". Provisional text that is not marked
provisional will be built as final.

## Prohibitions

No marketing or evaluative adjectives (powerful, seamless, robust, intuitive). No hype.
No hedging filler (arguably, perhaps it might be worth considering). No rhetorical
questions. No exclamation marks. No emoji. No bold-for-emphasis. No closing summaries
that restate the content. No reassurance about how the reader might feel.

## Scope of application

Apply the register to the whole deliverable, including titles, captions, list items,
and any accompanying explanation the user asked for. When the user asks for
conversational replies in this register, answer in it: short declarative sentences,
condition-first logic, exact terms, nothing decorative.

## Reference files

Two reference files carry the vocabulary layer this register depends on. They are drawn
from ASD-STE100 Simplified Technical English, which shares bob's core commitment: one
word per concept, no hedging, condition before consequence.

- `references/word-substitutions.md` — unapproved-to-approved word mappings, one-meaning
  rulings, and the frequent-offender function words. Read it before drafting. It is
  short, and it is the fastest way to catch the Latinate padding (utilize, commence,
  facilitate, prior to) that makes prose sound like it is selling something.
- `references/examples.md` — worked before/after rewrites covering verb forms, phrasing,
  noun clusters, and a common-mistakes checklist. Read it when rewriting existing text or
  when the application of a rule is unclear.

Where the references disagree with this skill, this skill wins. STE is written for
maintenance procedures, so it mandates the imperative and active voice; bob is written
for specifications and uses third-person declarative sentences, with passive voice where
the agent is obvious or irrelevant. Take the vocabulary, the one-meaning discipline, and
the anti-hedging rules from the references. Ignore their imperative-voice instructions
and their WARNING/CAUTION/NOTE conventions, which belong to manuals rather than specs.

## Example

Input: "write something about how our new export button lets users get their data out
whenever they want, it's super flexible"

Output:

```
Data export

An Export button is added to the report toolbar. When the user presses it, the
application generates a file containing the current report data and offers it for
download.

The user selects one of two formats (CSV or XLSX) from a dialog displayed when the
button is pressed. If report data is still loading at the moment the button is pressed,
the button is disabled and a tooltip reading "Report is loading" is shown.

The export reflects the filters active at the time the button is pressed. Filters
applied after the file is generated do not affect the downloaded file.
```
