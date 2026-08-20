---
name: table-sources-maintainer
description: Build, audit, reconcile, and update a research repo's figure/table source map from the active manuscript to paper-facing assets, LaTeX labels, code-side outputs, generators, owners, and open issues. Use for TABLE_SOURCES.md maintenance, full manuscript-to-source reconciliation, targeted source tracing, panel splitting, stale-row detection, manuscript commit links, and ownership attribution.
---

# Table Sources Maintainer

## Goal

Maintain a complete source map for every active manuscript figure and table. The active manuscript is the factual source for the artifact universe; an existing source map is prior state to reconcile, not an inventory to trust.

Use `assets/TABLE_SOURCES.template.md` when creating or normalizing a source map. Use the bundled scripts to rebuild the manuscript inventory and compare it with the existing map before making judgments.

## Canonical Source

- Source of truth: `https://github.com/xisun0/EmpiricalOps/tree/main/skills/table-sources-maintainer`.
- Repo-local copies may live under `.agents/skills/table-sources-maintainer`; inspect the canonical copy before changing maintainer rules.
- Keep `maintainer_commit` empty while the skill has uncommitted edits or no pinned upstream revision. Once pinned, use a plain full-commit URL to the canonical skill folder.

## Modes

Choose scope and mutation independently.

### Scope

- `full-reconcile`: default for requests to audit, maintain, refresh, synchronize, or check the current source map. Rebuild the complete active artifact inventory and revalidate every active row.
- `targeted-update`: use only when the user explicitly limits work to named artifacts. Still rebuild the complete inventory and report drift outside the target; only deep-trace and edit the named rows.
- `bootstrap`: use when no source map exists.

### Mutation

- `audit-only`: report findings without editing.
- `update`: edit the source map. Do not edit manuscript assets or replication code unless separately requested.

### Defaults

- Scope defaults to `full-reconcile`. Use `targeted-update` only when the user explicitly limits the work to named artifacts, and use `bootstrap` only when no source map exists.
- Mutation defaults to `audit-only` for requests to audit, check, inspect, or review a source map.
- Mutation defaults to `update` for requests to maintain, update, refresh, synchronize, reconcile, create, or fix a source map.
- An explicit user instruction overrides these defaults. Record both dimensions as `<scope> + <mutation>`.

## Required Workflow

1. **Lock the active manuscript path.**
   Prefer the user's named file, then explicit repo documentation, then the existing map. Preserve an existing `Draft:`, `Main source:`, or `Appendix source:` selection unless the user or clear repo documentation identifies a replacement. Locking the source path does not lock the existing artifact rows.

2. **Identify ownership boundaries.**
   Determine which Git repo or submodule owns the manuscript and paper-facing assets. Run history commands in that repo.

3. **Rebuild a fresh artifact inventory.**
   Run:

   ```bash
   python3 .agents/skills/table-sources-maintainer/scripts/inventory_manuscript_artifacts.py \
     --manuscript <active.tex> --aux <active.aux> --output <inventory.json>
   ```

   Derive the inventory independently of `TABLE_SOURCES.md`. Include active table and figure environments in manuscript order, main/appendix location, labels, captions, direct and wrapper-based table inputs, figure assets, inline bodies, continued floats, and source lines. Exclude commented-out material. Treat unresolved macros or inputs as audit blockers, not as absent artifacts.

4. **Run a bidirectional reconciliation.**
   Run:

   ```bash
   python3 .agents/skills/table-sources-maintainer/scripts/reconcile_source_map.py \
     --inventory <inventory.json> --source-map <TABLE_SOURCES.md>
   ```

   Classify every difference as `missing_from_map`, `stale_in_map`, `mapping_changed`, or `unchanged`. Check labels and active draft-asset usages in both directions.

5. **Normalize logical artifacts and panels.**
   Follow manuscript numbering from the current `.aux` when available. Merge continued floats into the same logical table. Split a table or figure into panel rows when separate substantive assets or generators need separate tracing. Preserve wrapper and panel labels together when both matter.

