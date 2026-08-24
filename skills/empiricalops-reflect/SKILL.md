---
name: empiricalops-reflect
description: Turn a completed research or repository session into evidence-based improvement proposals, routing each lesson to the current project, the public owner-oriented EmpiricalOps repository, or no durable change. Use when the user asks to reflect on a workflow, capture reusable preferences, or decide where a correction should be institutionalized. Do not implement proposals without separate authorization.
---

# EmpiricalOps Reflect

Extract durable workflow improvements rather than writing a chronological session summary. EmpiricalOps primarily serves its owner, so stable personal preferences belong in the public EmpiricalOps repository when they can be published safely; they do not need to be universal best practices.

## Workflow

1. State the completed outcome in one sentence.
2. Identify corrections, avoidable rework, repeated preferences, missing defaults, and workflow decisions supported by the session. Exclude ordinary command errors and research findings that do not imply a process change.
3. Inspect the relevant project guidance and EmpiricalOps skills before proposing a new rule. Distinguish a missing or hard-to-find instruction from failure to follow an instruction that already exists.
4. Read [references/routing-rubric.md](references/routing-rubric.md) and route each candidate to `local_project`, `public_empiricalops`, or `no_change`.
5. Apply a publication gate: remove credentials, licensed or confidential data, unpublished project details, private paths, and identifying information that is not itself the approved preference.
6. Prefer the smallest change to an existing skill, reference, template, setup question, or project guidance. Propose a new skill only when the capability is genuinely distinct.
7. Write the proposal using [references/proposal-schema.md](references/proposal-schema.md). Include evidence, root cause, target file or component, patch-level change, why the scope fits, and how future behavior can be checked.
8. Stop after the proposal unless the user separately authorizes edits, issues, commits, pushes, memory updates, or other mutations.

## Routing Principles

- A stable owner preference is sufficient for `public_empiricalops`; do not require proof that it benefits multiple unrelated users.
- Phrase owner-specific public rules as EmpiricalOps defaults or preferences, not universal methodological claims. Preserve project-local override mechanisms.
- A project name, data definition, sample rule, path, branch topology, or artifact-specific decision normally remains local unless an abstract reusable workflow can be separated from it.
- One explicit user correction can establish a preference. A single agent mistake without user endorsement is only a candidate and may result in `no_change`.
- A proposal may have two layers: a public default plus a local project instantiation. Keep their contents and targets separate.
- Do not accumulate defensive rules for every observed failure. If existing guidance is clear, propose better discovery or no change rather than duplicating it.

## Output Boundary

Reflection is read-only by default. It does not itself edit repositories, update personal memory, open issues, install skills, or create commits. When implementation is authorized, use the skill responsible for the target artifact and preserve its workflow and validation requirements.
