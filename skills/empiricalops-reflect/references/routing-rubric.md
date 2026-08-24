# Reflection Routing Rubric

Route the lesson by the narrowest durable scope that preserves the owner's intent.

## Local Project

Use `local_project` when the lesson depends on facts or decisions specific to the active repository:

- project branch names or submodule topology
- variable definitions, sample windows, or empirical specifications
- restricted-data locations and source vintages
- artifact ownership, manuscript paths, or release sequence
- a one-project exception to an EmpiricalOps default

Typical targets are `AGENTS.md`, `GIT_HYGIENE.md`, `.empiricalops/project.yml`, a source map, or a repo-local skill.

## Public EmpiricalOps

Use `public_empiricalops` for a stable owner preference or reusable operating rule that can be published safely. General popularity is not required because the repository is owner-oriented.

Examples include:

- defaulting exploratory PRs to squash merge
- preserving user-authored dirty worktree changes
- separating generated replication outputs from paper-facing artifacts
- asking a setup question before writing Git identity
- proposing rather than automatically applying session reflections

Typical targets are an existing skill, fallback reference, public template, catalog contract, or setup question. State when project-local guidance may override the public default.

## No Durable Change

Use `no_change` when:

- the event is a transient tool or command failure
- an existing instruction is already clear and discoverable
- the lesson is a research result rather than a workflow rule
- the proposed rule would encode a private project fact in public infrastructure
- added complexity would outweigh the likely benefit
- evidence is too weak and the user has not endorsed the preference

Explain the disposition briefly; do not invent a target merely to produce an action item.

## Dual-Layer Proposals

Some lessons justify both scopes. For example:

- Public: EmpiricalOps recommends squash merge for exploratory branches.
- Local: a project specifies `dev` as the target branch and documents its writing-submodule sequence.

Create separate proposal entries. The public rule must not contain the local branch names or repository-specific sequence.

## Publication Gate

Before routing anything to the public repository, remove or abstract:

- credentials and authentication details
- licensed, confidential, or embargoed data
- unpublished estimates not needed to explain the workflow
- machine-specific absolute paths
- personal identifiers unless the user explicitly wants that identity published

Public EmpiricalOps may encode the owner's preferences, but publication is not permission to expose sensitive content.
