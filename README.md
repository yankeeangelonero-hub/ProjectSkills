# ProjectSkills

Project-work [Claude Code](https://claude.com/claude-code) Agent Skills, packaged
as a plugin marketplace. The marketplace (`.claude-plugin/marketplace.json`)
exposes one plugin, `vouse-project`, under `plugins/vouse-project/`.

## The plugin

[`vouse-project`](plugins/vouse-project/) manages a project's lifecycle on a
fixed artefact set — `MAP.md`, `LEDGER.md`, `LAW.md`, `CLAUDE.md`, `record/`,
`work/`, `issues/`, `skills/`. Skills judge, scripts execute, hooks enforce, and
state is derived from ground truth or it does not exist. Setup is one command run
once per project, on a fresh repo or one already in progress:

```
/vouse-project:init [directory]
```

| Skill | What it does |
|---|---|
| [`vouse-project`](plugins/vouse-project/skills/vouse-project/) | Seed a project, open and close versions and campaigns, route change requests, record frozen findings, capture portable project knowhow as tracked skills, and track known bugs. Ships the derived-state scripts, the append-only record guard hook, and the templates that `init` installs into the target project. |
| [`bob-write`](plugins/vouse-project/skills/bob-write/) | Write prose in "bob" — a flat, declarative engineering-specification register (condition-first, one term per concept, no marketing language). Bundled because every prose surface of `vouse-project` is written in it, so the plugin works on a machine with nothing else installed. |

Design rationale — why this artefact set, and the production failures it answers
— is in
[`references/rationale.md`](plugins/vouse-project/skills/vouse-project/references/rationale.md).

## Installing

Register the marketplace once and enable the plugin; with `autoUpdate` a push to
this repo reaches every machine on startup.

Declarative (in `~/.claude/settings.json`):

```json
{
  "extraKnownMarketplaces": {
    "project-skills": {
      "source": { "source": "github", "repo": "yankeeangelonero-hub/ProjectSkills" },
      "autoUpdate": true
    }
  },
  "enabledPlugins": {
    "vouse-project@project-skills": true
  }
}
```

Or interactively: `/plugin marketplace add yankeeangelonero-hub/ProjectSkills`,
then install from `/plugin`.

The marketplace itself is still named `project-skills`, so a machine that already
registered it keeps that entry; only the plugin key changes — the old
`project-skills@project-skills` becomes `vouse-project@project-skills`.

The repo is private — the machine needs GitHub credentials that can read it
(`gh auth login` or a cached git credential).

## Relationship to the Skills repo

`vouse-project` is also published from
[`yankeeangelonero-hub/Skills`](https://github.com/yankeeangelonero-hub/Skills)
as `plugins/vouse-project/`; this marketplace carries it alone so project work
installs without the rest of that suite. Keep the two copies in step.

`bob-write` is a copy. The canonical source is
`plugins/vouse-skills/skills/bob-write/` in the Skills repo. Edit the canonical
copy, then re-copy to every bundle. If more than one of these marketplaces is
enabled on a machine, `bob-write` is listed once per copy; every listing loads
the same content.

The earlier `vouse-pm` skill that this marketplace used to carry has been
replaced by `vouse-project`; it remains in this repo's git history.
