# AGENTS.md

> Project context for AI coding agents (Codex, Gemini, Cursor, etc.).

## Project Overview

This is the **code repository** for an applied-economics research project following the [SoDa Replicator](https://github.com/sodalabsio/soda_replicator) template. It is designed for reproducible, journal-ready analysis.

## Repository Structure

```
code/
├── dataprep/          # Data preparation scripts, organized by source
├── analysis/          # Analysis scripts (regressions, figures, tables)
├── checklist.md       # Replication compliance checklist
├── renv.lock          # R package lockfile (or requirements.txt for Python)
└── .github/
    ├── workflows/
    │   ├── claude.yml     # Claude code review (tag @claude in PRs/issues)
    │   └── codex.yml      # Codex code review (tag @codex in PRs/issues)
    └── skills/
        └── replication-compliance/   # DCAS compliance audit skill
```

Data lives in `../data/` (not tracked by git).
Paper lives in `../paper/` (separate repository).

## Coding Standards

**Always enforce these rules:**

- **Relative paths only.** All data reads must use `../data/...`. Never use absolute paths (`/Users/`, `C:\`, `/home/`).
- **Virtual environment.** `renv.lock` (R) or `requirements.txt` with pinned versions (Python) must be kept up to date.
- **Random seeds.** Set a seed before any randomization: `set.seed(12345)` (R), `np.random.seed(12345)` (Python), `set seed 12345` (Stata).
- **Output paths.** Figures and tables go to `../paper/results/figures/` and `../paper/results/tables/`.
- **No manual steps.** Scripts must run end-to-end without manual file operations.
- **Script headers.** Each script needs a header comment describing its purpose, inputs, and outputs.

## Review Guidelines

When reviewing a pull request or issue, check it against `checklist.md`. Only review items marked `[x]`.

## Replication Compliance Skill

The automated DCAS compliance checker is available at `.github/scripts/check_compliance.py`.

To run the automated checker:
```bash
python .github/scripts/check_compliance.py .
```

## Git Safety

| Level | Commands | Policy |
|-------|----------|--------|
| Safe | `git status`, `log`, `diff` | Execute freely |
| Moderate | `git add`, `commit`, `checkout -b` | Confirm first |
| Dangerous | `push`, `merge`, `rebase` | User runs manually |
| Forbidden | `push --force`, `reset --hard`, `clean -f` | Never execute |
