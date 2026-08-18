# ProjectSkills

Project-work [Claude Code](https://claude.com/claude-code) Agent Skills, packaged
as a plugin marketplace. The marketplace (`.claude-plugin/marketplace.json`)
exposes one plugin, `project-skills`, under `plugins/project-skills/`.

## Skills

| Skill | What it does |
|---|---|
| [`vouse-pm`](plugins/project-skills/skills/vouse-pm/) | Recall from / capture into a local PM-continuity tree — project status, timelines, correspondence, meeting minutes, schedules, weekly plans, handoffs. The tree's location is resolved per machine, never hardcoded. |
| [`bob-write`](plugins/project-skills/skills/bob-write/) | Write prose in "bob" — a flat, declarative engineering-specification register (condition-first, one term per concept, no marketing language). Bundled because `vouse-pm` writes its notes in it, so this plugin works on a machine with nothing else installed. |

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
    "project-skills@project-skills": true
  }
}
```

Or interactively: `/plugin marketplace add yankeeangelonero-hub/ProjectSkills`,
then install from `/plugin`.

The repo is private — the machine needs GitHub credentials that can read it
(`gh auth login` or a cached git credential).

## Relationship to the Skills repo

`vouse-pm` lives here and only here; it was moved out of
[`yankeeangelonero-hub/Skills`](https://github.com/yankeeangelonero-hub/Skills)
so that PM work installs without the rest of that suite.

`bob-write` is a copy. The canonical source is
`plugins/vouse-skills/skills/bob-write/` in the Skills repo, and it is also
bundled into the `vouse-project` plugin there for the same standalone reason.
Edit the canonical copy, then re-copy to both. If more than one of these
marketplaces is enabled on a machine, `bob-write` is listed once per copy; every
listing loads the same content.
