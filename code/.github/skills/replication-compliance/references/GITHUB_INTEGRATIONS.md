# AI Code Review Integrations for Research Replication

This guide covers setting up AI coding assistants to check replication compliance. There are **two distinct architectures** for AI code assistance, each suited to different workflows.

---

## Two Models of AI Assistance

### Cloud Sandbox Environments (Provider-Managed VMs)

The AI runs your code in isolated virtual machines managed by the provider. Best for **interactive analysis and remediation**.

| Platform | Access | Code Execution | Config File |
|----------|--------|----------------|-------------|
| **[Claude Code on Web](https://claude.ai/code)** | Pro/Max/Team/Enterprise | Full sandbox (bubblewrap/seatbelt) | `CLAUDE.md` |
| **[OpenAI Codex Cloud](https://chatgpt.com/codex)** | ChatGPT Plus/Pro/Team | Full sandbox (containers) | `AGENTS.md` |

**How it works:**
1. Connect your GitHub account in the web UI
2. Select a repository
3. Submit a task (e.g., "Run the compliance checker and fix any issues")
4. AI clones repo to isolated VM, executes code, runs tests, iterates
5. Review changes and create PR

**Pros:** Interactive, stateful sessions; can run scripts and fix issues autonomously
**Cons:** Manual process; code uploaded to provider's servers; may lack specialized tools (Stata, MATLAB)

### GitHub Actions (Runs on Your Runners)

The AI model is called from CI/CD workflows running on GitHub's infrastructure. Best for **automated, continuous verification**.

| Platform | Action | Trigger | Config File |
|----------|--------|---------|-------------|
| **GitHub Copilot** | Native (rulesets) | `@copilot review` | `copilot-instructions.md` |
| **Claude Code** | `anthropics/claude-code-action@v1` | `@claude` | `CLAUDE.md` |
| **Gemini CLI** | `google-github-actions/run-gemini-cli@v1` | `@gemini-cli` | `GEMINI.md` |
| **OpenAI Codex** | `openai/codex-action@v1` | `@codex review` | `AGENTS.md` |
| **Cursor CLI** | Custom YAML | Custom | `permissions.json` |

**How it works:**
1. Configure workflow YAML and secrets
2. AI reviews code on PR open or @mention
3. Posts comments with findings
4. Can run `check_compliance.py` as part of workflow

**Pros:** Automated; full environment control; runs on every PR; code stays on GitHub
**Cons:** Less interactive; requires YAML configuration

### Architecture Comparison

| Aspect | Cloud Sandbox | GitHub Actions |
|--------|--------------|----------------|
| **Where code runs** | Provider's isolated VMs | GitHub-hosted runners |
| **Code execution** | Full (tests, scripts, iteration) | Workflow-defined only |
| **Environment control** | Provider's "universal" image | Full control (any language/version) |
| **Interactivity** | High (chat-based) | Low (automated) |
| **Data privacy** | Code on provider servers | Code on GitHub infrastructure |
| **Best for** | Interactive remediation | Continuous verification |

---

## Recommended Strategy for Replication Compliance

Use **both approaches** for a complete compliance workflow:

### 1. Automated PR Checks (GitHub Actions)

Run `check_compliance.py` on every pull request:

```yaml
name: Compliance Check
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Run Compliance Check
        id: check
        run: |
          python .github/skills/replication-compliance/scripts/check_compliance.py . --json > compliance.json
          echo "## Compliance Report" >> $GITHUB_STEP_SUMMARY
          python .github/skills/replication-compliance/scripts/check_compliance.py . >> $GITHUB_STEP_SUMMARY

      - name: Post Results
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const results = JSON.parse(fs.readFileSync('compliance.json', 'utf8'));
            const body = `## DCAS Compliance Check\n\n` +
              `**Score:** ${results.summary.score} (${results.summary.percent}%)\n` +
              `**Errors:** ${results.summary.errors} | **Warnings:** ${results.summary.warnings}\n\n` +
              `See job summary for full report.`;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: body
            });
