---
name: table-sources-maintainer
description: Maintain a research repo's figure/table source map from manuscript draft assets to LaTeX labels, repo sources, and owners. Use when updating or auditing files such as TABLE_SOURCES.md, tracing manuscript figures/tables, deciding whether to list filenames or full paths, splitting multi-panel table rows, linking manuscript commit hashes, or assigning owners from git history.
---

# Table Sources Maintainer

## Goal

Produce or update a source map that lets a future reader answer, for every manuscript figure/table: what draft asset is used, what LaTeX label refers to it, what repo file regenerates or explains it, who first introduced the paper-facing asset, and which open issues still track related work.

Use `assets/TABLE_SOURCES.template.md` when creating a new file or when an existing source map needs normalization.
Source maps should use front matter with `managed_by: table-sources-maintainer`, a plain-URL `maintainer_commit` value for the skill version used to maintain the file, and protected fields matching this skill's confirmation rules.
Leave `maintainer_commit` empty until the maintainer skill is pinned to a committed revision.

## Canonical Source

- Source of truth: `https://github.com/xisun0/EmpiricalOps/tree/main/skills/table-sources-maintainer`.
- Repo-local copies may live under `.agents/skills/table-sources-maintainer`; before changing maintainer rules, check the source-of-truth repository above.
- When filling `maintainer_commit` for a copied skill, use a pinned full-commit URL under the same EmpiricalOps skill path, not the downstream repo copy.

## Front Matter

- `managed_by` must be `table-sources-maintainer`.
- `maintainer_commit` records the Git commit for the maintainer skill version used in the latest maintenance pass.
  Write it as a plain URL that points to the maintainer skill folder at the full commit hash, for example `https://github.com/<owner>/<repo>/tree/<full_hash>/skills/table-sources-maintainer`.
  Do not use markdown-link syntax in front matter because YAML metadata parsers may reject or misread it.
  This is the commit that defines the skill instructions, not the manuscript commit and not the source-map file commit.
- If the skill is copied from a central operations repo, link to that central repo's skill folder at the pinned commit.
  If the current skill has uncommitted edits or no pinned upstream commit, leave `maintainer_commit` empty and say so in the final response.
- `protected_fields` must include fields that require human confirmation before changing.

## Execution Workflow

1. Locate the active manuscript.
   Prefer the file named by the user. Otherwise inspect repo docs, the existing source map, recently edited manuscript files, and common manuscript directories such as `writing/`, `paper/`, `manuscript/`, or `draft/`.
   Treat existing source-map `Draft:`, `Main source:`, and `Appendix source:` lines as the locked active-source mapping unless the user explicitly names a different source or repo documentation clearly marks another file as active.
   Do not add, remove, split, or switch manuscript source files solely because another `.tex` file is newer, standalone, more complete, or contains additional tables/figures.
   If a plausible alternative source is found, preserve the existing source mapping, record the ambiguity in `To Be Confirmed`, and ask for confirmation before remapping.
2. Identify the git repo that owns the manuscript assets.
   If the manuscript directory is a submodule, run commit and history commands inside that submodule.
3. Record the manuscript source at the top of the source map.
   Update the `Updated:` line to the current maintenance date and keep the date bolded.
   Use a short displayed hash linked to the remote blob URL for the main source tex file at the full commit hash.
   If one source file contains both main and appendix artifacts, use one `Draft:` line and state that this draft contains both main and appendix figures/tables.
   If main tables/figures and appendix tables/figures come from separate source files, define both `Main source` and `Appendix source` at the top.
4. Extract figures and tables from the manuscript in order.
   Use separate `Main Figures and Tables` and `Appendix Figures and Tables` sections by default.
   Omit the appendix section only when the manuscript has no appendix figures or tables.
5. Fill one row per artifact or per panel, using the column rules below.
6. Verify duplicate draft-asset filenames before shortening paths.
7. Before changing any existing `owner` or `related open issues` value, including `TBD` or `-`, get explicit human confirmation.
   Add or correct other cells directly when the evidence is clear, preserve any manual owner correction from the user, and preserve issue-link decisions unless the user confirms a change.
8. Add or update a `To Be Confirmed` section for unresolved source-map risks that need human review.
   Use it for ambiguity that affects interpretation or maintenance, such as unresolved generators, inlined/manual tables with unclear ownership, missing active labels, or source chains that look plausible but are not verified.
   Do not use it to duplicate every routine `TBD` cell.
9. Keep `Notes` as the final section of the source map.
10. Fill `maintainer_commit` only when the maintainer skill version is pinned to a committed revision.
    Use a plain URL to the maintainer skill folder at that commit; otherwise leave it empty.
11. Run `git diff --check -- <source-map-file>` after edits.
    Do not compile LaTeX unless manuscript LaTeX sources or assets changed.

## Required Columns

Use these columns unless the existing repo has a better established naming convention:

```md
| No. | LaTeX label | draft asset | repo source | owner | related open issues |
|---|---|---|---|---|---|
```

## Column Rules

### No.