6. **Trace every active source chain.**
   Trace `manuscript wrapper -> draft asset -> code-side output -> generator`. Search label-derived filenames, exact asset basenames, generator output statements, nearby run scripts, and source-map documentation. Classify each chain as:
   - `verified`: exact active asset and generator/output link found;
   - `manual`: intentionally assembled or maintained by hand, with inputs stated;
   - `candidate`: plausible source found but exact generation link not established;
   - `unresolved`: no defensible source chain.

   Do not present `candidate` as verified. Put material candidate or unresolved chains in `To Be Confirmed`.

7. **Reconcile protected fields by artifact identity.**
   Match rows by active label and draft asset, not old row number. Preserve existing `owner` and `related open issues` values when an artifact is renumbered, moved, or split. Before changing an existing active artifact's protected value, including `TBD` or `-`, obtain explicit human confirmation. Removing a row proven inactive is not a protected-field edit; report the removal. For new rows, fill protected fields only from clear evidence, otherwise use `TBD` or `-`.

8. **Update map metadata and sections.**
   Record the current manuscript commit, current date, scope and mutation mode, and coverage counts. Keep separate main and appendix sections when both exist. Keep `Notes` last. Number every `To Be Confirmed` item.

9. **Apply the completion gate.**
   Do not report a full reconciliation as complete unless:
   - every active top-level table and figure label is mapped;
   - every active draft asset usage is mapped or explicitly represented by an inline/manual row;
   - no stale row remains without an explicit reason;
   - every row has all required columns and a source-chain classification, including unresolved;
   - coverage counts equal the fresh inventory after continued-float and panel normalization;
   - all remaining ambiguities appear in `To Be Confirmed`.

10. **Validate the edit.**
    Re-run reconciliation until it reports no missing or stale labels/assets. Run `git diff --check -- <source-map-file>`. Do not compile LaTeX unless manuscript LaTeX or assets changed.

## Required Columns

```md
| No. | LaTeX label | draft asset | repo source | owner | related open issues |
|---|---|---|---|---|---|
```

Use an established equivalent only when the repository already has one.

## Column Rules

### No.

- Follow current manuscript numbering and order.
- Preserve the manuscript's appendix naming style.
- Use panel rows when separate substantive assets or source chains are used.

### LaTeX label

- Record active labels only.
- Keep wrapper and panel labels in one cell when both identify the artifact.
- Write `no active label` only when an active environment genuinely lacks a label.

### draft asset

- For figures, record actual included image assets, not wrapper files.
- For tables, record active paper-facing table fragments.
- For inline tables, write `inlined in manuscript source`, `inlined in main source`, or `inlined in appendix source`.
- Use filenames only after checking duplicate basenames. Retain paths for duplicated basenames.

### repo source

- Record the code-side output and generator when their basename differs from the draft asset.
- When an exact same-basename code-side output is verified, list the generator directly.
- For manually assembled assets, name component outputs and the formatter or assembly step.
- Prefix an unverified but plausible chain with `candidate:` and add it to `To Be Confirmed`.
- Use `TBD` when no defensible source or generator is found.

### owner

- Owner is the first Git author who added the paper-facing asset, not the generator author.
- For inline artifacts, use the first author of the manuscript block when recoverable.
- Preserve explicit human corrections.
- Use:

  ```bash
  git -C <asset-repo-or-submodule> log --follow --diff-filter=A \
    --format='%ad\t%an\t%H' --date=short -- <asset-path>
  ```

### related open issues

- Include only currently open issues directly tied to the artifact, source, specification, or unresolved validation.
- Use `-` when no clearly related open issue is known.
- If issue lookup is unavailable, preserve existing values and report that verification is incomplete.

## Front Matter

- `managed_by` must be `table-sources-maintainer`.
- `maintainer_commit` must be a plain URL to the canonical skill folder at a full commit hash, or empty when the skill is unpinned.
- `protected_fields` must include `owner` and `related open issues` unless the repository explicitly defines different protected fields.

## Completion Response

Report mode, active manuscript commit, fresh inventory counts, reconciliation result, changed rows, source-chain status, all numbered `To Be Confirmed` items, `maintainer_commit` status, and validation results.
