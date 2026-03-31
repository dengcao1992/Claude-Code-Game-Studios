#!/usr/bin/env python3
from pathlib import Path
import json, shutil, re

ROOT = Path(__file__).resolve().parent.parent
CLAUDE = ROOT / '.claude'

# 1) Skills: Codex expects .agents/skills
skills_dst = ROOT / '.agents' / 'skills'
if skills_dst.exists():
    shutil.rmtree(skills_dst)
skills_dst.parent.mkdir(parents=True, exist_ok=True)
shutil.copytree(CLAUDE / 'skills', skills_dst)

# 2) Hooks: .codex/hooks + .codex/hooks.json
hooks_dst = ROOT / '.codex' / 'hooks'
if hooks_dst.exists():
    shutil.rmtree(hooks_dst)
hooks_dst.parent.mkdir(parents=True, exist_ok=True)
shutil.copytree(CLAUDE / 'hooks', hooks_dst)

root_cmd = '$(git rev-parse --show-toplevel)'
def hook_cmd(name: str) -> str:
    return f'bash "{root_cmd}/.codex/hooks/{name}"'

converted = {
    'hooks': {
        'SessionStart': [
            {'matcher': '', 'hooks': [
                {'type': 'command', 'command': hook_cmd('session-start.sh'), 'timeout': 10},
                {'type': 'command', 'command': hook_cmd('detect-gaps.sh'), 'timeout': 10},
            ]}
        ],
        'PreToolUse': [
            {'matcher': 'Bash', 'hooks': [
                {'type': 'command', 'command': hook_cmd('validate-commit.sh'), 'timeout': 15},
                {'type': 'command', 'command': hook_cmd('validate-push.sh'), 'timeout': 10},
            ]}
        ],
        # Codex currently emits Bash for PostToolUse; keep validation hooks on Bash output checks only.
        'PostToolUse': [
            {'matcher': 'Bash', 'hooks': [
                {'type': 'command', 'command': hook_cmd('validate-assets.sh'), 'timeout': 10},
            ]}
        ],
        'Stop': [
            {'matcher': '', 'hooks': [
                {'type': 'command', 'command': hook_cmd('session-stop.sh'), 'timeout': 10},
            ]}
        ]
    }
}
(ROOT / '.codex' / 'hooks.json').write_text(json.dumps(converted, indent=2) + '\n')

# 3) Subagents: .codex/agents/*.toml converted from .claude/agents/*.md
agents_dst = ROOT / '.codex' / 'agents'
if agents_dst.exists():
    shutil.rmtree(agents_dst)
agents_dst.mkdir(parents=True, exist_ok=True)

model_map = {
    'opus': 'gpt-5.4',
    'sonnet': 'gpt-5.3-codex-spark',
    'haiku': 'gpt-5.3-codex-spark',
}

def parse_frontmatter(text: str):
    if not text.startswith('---\n'):
        return {}, text
    end = text.find('\n---\n', 4)
    if end == -1:
        return {}, text
    fm = text[4:end]
    body = text[end+5:]
    data = {}
    for line in fm.splitlines():
        if ':' not in line:
            continue
        k, v = line.split(':', 1)
        data[k.strip()] = v.strip().strip('"')
    return data, body.strip()

for md in sorted((CLAUDE / 'agents').glob('*.md')):
    text = md.read_text()
    fm, body = parse_frontmatter(text)
    name = fm.get('name', md.stem).replace('-', '_')
    desc = fm.get('description', f'Game studio specialist: {md.stem}')
    model = model_map.get(fm.get('model', '').lower(), 'gpt-5.3-codex-spark')
    sandbox = 'workspace-write'
    if 'disallowedTools' in fm and 'Bash' in fm['disallowedTools']:
        sandbox = 'read-only'
    content = (
        f'name = "{name}"\n'
        f'description = {json.dumps(desc)}\n'
        f'model = "{model}"\n'
        f'sandbox_mode = "{sandbox}"\n'
        'developer_instructions = """\n'
        f'{body}\n'
        '"""\n'
    )
    (agents_dst / f'{md.stem}.toml').write_text(content)

# 4) Rules: Codex .rules are exec policy; project coding standards are mirrored as markdown references.
rules_dst = ROOT / '.codex' / 'rules'
rules_dst.mkdir(parents=True, exist_ok=True)
(rules_dst / 'default.rules').write_text(
    '# Execution safety rules for Codex\n'
    'prefix_rule(pattern = ["rm", "-rf"], decision = "deny", justification = "Dangerous delete blocked.")\n'
    'prefix_rule(pattern = ["git", "push", "--force"], decision = "deny", justification = "Force push blocked.")\n'
    'prefix_rule(pattern = ["git", "reset", "--hard"], decision = "deny", justification = "Hard reset blocked.")\n'
)

standards_dst = rules_dst / 'project-standards'
if standards_dst.exists():
    shutil.rmtree(standards_dst)
shutil.copytree(CLAUDE / 'rules', standards_dst)

summary = [
    '# Project Path-Scoped Coding Standards',
    '',
    'These files are mirrored from `.claude/rules/*.md` for Codex users.',
    'When editing matching paths, consult the referenced markdown rule file before changing code.',
    '',
]
for md in sorted(standards_dst.glob('*.md')):
    summary.append(f'- `{md.name}` -> `.codex/rules/project-standards/{md.name}`')
summary.append('')
(rules_dst / 'README.md').write_text('\n'.join(summary))

print('Synced Codex assets: .agents/skills, .codex/agents, .codex/hooks, .codex/rules (+project-standards)')
