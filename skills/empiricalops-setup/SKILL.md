---
name: empiricalops-setup
description: Bootstrap or audit an empirical research repository through a guided interview, recommend and install EmpiricalOps skills from the public catalog, and generate project-local workflow configuration. Use when starting EmpiricalOps in a new or existing repo, adding capabilities, or checking setup drift. Do not silently install skills or overwrite project guidance.
---

# EmpiricalOps Setup

Configure the project through a short, evidence-based interview. Scan first, ask only questions that cannot be answered safely from the repository, and show a proposed plan before making changes.

## Modes

- `init`: create the first project profile and skill plan.
- `add`: recommend and configure additional skills for a new workflow.
- `audit`: compare the repository, installed skills, and lockfile without changing them.
- `update`: propose pinned skill upgrades and any required configuration migration.

## Workflow

1. Inspect the repository read-only: languages, manuscript layout, Git branches, submodules, existing guidance, installed skills, and data boundaries.
2. Read [references/question-flow.md](references/question-flow.md) and ask the unresolved project-level questions. Present detected values as suggestions, not facts the user has already approved.
3. Record confirmed answers using [references/config-schema.md](references/config-schema.md). Never render unresolved required values into project guidance.
4. Read the public EmpiricalOps catalog described in [references/catalog-contract.md](references/catalog-contract.md). Recommend skills as Required, Recommended, or Optional based on the user's actual workflows.
5. Show the skill source, pinned version or commit, dependencies, installation scope, files to be created or changed, and any per-skill questions. Obtain confirmation before downloading, installing, or modifying files.
6. Resolve dependencies, then process each selected skill's `setup.yml`. Reuse answers with the same stable question ID; ask only conditional or unresolved questions.
7. Patch managed sections rather than replacing human-authored files. Preserve existing repository conventions unless the user explicitly chooses to change them.
8. Validate installed skills and generated configuration. Return a setup receipt listing confirmed decisions, installed versions, changed files, skipped recommendations, and unresolved items.

## Decision Rules

- Separate detection, recommendation, and authorization. Detection never authorizes mutation.
- Project-local guidance overrides catalog defaults. A current user answer overrides both.
- Use `null` for unresolved decisions in the draft profile. Do not substitute sample identities or placeholder text.
- Git identity defaults to `inherit`, which means do not write a name or email. Ask for both only when the user chooses a dedicated identity.
- Recommend `squash` as the general PR merge default, but record it only after confirmation.
- Pin installations to a catalog commit or release and verify the package checksum when provided. Do not install from an unpinned moving branch.
- Installation does not grant a skill permission to perform future external or destructive actions.

The current skeleton specifies orchestration and configuration contracts. If the requested mode requires an installer that is not yet implemented, produce the plan and stop before installation rather than improvising download or overwrite behavior.