```

### 2. Interactive Remediation (Cloud Sandbox)

When a PR fails the automated check:

1. Open [claude.ai/code](https://claude.ai/code) or [chatgpt.com/codex](https://chatgpt.com/codex)
2. Connect to the repository
3. Ask: *"Run the compliance checker at `.github/skills/replication-compliance/scripts/check_compliance.py` and fix any errors found"*
4. Review the AI's changes in the diff view
5. Create a PR with the fixes

This combination provides **continuous automated verification** plus **efficient interactive remediation**.

---

## Security Considerations

### Cloud Sandboxes

| Concern | Mitigation |
|---------|------------|
| **Data privacy** | Code uploaded to provider servers (review their data policies) |
| **Credentials** | Never in sandbox; handled via secure proxy with scoped tokens |
| **Network access** | Limited by default; configurable per environment |

### GitHub Actions

| Concern | Mitigation |
|---------|------------|
| **Secret management** | Use GitHub Secrets; never hardcode API keys |
| **Runner security** | GitHub-hosted = fresh VM per job; self-hosted = your responsibility |
| **Supply chain** | Pin action versions to SHA (e.g., `@b4ffde65...` not `@v5`) |
| **Prompt injection** | Don't grant `contents: write` unless needed; review AI suggestions |

---

## Tool-Specific Setup

### Quick Reference

| Tool | Recommended Setup | Documentation |
|------|-------------------|---------------|
| **GitHub Copilot** | Repository Rulesets | [Copilot Code Review](https://docs.github.com/copilot/using-github-copilot/code-review/using-copilot-code-review) |
| **Claude Code** | `claude /install-github-app` | [Claude Code Action](https://github.com/anthropics/claude-code-action) |
| **Claude Web** | Connect GitHub at claude.ai/code | [Claude Code on Web](https://code.claude.com/docs/en/claude-code-on-the-web) |
| **Codex Cloud** | Connect GitHub at chatgpt.com/codex | [Codex Cloud](https://developers.openai.com/codex/cloud/) |
| **Codex Action** | YAML workflow | [Codex GitHub Action](https://developers.openai.com/codex/github-action/) |
| **Gemini CLI** | `gemini /setup-github` | [run-gemini-cli](https://github.com/google-github-actions/run-gemini-cli) |

---

## 1. GitHub Copilot (Native - Recommended)

GitHub Copilot has built-in code review requiring no GitHub Actions setup.

### Setup via Repository Ruleset (Recommended)

1. Go to **Settings** → **Rules** → **Rulesets**
2. Click **New ruleset** → **New branch ruleset**
3. Name the ruleset (e.g., "AI Code Review") and set to **Active**
4. Under "Target branches," select your main branches
5. Under "Branch rules," enable **"Automatically request Copilot code review"**
6. Optional: Enable "Review new pushes" and "Review draft pull requests"
7. Click **Create**

### Organization-Wide Setup

1. Go to **Organization Settings** → **Repository** → **Rulesets**
2. Create a new branch ruleset
3. Under "Target repositories," use patterns (e.g., `*` for all, `research-*` for prefixed repos)
4. Enable automatic Copilot code review
5. Click **Create**

### Custom Instructions

Create `.github/copilot-instructions.md`:

```markdown
## Code Review Instructions

When reviewing pull requests in this research repository, focus on DCAS compliance:

### Critical Checks [MUST FLAG]
1. **Absolute Paths**: Flag paths like C:\, /Users/, /home/, ~
2. **Missing Seeds**: Verify random seeds before randomization
   - Stata: `set seed`
   - R: `set.seed()`
   - Python: `random.seed()`, `np.random.seed()`
   - MATLAB: `rng()`

### High Priority [SHOULD FLAG]
3. **Unpinned Dependencies**: Python packages without `==` version pins
4. **Missing Documentation**: README not updated with changes

