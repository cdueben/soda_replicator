# Version Control Workflows for Replication Packages

Safe, reproducible version control practices for research projects.

---

## Choosing Your Interface

This guide provides instructions for both command line and GitHub Desktop. Choose what works for you:

| Interface | Best For | Pros | Cons |
|-----------|----------|------|------|
| **Command Line** (`git`, `gh`) | Power users, automation | Full control, scriptable | Steeper learning curve |
| **GitHub Desktop** | Visual learners, beginners | Easy to visualize changes | Some advanced features unavailable |

**GitHub Desktop Download:** https://desktop.github.com/

---

## Repository Setup

### Initial Setup for New Project

<details>
<summary><strong>Command Line</strong></summary>

```bash
# Create repository structure
mkdir my-project && cd my-project

# Initialize code repository
cd code
git init
git add .
git commit -m "Initial commit: project structure"

# Create remote (do this on GitHub first, then:)
git remote add origin https://github.com/username/my-project-code.git
git push -u origin main

# Repeat for paper repository
cd ../paper
git init
# ... same steps
```
</details>

<details>
<summary><strong>GitHub Desktop</strong></summary>

1. **Create repository on GitHub.com first:**
   - Go to github.com → Click "+" → "New repository"
   - Name it `my-project-code`
   - Check "Add a README file"
   - Click "Create repository"

2. **Clone in GitHub Desktop:**
   - File → Clone Repository
   - Select your new repository
   - Choose local path (e.g., `~/Documents/my-project/code`)
   - Click "Clone"

3. **Add your files:**
   - Copy your project files into the cloned folder
   - GitHub Desktop will show them as "Changes"

4. **Commit:**
   - Write summary: "Initial commit: project structure"
   - Click "Commit to main"

5. **Push:**
   - Click "Push origin" (top right)

6. **Repeat for paper repository**
</details>

### Clone Existing Project

```bash
# Clone code repo
git clone https://github.com/username/my-project-code.git code

# Clone paper repo
git clone https://github.com/username/my-project-paper.git paper

# Data folder (shared via cloud, not git)
# Download from Dropbox/Google Drive/etc.
```

---

## Daily Workflow

### Starting Work

<details>
<summary><strong>Command Line</strong></summary>

```bash
# Always start by pulling latest changes
git pull origin main

# Check status
git status

# Create feature branch for significant changes
git checkout -b feature/add-robustness-checks
```
</details>

<details>
<summary><strong>GitHub Desktop</strong></summary>

1. **Fetch and pull latest changes:**
   - Click "Fetch origin" (top right)
   - If changes exist, click "Pull origin"

2. **Check status:**
   - Left panel shows any local changes
   - "History" tab shows recent commits

3. **Create feature branch:**
   - Current Branch dropdown → "New Branch"
   - Name: `feature/add-robustness-checks`
   - Click "Create Branch"
</details>

### Making Changes

<details>
<summary><strong>Command Line</strong></summary>

```bash
# Stage specific files (preferred over git add .)
git add analysis/regressions.do
git add analysis/summary_stats.do

# Review what you're committing
git diff --staged

# Commit with descriptive message
git commit -m "Add robustness checks for main specification

- Cluster standard errors at state level
- Add year fixed effects
- Include demographic controls"
```
</details>

<details>
<summary><strong>GitHub Desktop</strong></summary>

1. **Select files to commit:**
   - Left panel shows all changed files
   - ✓ Check the files you want to commit
   - Uncheck files you want to exclude

2. **Review changes:**
   - Click on a file to see the diff (green = added, red = removed)

3. **Write commit message:**
   - Summary (required): "Add robustness checks for main specification"
   - Description (optional):
     ```
     - Cluster standard errors at state level
     - Add year fixed effects
     - Include demographic controls
     ```

4. **Commit:**
   - Click "Commit to [branch-name]"
</details>

### Pushing Changes

<details>
<summary><strong>Command Line</strong></summary>

```bash
# Push to remote
git push origin main

# Or if on feature branch
git push origin feature/add-robustness-checks
```
</details>

<details>
<summary><strong>GitHub Desktop</strong></summary>

1. **Push to remote:**
   - Click "Push origin" button (top right)
   - Or: Repository → Push

