# EmpiricalOps Catalog Contract

The bootstrap skill discovers installable packages from the public EmpiricalOps repository. Resolve the catalog itself at an immutable commit or release and record that revision in the project lockfile. Entries describe packages inside that pinned catalog; they do not repeat a self-referential commit that becomes stale whenever the catalog changes.

## Catalog Entry

```yaml
skills:
  commit-messager:
    path: skills/commit-messager
    import_method: vendor-copy
    capabilities:
      - git_commits
      - pull_requests
    dependencies: []
    setup_manifest: setup.yml
```

Required entry fields are `path`, `import_method`, and dependency information. The installation plan must separately include the immutable catalog revision. A checksum is required when installation uses a separately published package archive.

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

Templates use `{{ question.id }}` placeholders. Render scalar values directly and lists as comma-separated values. Managed-section templates must carry stable start and end markers so repeated setup updates only the owned section.

## Installation Plan

Before installation, show:

- catalog repository and pinned revision
- selected skills and dependency order
- project or user installation destination
- files that would be created, patched, or replaced
- unresolved questions and migrations
- validation to be run

Never install a skill merely because it is classified as Recommended.