### Severity Levels
- `[CRITICAL]` - Will break replication
- `[HIGH]` - Significant reproducibility risk
- `[MEDIUM]` - Best practice violation
```

### Path-Specific Instructions

Create `.github/instructions/data-review.instructions.md`:

```markdown
---
applyTo: data/**
---
For changes to data files, verify:
- Data availability statement is updated
- Codebook reflects any schema changes
- Data citations are complete
```

### Manual Review

Comment `@copilot review` on any PR.

### References
- [Using Copilot Code Review](https://docs.github.com/copilot/using-github-copilot/code-review/using-copilot-code-review)
- [Configuring Automatic Code Review](https://docs.github.com/en/copilot/using-github-copilot/code-review/configuring-automatic-code-review-by-copilot)

---

## 2. Claude Code Action

### Quick Setup (Recommended)

```bash
# In terminal with Claude Code installed
claude /install-github-app
```

This automatically:
- Creates and installs a GitHub App
- Configures repository secrets
- Creates the workflow file

**Requirements:** Repository admin access, Anthropic API key

### Manual Setup

1. Install the Claude GitHub App: https://github.com/apps/claude
2. Add `ANTHROPIC_API_KEY` to repository secrets (Settings → Secrets → Actions)
3. Create `.github/workflows/claude-review.yml`:

```yaml
name: Claude Code Review

on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]

jobs:
  claude-review:
    # Only run when @claude is mentioned
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
      issues: write
    steps:
      - name: Checkout repository
        uses: actions/checkout@v6
        with:
          fetch-depth: 0

      - name: Run Claude Code Action
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

### Automatic PR Review

For automatic reviews on all PRs (no @mention needed):

```yaml
name: Claude Auto Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  auto-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 0

      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Review this PR for DCAS compliance:
            1. Check for absolute paths (C:\, /Users/, /home/)
            2. Verify random seeds before randomization
            3. Check dependency pinning
            4. Verify documentation updates

            Reference: .github/skills/replication-compliance/SKILL.md
```

### Project Context

Create `CLAUDE.md` in your repository root:

```markdown
# Project Context for Claude

## This Repository
Research replication package following DCAS v1.0 standards.

## Code Review Focus
- Portability: No absolute paths
- Reproducibility: Random seeds, deterministic sorts
- Dependencies: Pinned versions
- Documentation: README accuracy

## Languages
Primary: [Stata/R/Python/MATLAB]
```

### References
- [Claude Code Action](https://github.com/anthropics/claude-code-action)
- [Setup Guide](https://github.com/anthropics/claude-code-action/blob/main/docs/setup.md)

---

## 3. Gemini CLI GitHub Action

### Quick Setup (Recommended)

```bash
# In Gemini CLI
gemini
/setup-github
```

This creates the necessary workflow files automatically.

### Manual Setup

1. Get API key from [Google AI Studio](https://aistudio.google.com/)
2. Add `GEMINI_API_KEY` to repository secrets
3. Add to `.gitignore`:
   ```
   .gemini/
   gha-creds-*.json
   ```
4. Download workflows:

```bash
mkdir -p .github/workflows
curl -o .github/workflows/gemini-dispatch.yml \
  https://raw.githubusercontent.com/google-github-actions/run-gemini-cli/main/examples/workflows/gemini-dispatch/gemini-dispatch.yml
curl -o .github/workflows/gemini-review.yml \
  https://raw.githubusercontent.com/google-github-actions/run-gemini-cli/main/examples/workflows/pr-review/gemini-review.yml
```

### Simplified Single Workflow

```yaml
name: Gemini Code Review

on:
  pull_request:
    types: [opened, synchronize]
  issue_comment:
    types: [created]

jobs:
  review:
    if: |
      github.event_name == 'pull_request' ||
      contains(github.event.comment.body, '@gemini-cli')
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
      issues: write
    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Run Gemini Review
        uses: google-github-actions/run-gemini-cli@v1
        with:
          gemini_api_key: ${{ secrets.GEMINI_API_KEY }}
```

### Project Context

Create `GEMINI.md` in repository root:

```markdown
# Gemini Review Guidelines

## Project Type
Research replication package (DCAS v1.0)

## Review Focus Areas
1. **Portability**: No absolute paths
2. **Reproducibility**: Seeds set, sorts deterministic
3. **Dependencies**: Versions pinned
4. **Documentation**: README current

## Severity Levels
- 🔴 Critical: Will break replication
- 🟠 High: Significant risk
- 🟡 Medium: Best practice
- 🟢 Low: Suggestion
```

### Custom Review Commands

Create `.gemini/commands/compliance-review.toml`:

```toml
[command]
name = "compliance-review"
description = "Review PR for DCAS compliance"

[prompt]
system = """
You are a research replication expert reviewing code for DCAS compliance.
Focus on: absolute paths, random seeds, dependency pinning, documentation.
"""
```

Trigger with: `@gemini-cli /compliance-review`

### References
- [run-gemini-cli](https://github.com/google-github-actions/run-gemini-cli)
- [PR Review Workflow](https://github.com/google-github-actions/run-gemini-cli/tree/main/examples/workflows/pr-review)
- [Gemini CLI GitHub Actions Blog](https://blog.google/technology/developers/introducing-gemini-cli-github-actions/)

---

## 4. OpenAI Codex

Codex offers both cloud-based (web UI) and GitHub Action integrations.

### Cloud Setup (chatgpt.com/codex) - Easiest

1. Go to [chatgpt.com/codex](https://chatgpt.com/codex)
2. Click **Connect GitHub** and authorize
3. Select repositories to enable
4. In Codex settings, toggle **Code review** for each repository
5. Optional: Enable **Automatic reviews** for all PRs

**Usage:** Comment `@codex review` on any PR, or reviews happen automatically if enabled.

### GitHub Action Setup

1. Add `OPENAI_API_KEY` to repository secrets
2. Create `.github/workflows/codex-review.yml`:

```yaml
name: Codex Code Review

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  codex-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - name: Checkout
        uses: actions/checkout@v6
        with:
          ref: refs/pull/${{ github.event.pull_request.number }}/merge

      - name: Fetch base and head refs
        run: |
          git fetch --no-tags origin \
            ${{ github.event.pull_request.base.ref }} \
            +refs/pull/${{ github.event.pull_request.number }}/head

      - name: Run Codex Review
        uses: openai/codex-action@v1
        with:
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          prompt-file: .github/codex/prompts/compliance-review.md
          sandbox: workspace-write
          safety-strategy: drop-sudo
```

### Review Prompt

Create `.github/codex/prompts/compliance-review.md`:

```markdown
Review this pull request for research replication compliance (DCAS v1.0):

## Critical Issues (P0)
- Absolute paths (C:\, /Users/, /home/, ~/)
- Missing random seeds before randomization

## High Priority (P1)
- Unpinned dependencies in requirements.txt
- Missing documentation updates

## Output
Provide findings as GitHub review comments with severity labels.
Reference AGENTS.md for project-specific guidance.
```

### Review Guidelines

Create or update `AGENTS.md`:

```markdown
## Review Guidelines

### Replication Compliance
When reviewing PRs, check for DCAS compliance:
- No absolute paths
- Random seeds set
- Dependencies pinned
- Documentation updated

### Priority Levels
- P0: Will break replication
- P1: Significant risk
- P2: Best practice
```

### References
- [Codex GitHub Integration](https://developers.openai.com/codex/integrations/github/)
- [Codex GitHub Action](https://developers.openai.com/codex/github-action/)
- [Codex Cloud](https://developers.openai.com/codex/cloud/)

---

## 5. Cursor CLI

Cursor CLI offers fine-grained permission control, making it ideal for security-conscious workflows.

### Setup

1. Generate API key from Cursor dashboard
2. Add `CURSOR_API_KEY` to repository secrets:
   ```bash
   gh secret set CURSOR_API_KEY --repo OWNER/REPO --body "$CURSOR_API_KEY"
   ```
3. Create workflow:

```yaml
name: Cursor Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Install Cursor CLI
        run: |
          curl https://cursor.com/install -fsS | bash
          echo "$HOME/.cursor/bin" >> $GITHUB_PATH

      - name: Run Review (Restricted Mode)
        env:
          CURSOR_API_KEY: ${{ secrets.CURSOR_API_KEY }}
        run: |
          agent -p "Review this PR for DCAS compliance. Do NOT create branches, commit, or push. Only analyze and comment."
```

### Permission-Based Restrictions (Key Security Feature)

Create `.cursor/permissions.json`:

```json
{
  "permissions": {
    "allow": [
      "Read(**/*)",
      "Shell(grep)",
      "Shell(python .github/skills/replication-compliance/scripts/check_compliance.py)"
    ],
    "deny": [
      "Shell(git)",
      "Shell(gh)",
      "Write(.env*)",
      "Write(**/credentials*)"
    ]
  }
}
```

This restricts the agent to:
- Read any file
- Run grep and the compliance checker
- Cannot modify git, GitHub CLI, or sensitive files

### References
- [Cursor CLI GitHub Actions](https://cursor.com/docs/cli/github-actions)

---

## 6. Google Antigravity (IDE-Based)

Antigravity is Google's new agentic IDE (VS Code fork) with built-in rules and workflows.

### Configuration Locations

| Scope | Rules | Workflows |
|-------|-------|-----------|
| Global | `~/.gemini/GEMINI.md` | `~/.gemini/antigravity/global_workflows/` |
| Workspace | `.agent/rules/` | `.agent/workflows/` |

### Example Rule

Create `.agent/rules/replication-compliance.md`:

```markdown
# Replication Compliance Rule