2. **If on a new branch:**
   - Click "Publish branch" (first time)
   - Then "Push origin" for subsequent pushes
</details>

---

## Safe Git Commands (Agent Can Execute)

These commands are read-only or reversible:

```bash
# Status and information
git status
git log --oneline -10
git diff
git diff --staged
git branch -a
git remote -v

# Viewing history
git show HEAD
git log --graph --oneline
git blame filename.do

# Fetching (doesn't change local files)
git fetch origin

# Stashing (temporary, reversible)
git stash
git stash list
git stash pop
```

---

## Moderate Risk Commands (Agent Should Confirm)

These make changes but are generally safe:

```bash
# Staging files
git add <specific-file>      # ✅ Preferred
git add .                    # ⚠️ Use cautiously

# Creating branches
git checkout -b new-branch
git branch new-branch

# Committing
git commit -m "message"

# Pulling (usually safe)
git pull origin main

# Creating tags
git tag v1.0
```

---

## Dangerous Commands (User Must Execute Manually)

**The agent will NEVER execute these. It will provide the command for you to review and run.**

### Pushing to Main/Master

```bash
# ⚠️ DANGEROUS: Review carefully before running
git push origin main

# Why dangerous:
# - Affects all collaborators immediately
# - Hard to undo if wrong
# - May trigger CI/CD pipelines
```

### Merging

```bash
# ⚠️ DANGEROUS: Always review PR first
git merge feature-branch

# Via GitHub CLI
gh pr merge <number> --merge

# Why dangerous:
# - Combines code that may conflict
# - Changes main branch history
# - May introduce bugs
```

### Deleting Branches

```bash
# ⚠️ DANGEROUS: Ensure branch is merged first
git branch -d feature-branch        # Safe: only deletes if merged
git branch -D feature-branch        # DANGEROUS: force delete

# Remote deletion
git push origin --delete feature-branch

# Why dangerous:
# - Loses unmerged work permanently
# - May break collaborators' workflows
```

### Resetting/Reverting

```bash
# ⚠️ DANGEROUS: Can lose work
git reset --hard HEAD~1    # Loses last commit AND changes
git reset --soft HEAD~1    # Keeps changes, undoes commit (safer)

# Safer alternative
git revert HEAD            # Creates new commit that undoes changes

# Why dangerous:
# - --hard loses uncommitted work
# - Can't easily undo if pushed
```

### Force Push

```bash
# ⛔ EXTREMELY DANGEROUS: Almost never appropriate
git push --force origin main

# Why forbidden:
# - Rewrites remote history
# - Breaks collaborators' repos
# - Can lose others' work permanently
```

---

## Pull Request Workflow

### Creating a PR (Safe)

<details>
<summary><strong>Command Line</strong></summary>

```bash
# Create and push branch
git checkout -b fix/typo-in-readme
# ... make changes ...
git add README.md
git commit -m "Fix typo in README"
git push -u origin fix/typo-in-readme

# Create PR via GitHub CLI
gh pr create --title "Fix typo in README" --body "Fixes small typo in installation instructions"
```
</details>

<details>
<summary><strong>GitHub Desktop</strong></summary>

1. **Create branch:**
   - Current Branch → New Branch → `fix/typo-in-readme`

2. **Make and commit changes:**
   - Edit files
   - Write commit message
   - Click "Commit to fix/typo-in-readme"

3. **Push and create PR:**
   - Click "Publish branch"
   - Click "Create Pull Request" (appears after push)
   - This opens GitHub.com in your browser

4. **On GitHub.com:**
   - Fill in PR title and description
   - Click "Create pull request"
</details>

### Reviewing a PR (Safe)

<details>
<summary><strong>Command Line</strong></summary>

```bash
# List open PRs
gh pr list

# View specific PR
gh pr view 123

# Check out PR locally for testing
gh pr checkout 123

# Add review comment
gh pr review 123 --comment --body "Looks good, but please add a test"
```
</details>

<details>
<summary><strong>GitHub Desktop</strong></summary>

1. **View PRs:**
   - Branch → Pull Requests (or use GitHub.com)

