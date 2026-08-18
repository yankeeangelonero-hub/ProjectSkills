# Adopt — seed a repository that already has work

Seeding a fresh directory produces an empty structure and that is correct.
Seeding a repository with months of history and then leaving the structure
empty is not: the project's real decisions, defects, and knowhow stay where
they were, and the new artefacts become a second front door that disagrees with
the first. This reference is the pass that closes that gap.

Run it after `init.py` and before filling the MAP / LEDGER / CLAUDE.md slots.
Everything here is a **proposal** — you survey and draft, the owner confirms.
Nothing lands unconfirmed.

## What you are looking for, and where it goes

| Found in the repository | Goes to | Test |
|---|---|---|
| A rule everyone follows — a CONTRIBUTING line, a lint config with a deliberate exception, a convention enforced in review | `LAW.md` row | Would violating it be treated as a defect? |
| An ADR, a decision log, a "why we chose X" section | `LAW.md` row, evidence link pointing at the existing document | Is it still in force? |
| An issue tracker, a TODO/FIXME with real content, a bug in someone's head | `issues/` | Does it exist in something already shipped or in use? |
| A README setup section people still get wrong, a runbook, a "how to run the thing" wiki page | `skills/` | Would a competent newcomer get it wrong without this? |
| A measurement, benchmark, or audit result the team still cites | `record/finding-…` | Is it a result, cited, not re-derivable from memory? |
| Work in flight right now | a slice in `work/` | Is someone actively building it? |
| Everything else | nowhere | Do not import history for its own sake. |

## The pass

1. **Survey, cheaply.** Read the README, `CONTRIBUTING`, any `docs/` index, the
   issue tracker if one exists, and the last twenty commit subjects. Grep for
   `TODO`, `FIXME`, `HACK`, `XXX`. Do not read the whole codebase — you are
   looking for decisions and defects, not architecture.

2. **Draft the proposals.** For each candidate, write one line: what it is,
   which artefact it belongs in, and the evidence you found it in. Keep the list
   short. Ten confirmed rows beat forty speculative ones, and a long list gets
   approved without being read, which is the same as not being reviewed.

3. **Put the list to the owner.** Group it by artefact. For each item ask the
   question that artefact requires:
   - LAW: "Is this still in force, and what enforces it — a test, a script, a
     hook, or convention?"
   - issues: "Is this still broken? Is there a workaround?"
   - skills: "Is this how it is actually done now?"
   - work: "Is this in flight, and who owns it?"

   Expect deletions. A rule nobody follows any more is not a LAW row, it is a
   correction the owner is now making — and that correction is worth more than
   the row would have been.

4. **Write only what was confirmed.** Use the scripts:
   `new_issue.py`, `new_skill.py`, `new_unit.py`. Every LAW row carries
   decided-when, evidence, and enforced-by — and if "enforced by" is a gate that
   does not exist, the row says `convention` honestly rather than naming a check
   nobody wrote.

5. **Write the history paragraph** for the seed LEDGER entry: what this project
   is, roughly how long it has been running, what state it is in today, and
   what this adoption imported. This is the only place the pre-ledger past is
   recorded. Write it for a cold reader who joins in six months, in the bob
   register.

6. **Regenerate and prove.**
   ```
   python scripts/regen_map.py .
   python scripts/check_fill.py .
   ```

## Dating what predates the ledger

Adopted material is dated by when it was **decided or discovered**, not by
today, when that date is knowable from a commit, a document, or the owner's
memory. Where it is not knowable, use today's date and say in the row or file
that the origin date is unknown. Never invent a date to make a table look tidy —
a wrong date in a LAW row is a false evidence trail.

## Where adoption stops

- **Do not import closed history.** Past releases, resolved bugs, and superseded
  decisions stay in git and the tracker. The artefacts carry what is live.
- **Do not retro-fit work units for finished work.** The LEDGER's seed entry
  summarises the past; `work/` holds what is open now.
- **Do not write a skill for something a script already enforces.** Point at the
  gate.
- **Do not adopt in a repository the owner is not present for.** Every item on
  the list is a question only they can answer; a solo adoption produces a
  confident-looking set of artefacts nobody has agreed to.

## Red flags

- A LAW row whose evidence is "it is obviously right" rather than a document,
  commit, or incident
- An issues list that is a TODO dump — `TODO: refactor this` is not a defect
- A skill written from the README rather than from what actually goes wrong
- An adoption that produces thirty artefacts and no deletions — you proposed,
  the owner rubber-stamped, and nothing was actually decided
- A seed LEDGER entry that reads as project marketing rather than a cold
  handover