When generating or reviewing code:
1. Never use absolute paths - use relative paths or environment variables
2. Always set random seeds before any randomization
3. Pin all dependency versions explicitly
4. Update README when changing data or code structure
```

### Example Workflow

Create `.agent/workflows/compliance-check.md`:

```markdown
# Compliance Check Workflow

Run the DCAS compliance checker on the current project:

1. Execute: `python .github/skills/replication-compliance/scripts/check_compliance.py .`
2. Review the output for errors and warnings
3. Suggest fixes for any issues found
```

Invoke with `/compliance-check` in the Antigravity chat.

### References
- [Customize Antigravity with Rules and Workflows](https://atamel.dev/posts/2025/11-25_customize_antigravity_rules_workflows/)

---

## Security Best Practices

### 1. Pin Action Versions (Recommended)

Instead of floating tags, use commit SHAs:

```yaml
# Less secure (tag can be moved)
uses: actions/checkout@v6

# More secure (immutable)
uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11
```

### 2. Minimal Permissions

Only grant what's needed:

```yaml
permissions:
  contents: read        # Read code (always needed)
  pull-requests: write  # Post review comments
  # Omit: contents: write, issues: write (unless needed)
```

### 3. Conditional Triggers

Avoid running on every event:

```yaml
jobs:
  review:
    # Only run when explicitly requested
    if: contains(github.event.comment.body, '@claude')