2. **Check out PR for testing:**
   - Branch → Pull Requests
   - Select the PR
   - Click "Checkout"
   - Test the code locally

3. **Add review comments:**
   - Go to GitHub.com → Pull requests → Select PR
   - Click "Files changed"
   - Click the `+` button on any line to add a comment
   - Click "Review changes" → Add summary → Submit
</details>

### Merging a PR (Dangerous - Manual Only)

⚠️ **Always review before merging. Never let an agent merge PRs automatically.**

<details>
<summary><strong>Command Line</strong></summary>

```bash
# ⚠️ ALWAYS review before merging
gh pr view 123                    # Review changes
gh pr checks 123                  # Verify CI passes
gh pr merge 123 --merge           # YOU run this manually
```
</details>

<details>
<summary><strong>GitHub Desktop / GitHub.com</strong></summary>

1. **Review on GitHub.com:**
   - Go to Pull Requests → Select PR
   - Review "Files changed" tab
   - Check that CI/checks pass (green checkmarks)

2. **Merge:**
   - Click "Merge pull request" button
   - Choose merge type:
     - "Create a merge commit" (default, preserves history)
     - "Squash and merge" (combines all commits)
     - "Rebase and merge" (linear history)
   - Click "Confirm merge"

3. **Delete branch (optional):**
   - Click "Delete branch" after merge
</details>

---

## Replication Package Version Control

### Pre-Submission Checklist

<details>
<summary><strong>Command Line</strong></summary>

```bash
# 1. Ensure clean working directory
git status
# Should show: "nothing to commit, working tree clean"

# 2. Tag the submission version
git tag -a v1.0-submission -m "Version submitted to journal"
git push origin v1.0-submission

# 3. Create GitHub release (via web or CLI)
gh release create v1.0-submission \
  --title "Replication Package v1.0" \
  --notes "Package submitted to [Journal] on [Date]"
```
</details>

<details>
<summary><strong>GitHub Desktop + GitHub.com</strong></summary>

1. **Ensure clean working directory:**
   - GitHub Desktop should show "No local changes"
   - If changes exist, commit or discard them

2. **Create tag on GitHub.com:**
   - Go to your repository on GitHub.com
   - Click "Releases" (right sidebar)
   - Click "Create a new release"
   - Click "Choose a tag" → Type `v1.0-submission` → "Create new tag"
   - Title: "Replication Package v1.0"
   - Description: "Package submitted to [Journal] on [Date]"
   - Click "Publish release"

Note: GitHub Desktop doesn't support creating tags directly. Use GitHub.com or command line.
</details>

### After Revision Requests

<details>
<summary><strong>Command Line</strong></summary>

```bash
# Create revision branch
git checkout -b revision-r1
# ... make changes ...
git commit -m "R1: Address reviewer comments on Table 2"
git push origin revision-r1

# When approved, merge and tag
git checkout main
git merge revision-r1
git tag -a v1.1-r1 -m "Revision 1 submitted"
git push origin main --tags
```
</details>

<details>
<summary><strong>GitHub Desktop</strong></summary>

1. **Create revision branch:**
   - Current Branch → New Branch → `revision-r1`

2. **Make changes and commit:**
   - Edit files as needed
   - Commit: "R1: Address reviewer comments on Table 2"
   - Push: Click "Publish branch"

3. **Create PR and merge (on GitHub.com):**
   - Click "Create Pull Request"
   - Review and merge on GitHub.com
   - Delete the revision branch

4. **Create tag (on GitHub.com):**
   - Releases → Create new release
   - Tag: `v1.1-r1`
   - Title: "Revision 1"
   - Publish
</details>

### Archiving Final Version

<details>
<summary><strong>Command Line</strong></summary>

```bash
# Tag final accepted version
git tag -a v2.0-accepted -m "Final accepted version"
git push origin v2.0-accepted

# Create release with DOI
gh release create v2.0-accepted \
  --title "Replication Package - Final" \
  --notes "Accepted version. DOI: 10.xxxx/xxxxx"
```
</details>

<details>
<summary><strong>GitHub.com</strong></summary>

1. **Create final release:**
   - Go to repository → Releases → "Create a new release"
   - Tag: `v2.0-accepted`
   - Title: "Replication Package - Final"
   - Description:
     ```
     Final accepted version.

     Published in: [Journal Name]
     DOI: 10.xxxx/xxxxx
     ```
   - Click "Publish release"

