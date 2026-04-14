# GitHub MCP Server Setup Guide

This guide helps users set up the GitHub MCP (Model Context Protocol) server for safe version control integration with AI agents.

## What is the GitHub MCP Server?

The [GitHub MCP Server](https://github.com/github/github-mcp-server) allows AI agents to interact with GitHub through natural language. It enables:

- Repository exploration and code searching
- Issue and PR creation/management
- GitHub Actions monitoring
- Security vulnerability detection
- Team collaboration features

## Safety First: Understanding Risk Levels

### Command Risk Categories

| Risk Level | Operations | Agent Behavior |
|------------|------------|----------------|
| 🟢 **Safe** | Read repos, list issues, view PRs, search code | Agent can execute freely |
| 🟡 **Moderate** | Create issues, comment, create branches | Agent should confirm first |
| 🔴 **Dangerous** | Merge PRs, delete branches, push to main, close issues | **User must execute manually** |
| ⛔ **Forbidden** | Force push, delete repos, modify permissions | **Never execute** |

### Dangerous Commands - Manual Only

The agent will **never** execute these commands automatically. Instead, it will provide the command for you to run manually:

```bash
# DANGEROUS - Always run manually after review

# Merging PRs
gh pr merge <number> --merge

# Deleting branches
gh branch -d <branch-name>
git push origin --delete <branch-name>

# Force operations
git push --force  # NEVER use without explicit user request
git reset --hard  # Can lose uncommitted work

# Closing/deleting
gh issue close <number>
gh pr close <number>
gh repo delete <repo>  # Extremely dangerous
```

---

## Setup Options

### Option 1: Remote Server (Recommended for Beginners)

The easiest setup - no local installation required.

**For VS Code / Cursor:**
1. Install the GitHub MCP extension
2. Authenticate with GitHub OAuth
3. MCP tools become available automatically

**Manual Configuration:**

Add to your MCP settings (location varies by agent):

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```

### Option 2: Local Docker Server (Recommended for Privacy)

Run the server locally for more control.

**Step 1: Create a GitHub Personal Access Token (PAT)**

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens
2. Click "Generate new token"
3. Configure:
   - **Name:** `mcp-server-local`
   - **Expiration:** 90 days (recommended)
   - **Repository access:** Select specific repositories (safer) or all
   - **Permissions:** See minimum scopes below

**Minimum Required Scopes:**
```
Repository permissions:
  - Contents: Read (for code access)
  - Issues: Read and write (for issue management)
  - Pull requests: Read and write (for PR management)
  - Metadata: Read (always required)

Account permissions:
  - (none required for basic use)
```

**Step 2: Store Token Securely**

```bash
# Create secure environment file
echo 'GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here' > ~/.github-mcp.env
chmod 600 ~/.github-mcp.env

# Add to .gitignore globally
echo '.github-mcp.env' >> ~/.gitignore_global
git config --global core.excludesfile ~/.gitignore_global
```

**Step 3: Run Docker Container**

```bash
# Load token and run
source ~/.github-mcp.env
docker run -i --rm \
  -e GITHUB_PERSONAL_ACCESS_TOKEN \
  ghcr.io/github/github-mcp-server
```

**Step 4: Configure Your Agent**

Add to MCP configuration:

```json
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

### Option 3: Local Binary (No Docker)

For users who cannot or prefer not to use Docker.

**⚠️ RISK WARNING: Non-Docker Installation**

| Risk | Description | Mitigation |
|------|-------------|------------|
| **System-wide installation** | Binary runs with your user permissions | Use read-only mode, limit token scopes |
| **No isolation** | No container sandbox | Never run with admin/sudo |
| **Update management** | You must manually update | Check for updates monthly |
| **Dependency conflicts** | Go runtime required | Use pre-built binaries if available |

**When to use non-Docker:**
- Docker not available (institutional restrictions, Windows Home)
- Performance-critical (slight overhead reduction)
- Offline environments (air-gapped systems)

**Step 1: Install Go (if not installed)**

```bash
# macOS
brew install go

# Ubuntu/Debian
sudo apt install golang-go

# Windows - download from https://go.dev/dl/
```

**Step 2: Build from Source**

```bash
# Clone repository
git clone https://github.com/github/github-mcp-server.git
cd github-mcp-server

# Build binary
go build -o github-mcp-server ./cmd/github-mcp-server

# Move to a permanent location
mkdir -p ~/.local/bin
mv github-mcp-server ~/.local/bin/

# Verify installation
~/.local/bin/github-mcp-server --help
```

**Step 3: Configure Your Agent**

```json
{
  "mcpServers": {
    "github": {
      "command": "${HOME}/.local/bin/github-mcp-server",
      "args": ["stdio", "--read-only"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

**Step 4: Set Up Token (Critical for Security)**

```bash
# Create token file with restricted permissions
echo 'export GITHUB_PERSONAL_ACCESS_TOKEN=ghp_yourtoken' > ~/.github-mcp-token
chmod 600 ~/.github-mcp-token

# Add to shell profile (.bashrc, .zshrc)
echo 'source ~/.github-mcp-token' >> ~/.zshrc

# NEVER commit this file
echo '.github-mcp-token' >> ~/.gitignore_global
```

### Option 4: npx/npm (Simplest Non-Docker)

If you have Node.js installed:

```bash
# Run directly without installation
npx @anthropic/github-mcp-server --read-only

# Or install globally
npm install -g @anthropic/github-mcp-server
```

**⚠️ Note:** Check if npm package is available; the official distribution may be Docker-only.

### Option 5: Pre-built Binaries

Check the [releases page](https://github.com/github/github-mcp-server/releases) for pre-built binaries:

```bash
# Download for your platform
curl -LO https://github.com/github/github-mcp-server/releases/latest/download/github-mcp-server-darwin-arm64

# Make executable
chmod +x github-mcp-server-darwin-arm64
mv github-mcp-server-darwin-arm64 ~/.local/bin/github-mcp-server
```

### Comparison: Docker vs Non-Docker

| Aspect | Docker | Non-Docker |
|--------|--------|------------|
| **Isolation** | ✅ Full container sandbox | ⚠️ Runs as your user |
| **Setup complexity** | Medium (need Docker) | Low-Medium |
| **Performance** | Slight overhead | Native speed |
| **Updates** | `docker pull` | Manual rebuild |
| **Offline use** | Need image cached | ✅ Fully offline |
| **Windows Home** | ❌ Not available | ✅ Works |
| **Institutional IT** | May be blocked | Usually allowed |

**Recommendation:** Use Docker if available. Use non-Docker only when Docker is not an option, and always enable `--read-only` mode.

---

## Safe Configuration Modes

### Read-Only Mode (Safest)

Prevents any modifications - ideal for exploration and learning:

```bash
docker run -i --rm \
  -e GITHUB_PERSONAL_ACCESS_TOKEN \
  ghcr.io/github/github-mcp-server \
  --read-only
```

Or in configuration:
```json
{
  "mcpServers": {
    "github": {
      "command": "github-mcp-server",
      "args": ["stdio", "--read-only"]
    }
  }
}
```

### Limited Toolsets

Only enable the tools you need:

```bash
# Only repos and issues (no PR merging, no deletions)
github-mcp-server stdio --toolsets repos,issues
```

**Recommended Safe Toolset:**
```
repos,issues,pull_requests,code_security
```

**Avoid for Safety:**
```
actions (can trigger workflows)
```

### Enterprise/Private Repos

For GitHub Enterprise:

```bash
export GITHUB_HOST=https://github.mycompany.com
github-mcp-server stdio
```

---

## Agent-Specific Setup

### Claude Code

Claude Code can use the `gh` CLI directly. No MCP setup required for basic operations:

```bash
# Verify gh is installed and authenticated
gh auth status

# Basic operations work out of the box
gh repo view
gh issue list
gh pr list
```

For MCP integration, add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server", "--read-only"]
    }
  }
}
```

### Cursor

Add to Cursor MCP settings:

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```

### VS Code with Copilot

Use the built-in GitHub integration or install the MCP extension.

### Other Agents (Gemini CLI, OpenCode, etc.)

Check your agent's MCP configuration documentation. Most support the standard format:

```json
{
  "mcpServers": {
    "github": {
      "command": "path/to/github-mcp-server",
      "args": ["stdio"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "..."
      }
    }
  }
}
```

---

## Security Best Practices

### Token Management

```bash
# ✅ DO: Use environment variables
export GITHUB_PERSONAL_ACCESS_TOKEN=$(cat ~/.github-token)

# ✅ DO: Use separate tokens per project
# project-a uses token with access to repo-a only
# project-b uses token with access to repo-b only

# ✅ DO: Set expiration dates
# Use 90-day tokens and rotate regularly

# ❌ DON'T: Hardcode tokens in config files
# ❌ DON'T: Commit tokens to git
# ❌ DON'T: Share tokens between users
# ❌ DON'T: Use tokens with excessive permissions
```

### File Permissions

```bash
# Secure your token files
chmod 600 ~/.github-mcp.env
chmod 600 ~/.github-token

# Verify permissions
ls -la ~/.github-mcp.env
# Should show: -rw-------
```

### .gitignore Protection

Add to your global gitignore:

```bash
# ~/.gitignore_global
.env
.github-mcp.env
*.token
*_token
.secrets
```

### Audit Your Access

Regularly review:

1. **Token permissions:** GitHub → Settings → Developer settings → Personal access tokens
2. **Repository access:** Which repos can the token access?
3. **Recent activity:** GitHub → Settings → Security log

---

## Troubleshooting

### "Authentication failed"

```bash
# Check token is set
echo $GITHUB_PERSONAL_ACCESS_TOKEN | head -c 10

# Verify token works
gh auth status
curl -H "Authorization: token $GITHUB_PERSONAL_ACCESS_TOKEN" https://api.github.com/user
```

### "Permission denied"

Token lacks required scopes. Regenerate with correct permissions.

### "Rate limited"

GitHub API has rate limits. Authenticated requests get 5,000/hour. Wait or use a different token.

### Docker Issues

```bash
# Ensure Docker is running
docker info

# Pull latest image
docker pull ghcr.io/github/github-mcp-server

# Check for port conflicts
docker ps
```

---

## Quick Reference Card

```bash
# Safe read operations (agent can do freely)
gh repo view owner/repo
gh issue list --repo owner/repo
gh pr list --repo owner/repo
gh api repos/owner/repo

# Moderate operations (agent should confirm)
gh issue create --title "..." --body "..."
gh pr create --title "..." --body "..."

# Dangerous operations (YOU must run manually)
gh pr merge <number>
gh issue close <number>
git push origin main

# Forbidden (never run)
git push --force
gh repo delete
```