```

### 4. Prompt Injection Awareness

AI tools read PR content, which could contain malicious instructions. Mitigations:
- Use Cursor's `permissions.json` to restrict actions
- Don't grant `contents: write` unless necessary
- Review AI suggestions before merging

### 5. Secret Management

- Never hardcode API keys in workflows
- Use repository or organization secrets
- Rotate keys periodically
- Use environment-specific secrets for staging/production

---

## Unified Instructions Approach

For teams using multiple AI tools, maintain a single source of truth:

### Create Master Instructions

Create `.github/AI_INSTRUCTIONS.md`:

```markdown
# AI Code Review Instructions

## Project Type
Research replication package following DCAS v1.0

## Critical Checks
1. **Absolute Paths**: Flag C:\, /Users/, /home/, ~/
2. **Random Seeds**: Verify seeds before randomization
3. **Dependencies**: Check version pinning
4. **Documentation**: Verify README updates

## Language-Specific
- Stata: `set seed`, `version`, `set varabbrev off`
- R: `set.seed()`, renv.lock
- Python: `random.seed()`, requirements.txt with ==
- MATLAB: `rng()`, toolbox documentation
```

### Copy to Tool-Specific Locations

Add a setup step to your workflows:

```yaml
- name: Prepare AI Instructions
  run: |
    cp .github/AI_INSTRUCTIONS.md CLAUDE.md
    cp .github/AI_INSTRUCTIONS.md GEMINI.md
    cp .github/AI_INSTRUCTIONS.md AGENTS.md
    mkdir -p .github && cp .github/AI_INSTRUCTIONS.md .github/copilot-instructions.md