2. **Download for archive:**
   - After publishing, click "Source code (zip)"
   - Upload this to Zenodo/ICPSR for DOI
</details>

---

## Collaboration Patterns

### Working with Co-Authors

<details>
<summary><strong>Command Line</strong></summary>

```bash
# Add collaborator (do via GitHub web interface for safety)
# Settings → Collaborators → Add people

# Fetch their changes
git fetch origin
git log origin/main --oneline

# Pull and integrate
git pull origin main
```
</details>

<details>
<summary><strong>GitHub Desktop + GitHub.com</strong></summary>

1. **Add collaborator (GitHub.com):**
   - Repository → Settings → Collaborators
   - Click "Add people"
   - Enter their GitHub username or email
   - They'll receive an invitation

2. **Fetch their changes:**
   - GitHub Desktop: Click "Fetch origin"
   - If changes exist, click "Pull origin"

3. **View their commits:**
   - History tab shows all commits
   - Click a commit to see what changed
</details>

### Code Review Workflow

<details>
<summary><strong>Command Line</strong></summary>

```bash
# Author: Create PR
gh pr create --title "Add sensitivity analysis" --reviewer coauthor

# Reviewer: Check out and review
gh pr checkout 42
# ... run code, review ...
gh pr review 42 --approve

# Author: Merge (MANUAL)
gh pr merge 42 --merge
```
</details>

<details>
<summary><strong>GitHub Desktop + GitHub.com</strong></summary>

**Author:**
1. Create branch, make changes, push
2. Click "Create Pull Request" in GitHub Desktop
3. On GitHub.com, add reviewer in right sidebar

**Reviewer:**
1. Go to Pull Requests on GitHub.com
2. Review "Files changed" tab
3. To test locally:
   - GitHub Desktop → Branch → Pull Requests
   - Select the PR → Checkout
4. Add comments or approve
5. Click "Review changes" → "Approve" → "Submit review"

**Author (merge):**
1. After approval, click "Merge pull request" on GitHub.com
</details>

### Handling Conflicts

<details>
<summary><strong>Command Line</strong></summary>

```bash
# If pull fails with conflicts
git status                    # See conflicted files
# Edit files to resolve conflicts (look for <<<<<<< markers)
git add resolved-file.do
git commit -m "Resolve merge conflict in regressions.do"
```
</details>

<details>
<summary><strong>GitHub Desktop</strong></summary>

1. **When conflict occurs:**
   - GitHub Desktop shows "Resolve conflicts" banner
   - Lists conflicted files

2. **Resolve in editor:**
   - Click "Open in [Editor]" for each conflicted file
   - Look for conflict markers:
     ```
     <<<<<<< HEAD
     Your changes
     =======
     Their changes
     >>>>>>> branch-name
     ```
   - Edit to keep the correct version
   - Delete the conflict markers

3. **Mark as resolved:**
   - After editing, save the file
   - In GitHub Desktop, the file moves to "Changes"
   - Commit: "Resolve merge conflict in regressions.do"

4. **Alternative - Use merge tool:**
   - Right-click conflicted file
   - "Open with External Merge Tool"
   - (Requires merge tool like VS Code, Sublime Merge)
</details>

---

## .gitignore for Research Projects

### Code Repository

```gitignore
# Data (stored separately)
*.csv
*.dta
*.rds
*.parquet
!data/examples/*.csv

# Generated outputs
*.log
*.smcl
results/tables/*.tex
results/figures/*.pdf

# Environment
.Rhistory
.RData
.Rproj.user/
__pycache__/
*.pyc
.env

# OS files
.DS_Store
Thumbs.db

# Editor files
*.swp
*~
.vscode/
.idea/
```

### Paper Repository

```gitignore
# LaTeX build files
*.aux
*.bbl
*.blg
*.fdb_latexmk
*.fls
*.out
*.synctex.gz
*.toc

# But keep the PDF
!manuscript.pdf

# OS files
.DS_Store
```

---

## Recovery Procedures

### "I committed something wrong"

