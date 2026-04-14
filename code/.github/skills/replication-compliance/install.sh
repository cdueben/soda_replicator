#!/bin/bash
#
# install.sh — Install the replication-compliance skill globally
#
# Detects installed AI tools and copies skill files to the correct location.
# Can be run locally (from within a downloaded soda_replicator) or via curl.
#
# Usage:
#   bash install.sh                  # Run locally from skill directory
#   curl -fsSL <url>/install.sh | bash   # Run remotely via curl
#

set -e

SKILL_NAME="replication-compliance"
REPO="Patrick-Healy/soda_replicator_dev"
SKILL_PATH="code/.github/skills/replication-compliance"
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

echo_green() { echo -e "${GREEN}$1${NC}"; }
echo_yellow() { echo -e "${YELLOW}$1${NC}"; }
echo_bold() { echo -e "${BOLD}$1${NC}"; }

INSTALLED=()

echo ""
echo_bold "========================================"
echo_bold "  Replication Compliance Skill Installer"
echo_bold "========================================"
echo ""

# --- Determine source directory ---
# If piped via curl, SCRIPT_DIR won't exist — clone from GitHub instead
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-/dev/null}")" 2>/dev/null && pwd || echo "")"

if [ -f "$SCRIPT_DIR/SKILL.md" ]; then
    # Running locally — use existing files
    SOURCE="$SCRIPT_DIR"
    echo "Installing from local files at: $SOURCE"
else
    # Running via curl — sparse clone from GitHub
    echo "Downloading skill from github.com/$REPO ..."
    TMPDIR_PATH=$(mktemp -d)
    git clone --filter=blob:none --sparse --quiet \
        "https://github.com/$REPO.git" "$TMPDIR_PATH/repo" 2>/dev/null
    cd "$TMPDIR_PATH/repo"
    git sparse-checkout set "$SKILL_PATH" --quiet
    SOURCE="$TMPDIR_PATH/repo/$SKILL_PATH"
    CLEANUP="$TMPDIR_PATH"
fi

echo ""

# --- Install per tool ---

if command -v claude &>/dev/null || [ -d "$HOME/.claude" ]; then
    DEST="$HOME/.claude/skills/$SKILL_NAME"
    mkdir -p "$DEST"
    cp -R "$SOURCE/." "$DEST/"
    echo_green "✓ Claude Code  →  ~/.claude/skills/$SKILL_NAME/"
    INSTALLED+=("Claude Code")
fi

if command -v codex &>/dev/null || [ -d "$HOME/.agents" ] || [ -d "$HOME/.codex" ]; then
    DEST="$HOME/.agents/skills/$SKILL_NAME"
    mkdir -p "$DEST"
    cp -R "$SOURCE/." "$DEST/"
    echo_green "✓ Codex        →  ~/.agents/skills/$SKILL_NAME/"
    INSTALLED+=("Codex")
fi

if [ -d "$HOME/.cursor" ]; then
    mkdir -p "$HOME/.cursor/rules"
    cp "$SOURCE/SKILL.md" "$HOME/.cursor/rules/$SKILL_NAME.mdc"
    echo_green "✓ Cursor       →  ~/.cursor/rules/$SKILL_NAME.mdc"
    INSTALLED+=("Cursor")
fi

if command -v gemini &>/dev/null || [ -d "$HOME/.gemini" ]; then
    DEST="$HOME/.gemini/skills/$SKILL_NAME"
    mkdir -p "$DEST"
    cp -R "$SOURCE/." "$DEST/"
    echo_green "✓ Gemini       →  ~/.gemini/skills/$SKILL_NAME/"
    INSTALLED+=("Gemini")
fi

# --- Cleanup ---
[ -n "${CLEANUP:-}" ] && rm -rf "$CLEANUP"

echo ""
if [ ${#INSTALLED[@]} -eq 0 ]; then
    echo_yellow "No supported AI tools detected (Claude Code, Codex, Cursor, Gemini)."
    echo "Install one of these tools and run this script again."
else
    echo_bold "Installed for: ${INSTALLED[*]}"
    echo ""
    echo "Usage:"
    echo "  Claude Code:  /replication-compliance"
    echo "  Codex:        \$replication-compliance"
    echo "  Cursor:       @replication-compliance"
    echo ""
    echo_yellow "Restart your AI tool to load the skill."
fi
echo ""
