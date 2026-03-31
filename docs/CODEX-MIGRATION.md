# Codex Migration Notes (from Claude layout)

This repository keeps `.claude/` as the source content, then maps it into Codex-native locations:

- Claude agents (`.claude/agents/*.md`) -> Codex subagents (`.codex/agents/*.toml`)
- Claude skills (`.claude/skills/*/SKILL.md`) -> Codex skills (`.agents/skills/*/SKILL.md`)
- Claude hooks (`.claude/hooks/*.sh` + `.claude/settings.json`) -> Codex hooks (`.codex/hooks/*.sh` + `.codex/hooks.json`)
- Claude path coding standards (`.claude/rules/*.md`) are mirrored to `.codex/rules/project-standards/*.md`; Codex execution policy rules are in `.codex/rules/*.rules`

## Why this mapping

Codex official docs define different native locations and formats:

1. `AGENTS.md` is project guidance.
2. Skills are discovered from `.agents/skills` (project scope) and `~/.codex/skills` (global scope).
3. Subagents are loaded from `.codex/agents/*.toml`.
4. Hooks use `.codex/hooks.json` (+ scripts) with the hooks feature flag enabled in `config.toml`.
5. Rules use `.rules` files for command/policy behavior, not markdown coding-style documents.

## Sync workflow

Run:

```bash
./tools/sync-codex-assets.sh
```

This regenerates:

- `.agents/skills/`
- `.codex/agents/`
- `.codex/hooks/`
- `.codex/hooks.json`
- `.codex/rules/default.rules`
- `.codex/rules/project-standards/*.md`

after updates in `.claude/`.