<details>
<summary><strong>Command Line</strong></summary>

```bash
# If not pushed yet:
git reset --soft HEAD~1      # Undo commit, keep changes
# Fix the issue, then recommit

# If already pushed:
git revert HEAD              # Create new commit that undoes it
git push origin main
```
</details>

<details>
<summary><strong>GitHub Desktop</strong></summary>

**If not pushed yet:**
1. History tab → Right-click the bad commit
2. Click "Undo Commit"
3. Changes return to "Changes" panel
4. Fix the issue, recommit

**If already pushed:**
1. History tab → Right-click the bad commit
2. Click "Revert Changes in Commit"
3. This creates a NEW commit that undoes it
4. Push the revert commit
</details>

### "I need to undo my last push"

<details>
<summary><strong>Command Line</strong></summary>

```bash
# DON'T force push. Instead:
git revert HEAD
git push origin main

# This preserves history and is safe for collaborators
```
</details>

<details>
<summary><strong>GitHub Desktop</strong></summary>

**Safe method (revert):**
1. History tab → Right-click the pushed commit
2. Click "Revert Changes in Commit"
3. New "revert" commit is created
4. Push origin

⚠️ Never use "Undo" on pushed commits - this requires force push.
</details>

### "I accidentally deleted a file"

<details>
<summary><strong>Command Line</strong></summary>

```bash
# If not committed:
git checkout -- deleted-file.do

# If committed but not pushed:
git reset --soft HEAD~1
git checkout -- deleted-file.do

# If pushed:
git checkout HEAD~1 -- deleted-file.do
git add deleted-file.do
git commit -m "Restore accidentally deleted file"
git push
```
</details>

<details>
<summary><strong>GitHub Desktop</strong></summary>

**If not committed:**
1. Changes panel → Right-click the deleted file
2. Click "Discard Changes"
3. File is restored

**If committed but not pushed:**
1. History tab → Right-click the commit
2. Click "Undo Commit"
3. Changes panel → Right-click deleted file
4. Click "Discard Changes"

**If already pushed:**
1. History tab → Find last commit that HAD the file
2. Right-click that commit
3. Click "Revert Changes in Commit" - ⚠️ This reverts ALL changes
4. Alternative: Use GitHub.com to view and copy the old file content
</details>

### "I need yesterday's version"

<details>
<summary><strong>Command Line</strong></summary>

```bash
# Find the commit
git log --oneline --since="2 days ago"

# View file at that commit
git show abc123:path/to/file.do

# Restore file from that commit
git checkout abc123 -- path/to/file.do
```
</details>

<details>
<summary><strong>GitHub Desktop + GitHub.com</strong></summary>

1. **Find the commit:**
   - GitHub Desktop → History tab
   - Scroll to find the date/commit you need
   - Note the commit message or hash

2. **View old version (GitHub.com):**
   - Go to repository on GitHub.com
   - Click "Commits"
   - Find and click the commit
   - Browse to the file
   - Click "View file" to see full content

3. **Restore old version:**
   - Copy the old file content from GitHub.com
   - Paste into your local file
   - Commit: "Restore [filename] to [date] version"

   *Or use command line:*
   ```bash
   git checkout abc123 -- path/to/file.do
   ```
</details>

---

## GitHub Desktop Quick Reference

| Task | GitHub Desktop |
|------|----------------|
| Clone repo | File → Clone Repository |
| Create branch | Current Branch → New Branch |
| Switch branch | Current Branch → Select branch |
| Stage files | Check boxes in Changes panel |
| Commit | Write message → Commit to [branch] |
| Push | Push origin (top bar) |
| Pull | Fetch origin → Pull origin |
| View history | History tab |
| Create PR | After push: "Create Pull Request" button |
| Undo commit | History → Right-click → Undo |
| Discard changes | Changes → Right-click file → Discard |
| View diff | Click file in Changes panel |
| Open in editor | Right-click file → Open in [Editor] |
| Stash changes | Branch → Stash All Changes |

**Limitations of GitHub Desktop:**
- Cannot create tags (use GitHub.com or CLI)
- Cannot cherry-pick commits
- Cannot interactive rebase
- Limited conflict resolution tools
- Cannot manage remotes (only origin)