- Follow the manuscript numbering and order.
- Use panel rows when separate source assets are used, for example `Table 7 Panel A` and `Table 7 Panel B`.
- Preserve the repo's appendix naming style, such as `Appendix Table A1`, `IA Table 1`, or `Figure A1`.

### draft asset

- Record the core figure or table file used by the current manuscript draft.
- For figures, list the actual image file included in the draft, such as `.png` or `.pdf`.
  Do not list wrapper `.tex` files whose only role is to insert an image.
- For tables, list the paper-facing manuscript table fragment, usually a `.tex` file.
- For inlined tables, write `inlined in manuscript source` when one source contains both main and appendix artifacts.
  If main and appendix are separate sources, write `inlined in main source` or `inlined in appendix source`.
  Inline status only describes how the table appears in the manuscript; it does not imply that the repo source is unknown.
- For readability, write only filenames in this column after checking for duplicate basenames.
- If any draft-asset basename is duplicated, keep the full path for the duplicated filename and tell the user which basename was duplicated.
- If one figure number contains multiple substantive image assets, keep one row only when the manuscript treats them as one combined figure; otherwise split into panel rows.

### LaTeX label

- Record the active manuscript label, such as `fig:<label>` or `tab:<label>`.
- If a wrapper label and panel labels both matter, keep them in one cell, for example `tab:<wrapper>` (`tab:<panel_a>`).
- If no active label exists, write `no active label`.

### repo source

- Record the repo file that can reproduce or explain the draft asset.
- Apply the same rule to figures and tables.
- If the maintained repo source artifact has the same basename as the draft asset, do not repeat the artifact path in `repo source`.
  Write the generator directly when known, for example `code/.../script.do`.
- If the maintained repo source artifact has a different basename from the draft asset, write the source artifact followed by the generator when known, for example `code/.../source_table.tex`, generated by `code/.../script.do`.
- If the same-basename source directory is known but the generator is unknown, write `same filename in code/.../; generator TBD`.
- If no source artifact exists, list the generating script when known.
- For inlined tables, search for a code-side source artifact before writing `source not yet located`.
  Derive candidate filenames from the LaTeX label by stripping the prefix, for example `tab:CN_2digit_favind_ols` -> `CN_2digit_favind_ols.tex`, and also try common numeric prefixes such as `2_CN_2digit_favind_ols.tex`.
  Search repo code/output directories for those filenames and for likely generator calls.
  If the inlined table contains multiple panels with separate code-side artifacts, split the source map into panel rows even though the manuscript block is inlined.
- For manual tables or screenshots, say so directly, for example `manual table in manuscript; no separate source file`.
- Use `TBD` when neither source nor generator is clear.

### owner

- `owner` is the first git author who added the paper-facing manuscript asset.
- For image figures, use the core image asset, not a wrapper tex.
- For table fragments, use the paper-facing table fragment.
- For inlined manuscript tables, use the first author who added the relevant manuscript block when known.
- Do not substitute the code-side generator author unless the user explicitly asks for code owner.
- If the user provides an explicit owner correction, preserve that manual owner and do not overwrite it from git history.
- Use `TBD` when ownership cannot be assigned cleanly from git history.

Run this from the repo that owns the paper-facing asset:

```bash
git -C <asset-repo-or-submodule> log --follow --diff-filter=A --format='%ad\t%an\t%H' --date=short -- <path-inside-that-repo>
```

### related open issues

- Record currently open issue links that directly track the artifact, its data source, specification, generator, or unresolved validation question.
- Use issue links, for example `[#107](https://github.com/<owner>/<repo>/issues/107)`.
- Use `-` when no clearly related open issue exists.
- Do not attach broad or weakly related issues just to fill the cell.
- If issue lookup fails, fill only issues already known from local context and tell the user that the column is incomplete.

## Checks

Before finishing:

- Confirm every row has the required columns.
- Confirm manuscript source mapping was not changed from existing `Draft:`, `Main source:`, or `Appendix source:` lines without explicit user direction, clear repo documentation, or a recorded confirmation.
- Confirm every listed draft asset exists, or is explicitly marked as inlined.
- Confirm draft-asset filenames were shortened only after checking duplicate basenames.
- Confirm figure rows list core image assets, not wrapper tex files.
- Confirm multi-panel tables with separate table fragments are split into panel rows.
- Confirm inlined tables were still searched for code-side source artifacts using label-derived filenames and generator references.
- Confirm `repo source` follows the unified same-basename rule for figures and tables.
- Confirm owner attribution comes from paper-facing asset history.
- Confirm related open issues are open and directly related, or use `-`.
- Confirm every changed existing `owner` or `related open issues` value, including `TBD` or `-`, was explicitly confirmed by the user.
- Confirm the `To Be Confirmed` section records the remaining high-risk ambiguities without duplicating every routine `TBD` cell.
- Confirm `Notes` is the final section.
- Run `git diff --check -- <source-map-file>`.

## Completion Response

When finishing a source-map update or audit, include the current `To Be Confirmed` items in the final response.
If the section is empty, say that there are no current `To Be Confirmed` items.
Keep the list concise, but do not omit items that remain in the source map.
Also state whether `maintainer_commit` was filled or intentionally left empty.
If filled, state which repo and folder the URL points to.
