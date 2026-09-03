---
name: empiricalops-setup
description: Bootstrap, extend, or audit an empirical research repository through a guided interview, a pinned EmpiricalOps skill plan, and validated project-local workflow configuration. Use when starting EmpiricalOps, adding capabilities, or checking setup drift. Install only through an available supported installer after explicit approval.
---

# EmpiricalOps Setup

Configure the project through a short, evidence-based interview. Scan first, ask only questions that cannot be answered safely from the repository, and keep installation state separate from setup completion.

## Modes

- `init`: create the first project profile and skill plan.
- `add`: recommend and configure additional skills for a new workflow.
- `audit`: compare the repository, installed skills, and lockfile without changing them.
- `update`: propose pinned skill upgrades and any required configuration migration.

## Workflow

1. Inspect the repository read-only: languages, manuscript layout, Git branches, submodules, existing guidance, installed skills, and data boundaries.
2. Read [references/question-flow.md](references/question-flow.md) and ask the unresolved project-level questions. Present detected values as suggestions, not facts the user has already approved.
3. Present unresolved decisions as explicit `question.id = proposed value` entries. A confirmation applies only to entries shown in that confirmation request. Record confirmed answers using [references/config-schema.md](references/config-schema.md). Never render unresolved required values into project guidance.
4. Read the public EmpiricalOps catalog described in [references/catalog-contract.md](references/catalog-contract.md). Recommend skills as Required, Recommended, or Optional based on the user's actual workflows.
5. Show the skill source, pinned catalog revision, dependencies, installation scope, files to be created or changed, and unresolved questions. Obtain confirmation before downloading, installing, or modifying files.
6. Resolve dependencies, then process each selected skill's `setup.yml`. Reuse answers with the same stable question ID; ask only conditional or unresolved questions. Treat these manifests as declarations; this setup skill owns orchestration.
7. Install only with an available supported installer that can pin the catalog revision and preserve complete skill folders. If none is available, produce the plan and stop with status `profile_draft`.
8. Patch managed sections rather than replacing human-authored files. Preserve existing repository conventions unless the user explicitly chooses to change them. Ensure generated guidance is routed from the repository's active agent-guidance file when a selected skill requires that output.
9. Run `scripts/validate_project_setup.py` against the profile, lockfile, and project root. Return a receipt that labels the result as `skills_installed`, `profile_draft`, or `setup_complete`, and lists confirmed decisions, installed revisions, changed files, skipped recommendations, and unresolved items.

## Decision Rules

- Separate detection, recommendation, and authorization. Detection never authorizes mutation.
- Never interpret a bare confirmation as approval for values that were not displayed with their stable question IDs.
- Project-local guidance overrides catalog defaults. A current user answer overrides both.
- Use `null` for unresolved decisions in the draft profile. Do not substitute sample identities or placeholder text.
- Git identity defaults to `inherit`, which means do not write a name or email. Ask for both only when the user chooses a dedicated identity.
- Recommend `squash` as the general PR merge default, but record it only after confirmation.
- Pin the catalog checkout to a commit or release and verify package checksums when provided. Do not install from an unpinned moving branch.
- Installation does not grant a skill permission to perform future external or destructive actions.

## Completion Gate

- `skills_installed`: approved skill folders exist and their immutable catalog revision is recorded, but project configuration may still be incomplete.
- `profile_draft`: one or more required or conditionally required decisions remain unresolved, or required managed outputs have not been generated and routed.
- `setup_complete`: the validator passes, every confirmed value is recorded, installed skills match the lockfile, and every required managed output is present and discoverable.

Never call installation alone setup completion.
