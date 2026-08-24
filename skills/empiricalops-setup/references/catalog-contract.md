# EmpiricalOps Catalog Contract

The bootstrap skill discovers installable packages from the public EmpiricalOps repository. The catalog should expose enough metadata to recommend, resolve, pin, and verify a skill without cloning every package first.

## Catalog Entry

```yaml
skills:
  commit-messager:
    path: skills/commit-messager
    version: 1.2.0
    commit: <full-commit-sha>
    checksum: <archive-sha256>
    capabilities:
      - git_commits
      - pull_requests
    dependencies: []
    setup_manifest: setup.yml
```

Required fields for installation are `path`, an immutable `version` or `commit`, and dependency information. A checksum is required when installation uses a packaged archive.

## Per-Skill Setup Manifest

Each configurable skill may include `setup.yml`:

```yaml
schema_version: 1

questions:
  - id: git.merge_strategy
    prompt: What should be the default PR merge strategy?
    type: choice
    options: [squash, merge, rebase]
    recommended: squash
    required: true
    scope: project

outputs:
  - target: GIT_HYGIENE.md
    mode: managed_section
    template: assets/git-hygiene-section.md

validation:
  - type: resolved_question
    id: git.merge_strategy
```

Question IDs are shared contracts. Two skills requesting `git.merge_strategy` must receive the same confirmed project-level answer rather than asking twice.

## Installation Plan

Before installation, show:

- catalog repository and pinned revision
- selected skills and dependency order
- project or user installation destination
- files that would be created, patched, or replaced
- unresolved questions and migrations
- validation to be run

Never install a skill merely because it is classified as Recommended.
