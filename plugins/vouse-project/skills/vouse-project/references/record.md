# Record — write frozen evidence and the ledger

`record/` is append-only history. The guard hook blocks edits to existing
files; this reference is about writing them right the first time.

## The four record kinds

| Prefix | When | Template |
|---|---|---|
| `freeze-` | BEFORE a campaign reads any outcome: pins every input | `templates/freeze-note.md` |
| `finding-` | A result worth keeping: what was measured, what it showed, residuals | `templates/finding.md` |
| `amendment-` | A definition or methodology change, dated, with scope stated | (finding template, scope section mandatory) |
| `lesson-` | An expensive mistake converted into a standing protection | (finding template, "the rule" section mandatory) |

A `lesson-` is not a skill. The lesson is the frozen, dated account of one
expensive mistake and the standing protection it bought; it never changes. The
skill is the living procedure someone follows tomorrow so the mistake does not
recur. An expensive mistake usually produces both, and they cite each other:
the lesson names the skill slug, the skill's Provenance section names the
lesson file. See `references/skills.md`.

Filenames: `<kind>-YYYY-MM-DD-<slug>.md`. Validate before commit:
`python scripts/check_record.py record/<file>.md`.

## Freeze notes — the integrity core

A freeze pins ALL of: configuration files (id + sha256 via
`scripts/pin_inputs.py`), engine/tool versions, seeds, source-data files,
**and every derivation lineage between source and input** — how records were
assigned, filtered, classed, remapped. Lineage omissions are first-order:
an unpinned assignment rule can move headline results by large margins while
every pinned hash stays green. If the exercise is one-shot, the freeze says
so; after outcomes are read, a corrected attempt is a NEW freeze, and the
missed one's finding stands.

## Supersession, not correction

Wrong or outdated record? Write a new dated file with `supersedes:
<old-filename>` in frontmatter (checked by `check_record.py`). The old file
stays. Readers of the old file deserve to find the new one — add a pointer
line to MAP or the finding index if one exists, never into the old file.

## Findings — write for the cold reader

State what was run (cite the freeze), what the numbers were (matched grain:
median↔median, same interval definitions, anchors named), what it means, and
the residuals as a plain list. Every claim a report or slide will later make
should be traceable to a sentence here. The register is bob (REQUIRED
SUB-SKILL: `bob-write`): flat declaratives, condition before consequence,
one term per concept, no hedging, no marketing, no narrative of how you
found it — discovery narrative goes in LEDGER prose if anywhere.

## The LEDGER entry

Every record-worthy event gets one dated LEDGER paragraph linking the record
files. LEDGER is the story; `record/` is the evidence; MAP is the pointer.
One fact, one home: the LEDGER cites numbers, it does not re-derive them.