```

---

## Integration with check_compliance.py

All AI reviewers can leverage the automated compliance checker:

```yaml
- name: Run Compliance Check
  id: compliance
  run: |
    python .github/skills/replication-compliance/scripts/check_compliance.py . --json > compliance.json
    echo "results<<EOF" >> $GITHUB_OUTPUT
    cat compliance.json >> $GITHUB_OUTPUT
    echo "EOF" >> $GITHUB_OUTPUT

- name: AI Review with Context
  uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: |
      Review this PR. The automated compliance checker found:
      ${{ steps.compliance.outputs.results }}

      Focus on the flagged issues and verify they're addressed.
```

This combines automated detection with AI-powered contextual feedback.

---

## Environment Considerations for Research Replication

Research projects often require specific software versions (Stata 17, R 4.3, MATLAB R2024a) that may not be available in cloud sandbox "universal" images.

### Cloud Sandbox Limitations

- Pre-installed tools may not include Stata, MATLAB, or Julia
- Specific R/Python package versions may differ from `renv.lock` or `requirements.txt`
- Cannot easily replicate complex research environments

### GitHub Actions Advantage

Full control over the execution environment:

```yaml
- name: Set up R
  uses: r-lib/actions/setup-r@v2
  with:
    r-version: '4.3.2'

- name: Install R dependencies
  run: |
    Rscript -e 'renv::restore()'

- name: Run compliance check
  run: python check_compliance.py . --json
```

**For research replication**, GitHub Actions is preferred for running the compliance checker because you can match the project's exact environment.

---

## Choosing the Right Approach

### By Use Case

| Use Case | Recommended Approach |
|----------|---------------------|
| **Continuous PR verification** | GitHub Actions (any tool) |
| **Interactive issue fixing** | Cloud Sandbox (Claude/Codex) |
| **Simple code review** | GitHub Copilot (native) |
| **Complex multi-step tasks** | Cloud Sandbox + Gemini dispatch |
| **Security-sensitive repos** | Cursor CLI (permissions.json) |

### By Platform

| If you already use... | Recommended Tool |
|----------------------|-----------------|
| GitHub Enterprise | **GitHub Copilot** (native, rulesets) |
| ChatGPT Plus/Pro | **Codex Cloud** + Codex Action |
| Claude Pro/Max | **Claude Code Web** + Claude Action |
| Google Cloud | **Gemini CLI** (Vertex AI auth) |
| VS Code/Cursor | **Cursor CLI** or IDE extensions |

### For Research Replication Specifically

1. **Automated checks**: GitHub Actions with `check_compliance.py` (full environment control)
2. **Interactive remediation**: Claude Code on Web or Codex Cloud (stateful fixing)
3. **Quick PR review**: GitHub Copilot with custom instructions (lowest friction)

The combination of **automated verification + interactive remediation** provides the most robust compliance workflow.
