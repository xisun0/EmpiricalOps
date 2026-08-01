# EmpiricalOps

EmpiricalOps collects reusable agent rules and skills for empirical research repos.

Each skill should be an independently portable package: keep its `SKILL.md`,
`scripts/`, `references/`, `agents/`, and other skill-specific resources inside
that skill's own directory. Do not rely on shared top-level scripts or mixed
resource folders for normal skill operation.

Top-level files such as `manifests/skills.yaml` are for registry and source
tracking only; a skill should remain usable when its folder is copied by itself.
