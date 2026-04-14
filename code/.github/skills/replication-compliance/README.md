# Replication Compliance Skill

Audit research repositories against the [Data and Code Availability Standard (DCAS)](https://datacodestandard.org) from within your AI coding tool.

> **Before installing:** This skill installs files globally into your AI tool's configuration directory (`~/.claude/skills/`, `~/.agents/skills/`, `~/.cursor/rules/`, etc.). Read [SKILL.md](SKILL.md) to understand what it does before running the installer.

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/Patrick-Healy/soda_replicator_dev/main/code/.github/skills/replication-compliance/install.sh | bash
```

The installer detects which AI tools you have installed (Claude Code, Codex, Cursor, Gemini) and copies the skill files to the correct location for each one. Only tools that are already installed on your machine are affected.

## What gets installed

| Tool | Location |
|------|----------|
| Claude Code | `~/.claude/skills/replication-compliance/` |
| OpenAI Codex | `~/.agents/skills/replication-compliance/` |
| Cursor | `~/.cursor/rules/replication-compliance.mdc` |
| Gemini CLI | `~/.gemini/skills/replication-compliance/` |

## Use it

**Claude Code** — from inside any research repository:
```
/replication-compliance
```

**Codex:**
```
$replication-compliance
```

**Cursor** — reference the rule in any prompt:
```
@replication-compliance audit this repo
```

## Full documentation

- [SKILL.md](SKILL.md) — complete audit workflow and checks
- [references/DCAS_RULES.md](references/DCAS_RULES.md) — all 16 DCAS rules explained
- [references/LANGUAGE_GUIDES.md](references/LANGUAGE_GUIDES.md) — Stata, R, Python, MATLAB, Julia specifics
- [references/CHECKLIST.md](references/CHECKLIST.md) — quick compliance checklist
- [scripts/check_compliance.py](scripts/check_compliance.py) — run automated checks without an AI tool
