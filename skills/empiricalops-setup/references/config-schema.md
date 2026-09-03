# Project Configuration Schema

Store confirmed and unresolved setup state in `.empiricalops/project.yml`. Store installed package resolution separately in `.empiricalops/skills.lock`.

## Placeholder Policy

- Use YAML `null` only in a draft profile to mean unanswered.
- Omit optional fields that are not applicable.
- Never use sample names, emails, paths, or branch names as operative defaults.
- Defaults belong in question manifests; confirmed answers belong in the project profile.
- Do not render a Markdown rule from a required field whose value is `null`.

This prevents a template value such as `Your Name`, `main`, or `squash` from becoming an accidental project rule.

## Core Shape

```yaml
schema_version: 1

project:
  kind: null

install:
  scope: null             # project | user

git:
  base_branch: null
  merge_strategy: null    # squash | merge | rebase
  commit_style: null
  scopes: null            # confirmed non-empty list when commit hygiene is configured
  identity:
    mode: inherit         # inherit | dedicated
    name: null            # required only for dedicated
    email: null           # required only for dedicated

writing:
  mode: null              # same_repo | submodule | separate_repo | none
  path: null
  merge_before_parent: null

outputs:
  exploratory_policy: null

data:
  restricted_policy: null
  external_root: null

empirics:
  default_winsorization: null
  default_fixed_effects: null
  default_clustering: null

reflection:
  activation: null        # explicit | suggest_after_complex_task
  public_repo: null
  save_local_reports: false
```

## Source Metadata

Implementations may store how an answer was obtained:

```yaml
decisions:
  git.merge_strategy:
    value: squash
    source: user
    confirmed_at: 2026-08-23
```

Detection should be represented as a proposal until confirmed:

```yaml
proposals:
  git.base_branch:
    value: dev
    source: detected
```

## Completion Semantics

Installation state and configuration state are independent. Derive rather than guess the final status:

- `skills_installed`: installed folders match a pinned lockfile.
- `profile_draft`: required answers or managed outputs are missing.
- `setup_complete`: `scripts/validate_project_setup.py` passes.

Optional empirical defaults may remain `null` intentionally. Required fields and conditional requirements are enforced by the validator.

## Git Identity

`inherit` means the setup must not write `user.name` or `user.email` into project files or Git configuration. It may report that an identity is configured without copying it into generated documentation.

When `mode: dedicated`, both `name` and `email` are required and must come from the user. Setup must state whether it proposes command-scoped identity, repository-local Git config, or documentation only; these are distinct mutations.
