# Guided Setup Flow

## 1. Confirm Detected Context

Summarize the repository facts that affect setup:

- empirical code languages and statistical packages
- manuscript and generated-output locations
- default and development branches
- writing repository or submodule arrangement
- existing `AGENTS.md`, `GIT_HYGIENE.md`, source maps, and skill directories
- current Git identity source without displaying credentials

Ask the user to correct only material misclassification.

## 2. Project-Level Questions

Use stable IDs so answers can be reused by multiple skills.

| ID | Question | Behavior |
|---|---|---|
| `install.scope` | Install skills for this project or for the user? | No assumed answer |
| `git.base_branch` | Which branch receives completed work? | Suggest the detected branch |
| `git.merge_strategy` | Default PR merge method? | Recommend `squash`; require confirmation |
| `git.identity.mode` | Inherit Git identity or use a dedicated agent identity? | Default `inherit` |
| `git.identity.name` | Dedicated commit name? | Ask only when mode is `dedicated` |
| `git.identity.email` | Dedicated commit email? | Ask only when mode is `dedicated` |
| `git.commit_style` | Commit subject convention? | Suggest detected convention |
| `writing.mode` | Same repo, submodule, or separate repo? | Prefer detected structure |
| `outputs.exploratory_policy` | Keep exploratory artifacts in target branches? | Recommend PR history or archive only |
| `data.restricted_policy` | Where do licensed, confidential, or large inputs live? | Required before generating data guidance |
| `empirics.default_winsorization` | Default winsorization rule? | Optional; no universal value |
| `empirics.default_clustering` | Default clustering convention? | Optional; do not infer from one table |
| `reflection.activation` | When should session reflection be suggested? | Recommend explicit invocation |
| `reflection.public_repo` | Where should owner-level workflow improvements be proposed? | Recommend the public EmpiricalOps repo |
| `reflection.save_local_reports` | Save reflection proposals automatically? | Recommend `false` |

Do not ask every question mechanically. Skip irrelevant items and reuse confirmed values already stored in the project profile.

## 3. Capability Interview

Ask what the user does, rather than asking them to recognize skill names. Candidate prompts include:

- Do code-generated regression outputs and paper-facing LaTeX tables differ?
- Do figures and tables need generator and manuscript provenance?
- Is systematic paper-code consistency checking needed?
- Are GitHub issues used as empirical decision records?
- Does the project require literature discovery and bibliography integration?
- Are writing and code released through separate repositories?
- Should completed complex workflows produce a scoped improvement proposal?

Map affirmative workflows to catalog capabilities, then present Required, Recommended, and Optional skills with one-sentence reasons.

## 4. Per-Skill Questions

After the user approves the skill plan, read each selected package's `setup.yml`.

1. Topologically order dependencies.
2. Merge questions by stable ID.
3. Fill answers already confirmed at project level.
4. Evaluate conditional questions.
5. Ask remaining questions grouped by skill, normally no more than three at a time.
6. Show the resulting file changes before applying them.

## 5. Completion Receipt

Report:

- detected and confirmed project profile
- installed skills, pinned versions, and scope
- generated or patched files
- declined and deferred recommendations
- validation results and unresolved required decisions

An unresolved required decision is a setup blocker, not permission to insert a sample value.
