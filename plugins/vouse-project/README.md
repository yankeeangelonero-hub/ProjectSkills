# vouse-project (plugin)

Project lifecycle management on a fixed artefact set: `MAP.md`, `LEDGER.md`,
`LAW.md`, `CLAUDE.md`, `record/`, `work/`, `issues/`, `skills/`. Skills judge;
scripts execute; hooks enforce. State is derived from ground truth or it does not
exist.

Two of those artefacts exist to make knowledge outlive the session and the
person:

- **`skills/`** — portable project knowhow, tracked in git at the project root so
  it arrives with the clone. A **skills scan is posed to the owner at every slice,
  version, and campaign close** — "should any of what this taught us become a
  project skill?" — and `check_work.py` refuses to flip a unit to `done` or
  `closed` while that answer is missing. The mandate is a gate, not a reminder.
- **`issues/`** — a known-defect tracker, one living file per bug, each carrying
  its workaround. Unresolved issues surface in `MAP.md`; filing is explicitly not
  scheduling, so filing stays cheap.

Both are indexed by generated `MAP.md` tables and named as standing rules in the
seeded `CLAUDE.md`, which carries behaviour while MAP carries state.

Setup is one command, run once per project:

```
/vouse-project:init [directory]
```

It seeds the structure, and on a repository that already has work it also runs
the adoption pass — surveying what exists and proposing the standing rules,
known defects, and portable knowhow the project already has but has not written
down. Nothing lands without the owner confirming it. Everything after setup runs
through the `vouse-project` skill.

The plugin carries two skills:

| Skill | Role |
|---|---|
| [`vouse-project`](skills/vouse-project/) | The lifecycle skill: seed a project, open and close versions and campaigns, route change requests, record frozen findings and freeze notes, capture portable knowhow as tracked project skills, and track known bugs. Ships derived-state scripts, an append-only record guard hook, and templates — all installed into the target project by `scripts/init.py`. |
| [`bob-write`](skills/bob-write/) | The writing register every prose surface of `vouse-project` is written in. Bundled because it is a required sub-skill; the plugin works standalone on a machine with nothing else installed. |

The bundled `bob-write` is a copy; the canonical source is
`plugins/vouse-skills/skills/bob-write/` in the sibling `Skills` repo. Edit there
and re-copy. If more than one bundle is enabled on one machine, `bob-write` is
listed once per copy; every listing loads the same content.

Design rationale — why this artefact set, and the production failures the
design answers — is in
[`skills/vouse-project/references/rationale.md`](skills/vouse-project/references/rationale.md).

Install via the `project-skills` marketplace at the repo root — see the
[repo README](../../README.md).
