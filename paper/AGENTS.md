# AGENTS.md

> Project context for AI coding agents (Codex, Gemini, Cursor, etc.).

## Project Overview

This is the **paper repository** for an applied-economics research project following the [SoDa Replicator](https://github.com/sodalabsio/soda_replicator) template.

## Repository Structure

```
paper/
├── draft/             # LaTeX manuscript source
├── presentation/      # Slides source
├── results/
│   ├── figures/       # Figures exported from code repo
│   └── tables/        # Tables exported from code repo
└── checklist.md       # Paper review checklist
```

Code and data live in separate repositories (`../code/`, `../data/`).

## Review Standards

When reviewing a pull request or issue, check it against `checklist.md`. Only review items marked `[x]`.

**Key rules:**

- **Figures and tables.** Every figure/table cited in the text must exist in `results/`. Numbers and content must match.
- **Standard errors.** Tables must show SEs in parentheses; clustering must be specified.
- **Significance stars.** If used, define them in table notes (e.g., `* p<0.10, ** p<0.05, *** p<0.01`).
- **Consistency.** Results must be identical across the manuscript, presentation, and results files.
- **LaTeX.** All cross-references must resolve; document must compile cleanly.

## Git Safety

| Level | Commands | Policy |
|-------|----------|--------|
| Safe | `git status`, `log`, `diff` | Execute freely |
| Moderate | `git add`, `commit`, `checkout -b` | Confirm first |
| Dangerous | `push`, `merge`, `rebase` | User runs manually |
| Forbidden | `push --force`, `reset --hard`, `clean -f` | Never execute |
