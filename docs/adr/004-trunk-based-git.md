# ADR-004: Trunk-Based Git Workflow with Atomic Conventional Commits

## Status

Accepted

## Context

We need a version control workflow suitable for a solo/small-team open-source
project. It should be simple, enforce discipline, and produce a clean `main`
history.

Options considered:

1. **Git Flow** — `develop`, `release`, `hotfix` branches. Too heavyweight for
   phase 1.

2. **GitHub Flow** — feature branches off `main`, PRs, no `develop`. Simple but
   doesn't enforce commit discipline.

3. **Trunk-based with feature branches** — short-lived branches off `main`,
   squash-merge, conventional commits. Enforces atomic commits and produces a
   clean linear history.

## Decision

Use trunk-based development with feature branches:

- `main` is always deployable and passes `pyrefly check` + `pytest`
- Branch naming: `feat/`, `fix/`, `chore/`, `docs/`
- Squash-merge feature branches to `main`
- Write squash commit messages as conventional commits
- Each commit within a branch must be atomic and pass type checking

### Commit Convention

```
feat: add requirements gathering agent
fix: correct cost estimate for multi-region deployments
test: add edge case coverage for tradeoff analyzer
chore: configure pyrefly with strict mode
docs: update pipeline workflow in AGENTS.md
```

## Consequences

- Positive: Clean, readable `main` history
- Positive: Forces small, focused commits that are easy to review
- Positive: Works well for solo dev and scales to small teams
- Negative: Requires discipline to use `git add -p` for atomic commits
- Negative: No `develop` branch for integration testing before `main`
