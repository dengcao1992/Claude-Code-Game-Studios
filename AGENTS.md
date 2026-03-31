# Codex Game Studios -- Agent Architecture

This repository was originally designed for Claude Code (`CLAUDE.md` + `.claude/`).
It now includes a Codex-compatible control plane centered on this `AGENTS.md` file and a dedicated Codex-compatible asset layout (`.agents/` + `.codex/`).

## Purpose

Turn one Codex session into a structured game-development studio using:
- **Subagents** (`.codex/agents/*.toml`)
- **Skills** (`.agents/skills/*/SKILL.md`)
- **Hooks** (`.codex/hooks.json` + `.codex/hooks/`)
- **Execution Rules** (`.codex/rules/*.rules`)
- **Templates** (`.claude/docs/templates/`)

Codex now has a native layout under `.agents/` and `.codex/`. Keep these in sync with `.claude/` via `tools/sync-codex-assets.sh`.

## Operating Protocol (Codex)

1. Ask clarifying questions before implementation when requirements are ambiguous.
2. Present options and tradeoffs for design-impacting decisions.
3. Keep changes scoped to the requested domain.
4. Run relevant checks/tests before commit.
5. Summarize changed files with citations in the final report.

## Delegation Model

- Directors define vision and constraints.
- Department leads own cross-feature consistency.
- Specialists implement scoped changes.
- Conflicts escalate to shared parent (creative/technical director), then producer.

Subagents live in `.codex/agents/*.toml` (converted from `.claude/agents/*.md`).

## Available Skills

Codex can load and execute the following skills directly from `SKILL.md` files.

### Onboarding & Planning
- start (`.agents/skills/start/SKILL.md`)
- project-stage-detect (`.agents/skills/project-stage-detect/SKILL.md`)
- setup-engine (`.agents/skills/setup-engine/SKILL.md`)
- sprint-plan (`.agents/skills/sprint-plan/SKILL.md`)
- milestone-review (`.agents/skills/milestone-review/SKILL.md`)
- estimate (`.agents/skills/estimate/SKILL.md`)
- retrospective (`.agents/skills/retrospective/SKILL.md`)

### Design & Analysis
- brainstorm (`.agents/skills/brainstorm/SKILL.md`)
- design-system (`.agents/skills/design-system/SKILL.md`)
- map-systems (`.agents/skills/map-systems/SKILL.md`)
- design-review (`.agents/skills/design-review/SKILL.md`)
- scope-check (`.agents/skills/scope-check/SKILL.md`)
- balance-check (`.agents/skills/balance-check/SKILL.md`)
- playtest-report (`.agents/skills/playtest-report/SKILL.md`)

### Engineering & QA
- code-review (`.agents/skills/code-review/SKILL.md`)
- perf-profile (`.agents/skills/perf-profile/SKILL.md`)
- tech-debt (`.agents/skills/tech-debt/SKILL.md`)
- architecture-decision (`.agents/skills/architecture-decision/SKILL.md`)
- gate-check (`.agents/skills/gate-check/SKILL.md`)
- bug-report (`.agents/skills/bug-report/SKILL.md`)
- asset-audit (`.agents/skills/asset-audit/SKILL.md`)
- reverse-document (`.agents/skills/reverse-document/SKILL.md`)

### Team-Orchestrated Workflows
- team-combat (`.agents/skills/team-combat/SKILL.md`)
- team-ui (`.agents/skills/team-ui/SKILL.md`)
- team-level (`.agents/skills/team-level/SKILL.md`)
- team-narrative (`.agents/skills/team-narrative/SKILL.md`)
- team-audio (`.agents/skills/team-audio/SKILL.md`)
- team-polish (`.agents/skills/team-polish/SKILL.md`)
- team-release (`.agents/skills/team-release/SKILL.md`)

### Release & Live Ops
- release-checklist (`.agents/skills/release-checklist/SKILL.md`)
- launch-checklist (`.agents/skills/launch-checklist/SKILL.md`)
- changelog (`.agents/skills/changelog/SKILL.md`)
- patch-notes (`.agents/skills/patch-notes/SKILL.md`)
- hotfix (`.agents/skills/hotfix/SKILL.md`)
- localize (`.agents/skills/localize/SKILL.md`)
- onboard (`.agents/skills/onboard/SKILL.md`)
- prototype (`.agents/skills/prototype/SKILL.md`)

## Rules and Hooks

- Execution rules are stored in `.codex/rules/*.rules` (Codex runtime policy rules).
- Path-scoped coding standards from `.claude/rules/*.md` are mirrored into `.codex/rules/project-standards/*.md`.
- Hook config is `.codex/hooks.json`, and scripts are in `.codex/hooks/`.

## Templates

Reusable content templates remain in `.claude/docs/templates/`.
Use them as starting points for GDDs, ADRs, sprint plans, and release docs.

## Compatibility Note

- **Claude Code users**: keep using `CLAUDE.md` and `.claude/settings.json`.
- **Codex users**: use this `AGENTS.md`, `.agents/skills/`, and `.codex/` configs.

This repository now ships both layouts (`.claude/` and Codex-native `.agents/.codex`) to support each frontend directly.

## Multi-Agent Usage (Codex)

Codex subagents are explicitly invoked by instruction in your prompt.
For usage patterns and copy-paste prompt templates, see:

- `docs/CODEX-MULTI-AGENT-USAGE.md`
