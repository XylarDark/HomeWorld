# Create PR

Create a well-structured pull request with Conventional Commits and proper branch/description.

## Steps

1. **Prepare branch**
   - Ensure all changes are committed (no uncommitted work unless intentional).
   - Push branch to remote.
   - Verify branch is up to date with main (rebase or merge as per team preference).

2. **Commit message**
   - Use Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, etc. (see `.cursor/rules/04-git-workflow.mdc`).
   - Branch naming: `feat/`, `fix/`, `docs/`, etc. (e.g. `feat/pcg-volume-bounds`).
   - PowerShell: use `;` not `&&` for chaining; use here-strings for multi-line commit messages.

3. **PR description**
   - Summarize what changed and why.
   - List any breaking changes or follow-up work.
   - Add screenshots or notes if UI/behavior changed.
   - Link related issues or task docs if applicable.

4. **Open PR**
   - Create the PR (e.g. `gh pr create` or via GitHub UI).
   - Add labels and reviewers as needed.

## Checklist

- [ ] Commits follow Conventional Commits
- [ ] Branch name matches change type
- [ ] No secrets or `.env` in commits
- [ ] Pre-commit checks passed (lint, build if applicable)
