---
name: consistency-auditor
description: Audit and fix consistency problems in empirical paper drafts, especially LaTeX manuscripts with generated tables and figures. Use for substantive consistency between manuscript statements and replication code, and for style consistency in notation, definitions, table notes, sample-period wording, table headers, refs, and figure/table source checks.
---

# Consistency Auditor

## Goal

Find and, when asked, fix consistency problems in empirical paper drafts.

The audit has two complementary passes:

- **Substantive consistency matrix**: for each paper-facing artifact or empirical claim, check whether reporting items such as sample period, filters, data source, transformations, units, winsorization, fixed effects, standard errors, clustering, and magnitudes match the replication code or generated outputs.
- **Variable consistency matrix**: for each recurring variable or construct, check whether notation, labels, definitions, transformations, units, data source wording, and table-note usage are consistent across the manuscript, tables, figures, notation files, and variable-definition files.

This skill can inspect code and generated artifacts to verify claims. It is not a substitute for regenerating empirical outputs unless the user explicitly asks to rerun code.

## Default Workflow

1. Locate the active manuscript.
   Prefer the file named by the user. Otherwise inspect repo docs, recent writing files, and common locations such as `writing/`, `Draft/`, `paper/`, or `manuscript/`.
   If the manuscript lives in a submodule, run Git and compile checks inside the submodule that owns the manuscript files.

2. Identify paper-facing artifacts.
   Extract active `\input{...}`, `\includegraphics{...}`, `\label{...}`, `\ref{...}`, and `\autoref{...}` entries from the active manuscript.
   Also inspect locally defined input wrappers such as `\newcommand{\drafttableinput}[1]{...}` and treat calls to those wrappers as active table inputs.
   For every active table wrapper, classify the table body as `external` (an imported fragment) or `inline` (a `tabular`, `tablenotes`, or equivalent body written in the manuscript file).
   Check only tables and figures used in the current paper unless the user asks for appendix-wide or repo-wide coverage.

3. Build the artifact universe.
   For each used table or figure, record:
   - manuscript label
   - paper-facing asset path
   - caption or table title
   - table or figure note
   - table-rule style and table-body formatting when the artifact is a table
   - table body and note font-size conventions when the artifact is a table
   - table source structure: inline body or external fragment
   - stated sample period
   - key variables and units
   - source code or source output path when discoverable
   Include major empirical text claims when they cite a table, figure, coefficient, sample, or specification.

4. Build a display-variable inventory before auditing definitions.
   For every active table and figure, extract all reader-visible variable candidates from table stub rows, outcome headers, panel labels, column headers, axis labels, legends, captions, and table notes. Include plain-text labels as well as \texttt{}, math-mode symbols, and code-like tokens. Include labels emitted by stargazer, esttab, outreg2, or plotting code. Exclude structural labels such as Observations, R-squared, Controls, and fixed-effect rows, but do not exclude a label merely because it is an ordinary English word, appears only in summary statistics, or is not typeset as code. For each candidate, record its artifact and display location.

5. Resolve every display variable to a variable family.
   For each inventory item, search the corresponding generation code and definitions for its code variable or expression, display-label aliases, raw level, transformed form, summary-statistic form, unit, denominator, currency, display scaling, data source, timing, and aggregation level. Create one family row for semantically related variants, but do not collapse distinct variants. For example, tot_assets, Assets, Assets100M, and log(Assets) belong to one total-assets family while remaining distinct entries: raw assets, raw assets displayed in RMB 100 million, and logged assets. A family is incomplete if a visible member has no defined unit or no evidence linking it to the code expression.

6. Build and fill the substantive consistency matrix.
   Do not trust paper-facing statements by default when source code is available.
   Use one row per table, figure, panel, or empirical text claim, and one column per reporting item.
   Standard columns:
   - sample period
   - sample filters
   - data source
   - dependent variable
   - controls or key variables
   - transformations and units
   - winsorization or trimming
   - fixed effects
   - standard errors and clustering
   - significance notation and table-body footers
   - table-rule style
   - table and table-note font style
   - signs, magnitudes, or coefficient statements
   - table, figure, panel, and hypothesis references
   Each cell should record the paper-facing wording, source-code evidence, and status: `verified`, `mismatch`, `missing`, or `unresolved`.

7. Build and fill the variable consistency matrix.
   Use one row per recurring variable, construct, index, score, ratio, premium, spread, or transformed outcome.
   Collect variable appearances from prose, equations, captions, table headers, table bodies, table notes, figure notes, legends, centralized notation files, and variable-definition tables.
   Build this appearance set from the active source graph, including resolved direct inputs and input-wrapper calls. Exclude commented-out LaTeX from findings, but report stale commented notation separately when it could be accidentally reactivated.
   Standard columns:
   - code variable or expression
   - display label and all aliases
   - artifact and display location
   - raw, transformed, and summary-statistic variants
   - text label
   - centralized definition
   - table-note definition
   - transformation
   - unit or scale
   - data source or construction
   - side-by-side conflicts with related measures
   - whether every visible variant is defined locally or centrally
   Each cell should record observed variants and the recommended canonical form.

   Apply a coverage gate before closing this pass: every non-structural display variable in the inventory must be marked defined and retained, replace with natural language, undefined, or inactive. Do not report a variable audit as complete if any visible table or figure label has no family row and disposition.

8. Audit table-note completeness.
   For each paper-facing table, check whether the note states the reporting items required to interpret and replicate the table: sample period, variable definitions, transformations, units, fixed effects, standard-error clustering, winsorization or trimming, and source-specific caveats.
   Also check whether significance-star and p-value explanations appear exactly once, in the final sentence of the table note, and do not appear inside the generated table body.

9. Check references and compile logs.
   Compile after LaTeX edits when feasible.
   Search logs for undefined references, undefined citations, missing files, and overfull boxes caused by edited labels.
   Separate hard build failures from existing warnings.

10. Report or patch.
   For an audit request, return findings first, ordered by severity.
   For a fix request, make narrow LaTeX/table edits and verify with compile or a clearly stated fallback.

## General Rules

- Treat paper-facing empirical wording as a claim to verify against source code or generated output when available.
- Audit substantive items horizontally across all artifacts, then audit notation and definitions vertically by variable.
- Do not guess. Mark unsupported items as `unresolved`, and report code-paper mismatches before editing.

## Substantive Checklist Items

Use these items as columns in the substantive consistency matrix. For each item, check every paper-facing table, figure, panel, and empirical text claim that uses it.

### Sample Period

Check:
- Whether the note, caption, or text states a sample window.
- Whether the stated start and end years match code filters, input data coverage, output filenames, and estimation-sample summaries.
- Whether the window is calendar year, fiscal year, event time, post-event horizon, or rolling window.
- Whether panels or columns use different windows.
- Whether missing-control, merge, or nonmissing-outcome restrictions shorten the effective sample.

Common mismatches:
- The paper states the data coverage window instead of the regression sample.
- A generated table uses a different sample after dropping missing controls.
- One panel has an updated period but the wrapper note still uses the old period.

### Sample Filters

Check:
- Inclusion and exclusion rules: country, market, exchange, industry, firm type, security type, event type, treated/control sample, and matched sample.
- Whether filters are applied before or after merges, winsorization, or aggregation.
- Whether the paper describes the estimation sample or a broader source universe.
- Whether each panel, outcome, or robustness column uses the same filters.

Common mismatches:
- A table note omits an exchange, listing-status, or industry exclusion used in code.
- The paper describes the raw sample while code estimates on a balanced, matched, or nonmissing subset.

### Data Source and Vintage

Check:
- Dataset, database, corpus, exchange, regulator, survey, or vendor named in the paper.
- Data vintage, release, snapshot date, or version when it affects interpretation.
- Merge keys and source hierarchy when a variable can come from more than one source.
- Currency, accounting standard, market venue, or text corpus used to construct a measure.

Common mismatches:
- A note names the final merged dataset but not the source defining the key measure.
- The code uses a newer data vintage than the manuscript says.
- A variable switches source across settings but the table note does not say which source is used.

### Dependent Variable

Check:
- Outcome definition, timing, aggregation level, and denominator.
- Whether the outcome is a level, indicator, count, amount, ratio, spread, return, premium, index, or score.
- Whether zero handling, offsets, event windows, cumulative windows, or annualization match the label.
- Whether table headers and text refer to the same outcome as the code.

Common mismatches:
- Header says a raw outcome but code uses `log(1+outcome)`.
- Text describes a count while code uses an indicator.
- The denominator or timing is omitted from the note.

### Controls and Key Variables

Check:
- Which controls appear in the code and whether the table note or variable definitions name them correctly.
- Variable timing: contemporaneous, lagged, baseline, pre-event, post-event, or averaged.
- Whether controls are levels, logs, ratios, standardized measures, or indicators.
- Whether key independent variables are measured at firm, industry, region, market, or time level.

Common mismatches:
- Paper uses one label for both a firm-level variable and an industry-level aggregate.
- A table note lists controls that are not in the final specification.
- A lag or baseline year is missing from the definition.

### Transformations and Units

Check:
- Logs, inverse hyperbolic sine, standardization, demeaning, residualization, winsorized values, and index normalization.
- Whether logs are natural logs and whether offsets such as `log(1+x)` are explicit.
- Units: dollars, local currency, millions, percentages, percentage points, basis points, shares, ratios, or index points.
- Currency conversions, inflation adjustment, exchange rates, and real versus nominal values.
- Whether arbitrary display scaling is mentioned only when needed for interpretation.

Common mismatches:
- Table reports coefficients on a transformed variable but the note defines the raw variable.
- Percent and percentage-point language are mixed.
- Units differ across text, table header, and note.

### Winsorization or Trimming

Check:
- Whether variables are winsorized, trimmed, capped, filtered, or left raw.
- Thresholds, such as 1/99, 5/95, or top-tail exclusions.
- Whether treatment is global, by year, by industry, by market, or by panel.
- Whether it happens before or after transformations, aggregation, or regression-sample restrictions.
- Whether the rule applies to all variables or only named variables.

Common mismatches:
- A generic note says all variables are winsorized but code winsorizes only controls.
- The note states 1/99 while code uses 5/95 or trims rather than caps.
- The code drops an extreme tail but the paper calls it winsorization.

### Fixed Effects

Check:
- Exact fixed-effect dimensions and interactions: year, firm, industry, region, market, cohort, event time, industry-year, firm-year, and similar.
- Whether fixed effects are absorbed, included as dummies, or differ across columns.
- Whether a table note states all fixed effects used in each panel or column.
- Whether the reported identifying variation is consistent with the fixed effects.

Common mismatches:
- Note says year and industry fixed effects, but code absorbs industry-year fixed effects.
- Some columns omit a fixed effect but the common note implies all columns include it.
- Text claims within-firm variation while code does not include firm fixed effects.

### Standard Errors and Clustering

Check:
- Robust, heteroskedasticity-robust, bootstrap, Newey-West, Driscoll-Kraay, randomization inference, or clustered standard errors.
- Cluster dimensions and whether they are one-way, two-way, multi-way, or nested.
- Whether clustering changes across panels, columns, outcomes, or robustness tables.
- Whether code uses small-sample corrections or special variance estimators that the paper should disclose.
- For every regression table with significance stars, whether the standard-error sentence is the penultimate reader-facing sentence of the table note, immediately before the final significance explanation. Move cross-references, variable definitions, sample qualifications, and winsorization statements before it.
- For a regression table without a significance explanation, whether the standard-error sentence is the final reader-facing sentence of the table note.
- Whether the standard-error sentence explicitly states the estimator and clustering dimensions used by code, rather than referring generically to another table.

Common mismatches:
- Table note says robust standard errors but code clusters by firm or industry-year.
- Two-way clustering in code is described as one-way clustering.
- Appendix and main tables use different SE rules without explanation.
- A table note inserts a summary-statistics cross-reference, a winsorization rule, or an R-squared explanation after the standard-error sentence, so the note's final two sentences do not read as standard errors followed by significance notation.

### Significance Notation and Table Footers

Check:
- Whether the significance-star explanation appears only in the table note, not in the table body or generated fragment.
- Whether the significance explanation is the final sentence of the table note.
- Whether all tables with displayed stars have a significance explanation, including descriptive-difference and t-test tables.
- Whether tables without stars avoid unnecessary p-value language.
- Whether the wording is consistent across main-text and appendix tables.
- Whether generated fragments contain redundant footer rows such as `Robust standard errors in parentheses` or `*** p<0.01, ** p<0.05, * p<0.1`.

Recommended default wording:
`$^{***}$, $^{**}$, and $^{*}$ denote significance at the 1\%, 5\%, and 10\% levels, respectively.`

Common mismatches:
- A wrapper note has the canonical sentence, but the generated table body also contains a robust-SE or p-value footer.
- The p-value sentence appears before variable definitions or sample construction details.
- Main tables use superscript notation while appendix tables use plain stars or `p<` cutoffs.
- A table has stars in coefficient or difference cells but no table-note explanation.

### Table Rule Style

Check:
- First infer the paper's canonical table-rule style from active tables, journal/template instructions, local writing guidelines, or explicit user preference.
- Whether all paper-facing tables follow that inferred style consistently.
- Whether horizontal-rule commands mix incompatible conventions across similar tables, such as `booktabs` rules in most tables but `\hline\hline` in generated summary-statistics fragments.
- Whether rule placement is coherent: avoid adjacent full-width rules with no header or data row between them, and avoid rule commands carrying generator spacing artifacts such as `\midrule \\[-1.8ex]`.
- Whether partial header rules follow the same convention as full-width rules, such as `\cmidrule` under `booktabs` or `\cline` under plain LaTeX rules.
- Whether `tabular` or `tabular*` column specifications use vertical rules, and whether that matches the inferred style.
- Whether table wrappers and generated fragments conflict, for example a wrapper follows one style while the input fragment adds another.
- Whether discovery includes direct `\input{...}` calls and project-defined wrapper macros such as `\drafttableinput{...}`.

Recommended process:
- State the inferred style before patching: e.g., "active tables use `booktabs`: `\toprule`, `\midrule`, `\bottomrule`, `\cmidrule`; vertical rules are absent."
- Treat the inferred style as the audit standard for that manuscript.
- Patch deviations toward the inferred style only when the convention is clear or the user has specified it.

Common mismatches:
- A scan reports no deviations because it follows only direct `\input{...}` and misses wrapper calls such as `\drafttableinput{...}`.
- Appendix summary-stat tables keep a different line convention from otherwise similar main-text or appendix tables.
- A generated table uses one horizontal-rule convention but retains vertical separators or partial rules from another convention.
- A generated summary-stat table has `\toprule` immediately followed by `\midrule`, or uses `\midrule \\[-1.8ex]` / `\bottomrule \\[-1.8ex]`.

### Table Source Structure

Check:
- Build an inventory of every active table wrapper and classify its body as inline or external, resolving direct `\input{...}` calls and project-defined input wrappers.
- Infer whether comparable tables follow a dominant source structure. Inline and external table bodies are not inherently inconsistent, but a mixed pattern among comparable main-text or appendix tables should be reported.
- When the manuscript's convention is wrapper plus external fragment, move each remaining inline `tabular` or equivalent table body to a dedicated table file. Retain the float placement, caption, label, centering, panel headings, width controls, document-level font switch, and the full `tablenotes` block in the manuscript wrapper.
- Verify that the extracted fragment is resolved through the manuscript's existing input path and produces the same rendered table, while panel headings, width settings, and notes remain correctly attached to the wrapper.

Common mismatches:
- Most appendix tables use external table bodies, but a few comparable appendix tables keep their body inline in the main draft.
- Extracting a table moves its caption or label into the fragment, making references and float placement harder to audit.
- Extracting a table moves its `tablenotes` block out of the manuscript wrapper, separating the note from the caption and surrounding text.
- An audit follows only imported fragments and therefore misses inline table bodies.

### Table and Table-Note Font Style

Check:
- First infer the manuscript's table font convention from active tables and local style guidance.
- Exclude commented-out table environments and inactive fragments before counting. A historical table retained behind line comments is not evidence of the active manuscript's style.
- Build a per-active-table body-font inventory. Identify the effective size switch before the table body and stop the scan at `tablenotes` or an inline `Notes:` paragraph; do not attribute a later note-level `\scriptsize` to the body.
- Record `\resizebox`, `\scalebox`, or similar wrappers separately. They change the rendered size but do not replace the source-font convention, so report both the source size and whether final size is scaling-controlled.
- Whether table body sizes are applied intentionally and consistently across comparable tables, such as regression tables versus summary-statistics tables.
- Whether all table notes use the same font size convention, including `tablenotes` environments and inline `Notes:` paragraphs.
- Whether stray font-size switches such as a bare `\small` after `\end{tablenotes}` affect following content or indicate a missing table note.
- Whether standalone appendix files and the main draft version of the same appendix table use the same note font and note structure.

Recommended process:
- State the inferred convention and the inventory before patching, such as "all active table notes use `\scriptsize`; 24 table bodies use `\scriptsize`, while six use `\small`."
- When a dominant body convention is clear, standardize source body sizes to it unless a named table needs a justified exception. Preserve width controls and then compile to verify that the resulting layout remains usable.
- Treat inline `\small\textit{Notes:}` or missing `tablenotes` as deviations when the rest of the manuscript uses `\scriptsize` notes.
- Keep body font changes separate from note font changes unless the user asks for both.

Common mismatches:
- A scan includes a commented-out legacy table and falsely reports an obsolete `\small` or `\footnotesize` style as active.
- A naive scan sees `\scriptsize` inside a later `tablenotes` environment and incorrectly reports that the preceding body is `\scriptsize`.
- A `\resizebox` makes two different source font sizes look similar in the PDF, masking a source-style inconsistency.
- A table body uses `\small`, but the note also inherits `\small` because no note-specific size is set.
- One appendix table has no `tablenotes` block while the corresponding main-draft table has one.
- A note is written as `\small\textit{Notes:}` while all other notes use `\scriptsize`.

### Figure-Note Style

Check:
- Whether figure notes use a figure-appropriate container, such as a `minipage`, rather than a bare `tablenotes` list outside its intended table context.
- Whether all active figure notes share the inferred note width, font size, `Notes:` weight, indentation, and spacing from the caption and graphic.
- Whether a multi-panel figure's note aligns to the intended figure or text block rather than inheriting the width or alignment of a preceding `center` environment.
- Whether the rendered note stays within the figure page boundaries and is visually consistent with the other figure notes.

Recommended process:
- Infer one canonical figure-note pattern from the active figures and apply it to every figure note. Keep table-note and figure-note containers separate even when their type size and `Notes:` label match.
- Render all figure pages after changes; list environments and paragraph alignment can create indentation differences that source scans miss.

Common mismatches:
- One figure uses a full-width `minipage` with italic `Notes:`, while another uses an indented `tablenotes` list with bold `Notes:`.
- A figure note follows a closed `center` environment and becomes left-aligned or adopts an unexpected list indent.

### Panel Headings and Alignment

Check:
- Whether every panel heading is aligned explicitly rather than relying on a preceding `\centering` declaration.
- Whether Panel A and subsequent panels in the same table use the same heading width, alignment, italicization, capitalization, and vertical spacing.
- Whether a heading that follows `\input{...}`, `\drafttableinput{...}`, `tabular`, `tabular*`, `\resizebox`, or `\scalebox` remains centered in the rendered PDF; those constructs can end or scope the preceding paragraph alignment.
- Whether the heading is centered on the table's effective width (`\linewidth` inside a constrained table container), rather than an outer width that creates an overfull box.

Recommended process:
- Use an explicit width-aware construction, such as `\noindent\makebox[\linewidth][c]{\textit{Panel B: ...}}\par`, for standalone panel headings.
- Render every multi-panel table after changing its headings; source inspection alone cannot establish the post-input alignment state.

Common mismatches:
- Panel A is centered because it appears before the first input table, while Panel B reverts to left alignment after the first `tabular*` or imported fragment ends.
- A heading uses `\textwidth` inside a `threeparttable` whose effective width is narrower, producing an overfull box despite an apparently centered PDF result.

### Table Width, Overflow, and Scale

Check:
- Build an inventory of every active table wrapper and its imported fragments, including direct `\input`, project wrapper macros, `tabular*`, `tabularx`, `\resizebox`, `\scalebox`, and landscape environments.
- Whether each table's effective width is bounded by its current container (`\linewidth` inside constrained environments, rather than blindly using `\textwidth`).
- Whether the LaTeX log's `Overfull \\hbox`, `Overfull \\vbox`, and `Float too large` warnings are table-related. Classify each warning rather than treating a clean compile exit as a width check.
- Whether rendered table pages stay within the left and right content boundaries, including landscape pages and tables that follow page-level prose.
- Whether shrink-to-fit controls keep labels, coefficients, headers, and notes legible, and whether paired panels use compatible widths.

Recommended process:
- Audit source structure first, compile, then render every page containing an active table. Inspect both ordinary and widest representatives at readable resolution; source inspection cannot detect clipping or a visually unbalanced scale.
- For every table-related warning, record `resolved`, `acceptable height-only`, or `unresolved`, with the table label and the rendered result.
- Group tables by comparable layout class before standardizing widths: for example, compact single-panel regressions with the same number of coefficient columns, multi-panel regressions, summary-statistics tables, and landscape tables. Use one explicit relative width for each compact class (for example, `0.8\linewidth`) rather than allowing natural-width `tabular` environments to vary with header text.
- Do not force every table to one physical width. Wider tables, multi-panel tables, and descriptive tables may need separate, internally consistent width classes.
- Prefer adjusting columns, header wrapping, or local spacing before scaling. Use `\resizebox` only when it preserves readable output and does not conceal an inconsistent table width.

Common mismatches:
- A `\resizebox{\textwidth}{!}{...}` is placed inside a narrower `threeparttable`, causing a horizontal overfull warning.
- A table fits in source but an imported `tabular*` expands beyond the parent wrapper.
- Comparable three- or four-column regression tables use a mix of natural-width `tabular` and fixed-width `tabular*`, so visually similar tables have inconsistent rule lengths and column spacing.
- A table is technically within the PDF page but extends into the margins or is shrunk enough to be unreadable.
- A warning labelled `Float too large` is a vertical-height issue, not evidence of horizontal width overflow; verify it visually and report it separately.

### Magnitudes, Signs, and Text Claims

Check:
- Coefficient signs, decimal places, percentage interpretations, economic magnitudes, standard-deviation effects, and event-window effects.
- Whether text cites the correct table, panel, column, and row.
- Whether the interpretation matches the transformed dependent and independent variables.
- Whether p-value or star language matches the displayed table if the paper mentions significance.

Common mismatches:
- Text uses an old coefficient after table regeneration.
- A log-point coefficient is described as a level-unit effect.
- The cited column has a different specification from the text claim.

### References, Labels, and Hypothesis Mapping

Check:
- Table, figure, panel, section, appendix, and equation references resolve and point to the intended artifact.
- Captions, titles, and in-text references use the same numbering and hypothesis mapping.
- Placeholder anchors are preserved when required by the repo.
- Compile logs have no new undefined references, undefined citations, missing files, or label conflicts.

Common mismatches:
- Text references a table label that no longer exists.
- A panel title changed but the text still describes the old panel.
- A hypothesis mapping remains from a previous table order.

## Variable Checklist Items

Use these items as columns in the variable consistency matrix. Work variable-by-variable: collect all surface forms before choosing a canonical wording.

### Notation or Symbol

Check:
- Math symbol, acronym, capitalization, hyphenation, subscript, superscript, and roman versus italic style.
- Whether the same notation refers to one concept only.
- Whether distinct constructs need distinct notation when shown side-by-side.

### Text Label

Check:
- How the variable is named in prose, captions, and interpretation sentences.
- Whether first use defines acronyms and later uses are consistent.
- Whether singular/plural and level/ratio/index language match the variable.

### Table and Figure Labels

Check:
- Headers, row labels, panel titles, axis labels, legends, and notes.
- Build the candidate set from every visible label, including plain words such as Assets, Sales, Debt, Size, Cash, Revenue, Employment, Market, or Value; do not limit discovery to acronyms, math symbols, or \texttt{}.
- For each label, identify the matching code expression and any generator-provided alias. Treat a label such as Assets100M as a display-scale claim, not merely a formatting variant.
- Check whether a summary-statistics label is the raw variable, a transformed variable, or a scaled display of the raw variable. It must not silently inherit the definition of a related regression control such as log(Assets).
- Whether labels are readable rather than raw code names.
- Whether long labels fit without forcing awkward layout or overfull boxes.

### Centralized Definition

Check:
- Variable-definition tables, notation files, glossary files, or appendix definitions.
- Whether every visible member of a variable family is defined. A definition for log(Assets) does not, by itself, define a summary-statistics row labelled Assets or Assets (RMB 100 million).
- Whether definitions are broad enough when one concept has multiple valid data sources.
- Whether definitions are precise enough when one label could mean multiple measures.

### Table-Note Definition

Check:
- Whether table-specific definitions identify the exact source, construction, timing, unit, and transformation used in that table.
- Whether the note adds needed context that the centralized definition intentionally leaves broad.
- Whether side-by-side related measures are distinguished clearly.
- Whether notation that first appears in a table note is explained there or in a central definition table.

### Undefined Notation

Check:
- Acronyms, raw variable names, code-style names, transformed variables, ratios, indices, spreads, premiums, and interaction terms that appear anywhere in the manuscript.
- Inline code-style tokens that occur inside math mode or a prose condition, including threshold rules such as `\texttt{n\_emphasize}>0`, `x_{it}=1`, `\mathbb{1}\{\cdot\}`, `Pr(Y>0\mid X)`, or a code-style variable embedded in a log, ratio, or interaction. Treat the full expression and each named variable as notation appearances.
- Indicator-construction rules: check both the economic meaning (for example, ``at least one supportive mention'') and any symbolic threshold used to express it. If the threshold is not needed for interpretation, prefer the natural-language rule in paper-facing prose and table notes; otherwise define the variable and threshold where it appears or in the centralized definition.
- Do not rely on a word-boundary scan alone: LaTeX code names often contain escaped underscores, for example `n\_emphasize`, which a conventional underscore-token pattern will miss. Extract math-mode spans and inspect `\texttt{...}`, `\mathrm{...}`, and escaped-underscore identifiers within them for comparisons, indicators, logs, ratios, interactions, and subscripts.
- Whether each notation is defined at first use, in a central notation or variable-definition table, or in the relevant table/figure note.
- Whether table notes introduce constructs that are not defined elsewhere.
- Whether appendix-only variables are still defined in the appendix note or appendix variable-definition section.
- Whether a table note says a variable is "included" without defining what it measures.

Common mismatches:
- A robustness table note names an extra control but leaves its construction to a later table.
- A generated table body uses raw code names while the table note defines only polished labels.
- A centralized definition exists for the main measure but not for a related appendix-only ratio or index.
- A table note explains an indicator in words but also exposes an otherwise undefined raw construction variable in a parenthetical condition.

Required disposition for every candidate:
- `defined and retained`: the notation is necessary and is defined locally or centrally.
- `replace with natural language`: the notation is an implementation detail that adds no reader-facing content.
- `undefined`: add or repair the definition.
- `inactive`: it occurs only in commented-out material; record it separately, not as an active-paper finding.

### Transformation

Check:
- Whether the variable is raw, logged, standardized, residualized, averaged, lagged, differenced, indexed, or normalized.
- Whether a summary-statistics table displays an untransformed level while regressions use a transformed version; report both members separately and state their relationship.
- Whether the transformation wording matches code and table labels.
- Whether offsets, denominators, windows, and baselines are explicit.

### Unit or Scale

Check:
- Unit of measurement and display scale.
- For every visible numeric row in a descriptive table, verify the denominator or scaling against the code expression. Examples include / 1e8, / 1e6, percent-to-decimal conversions, basis points, and annualization.
- Require that the displayed unit appear in the row label, table note, or an unambiguous centralized definition. A raw code-style suffix such as 100M is not sufficient unless it is defined as a 100-million-RMB scale.
- Whether the same variable is reported in levels in one place and scaled units elsewhere.
- Whether coefficient interpretations use the same unit as the table.

### Data Source or Construction

Check:
- Source dataset, corpus, market, geography, frequency, and construction code.
- Whether the same variable name masks source differences across empirical settings.
- Whether the paper should use a common label with table-specific source notes or distinct labels.

### Related-Measure Conflicts

Check:
- Whether two variables share a label but differ in source, timing, geography, unit, transformation, or aggregation.
- Whether related variables appear side-by-side and need qualifiers.
- Whether the preferred wording is natural-language rather than formula-heavy when the audience needs interpretation more than algebra.

## Common Search Commands

Use `rg` first.

```bash
rg -n "\\\\input|\\\\includegraphics|\\\\label|\\\\ref|\\\\autoref" writing Draft paper manuscript
rg -n "\\\\newcommand\\{\\\\[^}]*input|\\\\[A-Za-z]*tableinput\\{" writing Draft paper manuscript
rg -n "\\\\hline|\\\\cline\\b|\\\\begin\\{tabular\\*?\\}.*\\||\\\\(toprule|midrule|bottomrule) *\\\\\\[-" writing Draft paper manuscript
rg -n "\\\\begin\\{tablenotes\\}|\\\\end\\{tablenotes\\}|\\\\(scriptsize|footnotesize|small)\\\\textit\\{Notes:|\\\\(scriptsize|footnotesize|small) *$" writing Draft paper manuscript
rg -n "\\\\texttt\\{|\\b[A-Z][A-Z0-9_]{1,}\\b|\\b[A-Za-z]+_[A-Za-z0-9_]+\\b" writing Draft paper manuscript
rg -n "^.*&.*\\\\\\\\|^[^%]*\\b(Assets|Sales|Debt|Size|Cash|Revenue|Employment|Market|Value)\\b" writing/Draft/tables writing/Draft/paper
rg -n "\\\\texttt\\{[^}]*\\} *[<>=]|\\b[A-Za-z][A-Za-z0-9_]*_[A-Za-z0-9_]+ *[<>=]|\\\\\\{[^}]*[<>=][^}]*\\\\\\}|\\\\mathbb\\{1\\}|\\\\mathbf\\{1\\}|\\\\mathds\\{1\\}|Pr\\([^)]*[<>=]" writing Draft paper manuscript
rg -n "log\\(|ln\\(|Log\\(|sample period|winsor|cluster|fixed effects|FE|premium|ratio|spread|index|score" writing Draft paper manuscript
rg -n "Robust standard errors|standard errors in parentheses|\\*\\*\\* p|p\\$<|denote significance|denote statistical significance" writing Draft paper manuscript
rg -n "sample|period|year|inrange|keep if|drop if|winsor|cluster|absorb|reghdfe|esttab|outreg" code scripts src
rg -n "covariate.labels|varlabels|labels\\(|row3\\(|plainrow\\(|scale|/ ?1e[0-9]+|log\\(|ln\\(" code scripts src
rg -n "undefined|Citation.*undefined|Reference.*undefined|Missing|Overfull" *.log writing/**/*.log Draft/**/*.log
```

Adapt paths to the repository.

When the manuscript defines wrapper macros for table inputs, use a small parser instead of relying only on `rg`. At minimum, collect active direct inputs and project-defined input-wrapper calls, ignore commented lines, resolve files through the same search paths used by the manuscript, and then scan the resolved files for `\hline`, `\cline`, and vertical-rule column specs.

## Editing Rules

- Preserve explicit editorial anchors such as `[INSERT TABLE \ref{...} HERE]`.
- Make narrow edits to paper-facing files unless the user asks to regenerate empirical outputs.
- If editing generated LaTeX table fragments directly, state that the polish may be overwritten by future code reruns.
- Prefer natural-language table-note definitions when notation would be hard to parse.
- Do not invent sample periods, variable units, source files, fixed effects, or clustering. Mark unresolved items clearly.
- Do not remove unrelated compile warnings, generated artifacts, or untracked files unless the user asks.

## Deliverable Modes

Choose the smallest mode that satisfies the user's request.

### Audit-Only Mode

Use when the user asks to inspect, check, audit, review, or diagnose consistency without explicitly asking for edits.

Do not modify files. Deliver:

```text
Substantive Consistency Matrix
- Artifact/claim x reporting item summary.
- Status values: verified, mismatch, missing, unresolved.
- Evidence: paper-facing wording plus code, output, log, or source-map location where available.

Variable Consistency Matrix
- Variable/construct x surface summary.
- Observed variants across notation, text, table headers, table notes, definitions, and figures.
- Recommended canonical wording.

Findings
- [severity] artifact/claim/variable: issue; evidence; recommended fix.

Unresolved
- Item: what could not be verified; why; where to look next.
```

### Fix Mode

Use when the user asks to fix, revise, harmonize, or apply a known set of consistency changes.

Modify only paper-facing files unless the user explicitly asks to regenerate code outputs. Apply fixes only when the source evidence or style convention is clear. Deliver:

```text
Changed
- Files changed.
- Substantive consistency fixes applied.
- Variable/style consistency fixes applied.

Verified
- Source-code or generated-output checks completed.
- LaTeX compile status when applicable.
- Undefined refs/citations and missing-file checks when applicable.

Remaining
- Unresolved source-code checks.
- Items intentionally not changed because evidence was unclear.
- Generated-table caveats or warnings not caused by this change.
```

### Full Audit Mode

Use when the user asks for a full, systematic, all-table, all-variable, or end-to-end consistency pass.

First produce or internally maintain the two matrices, then patch only verified issues if the user asked for fixes, then verify the manuscript build when applicable. Deliver:

```text
Audit Coverage
- Active manuscript source.
- Tables, figures, panels, and empirical text claims checked.
- Variables or constructs checked.

Resolved
- Mismatches or missing notes fixed, grouped by checklist item.

Matrices
- Compact substantive matrix summary.
- Compact variable matrix summary.

Verified
- Code/output sources checked.
- Compile and reference-check results.

Remaining
- Unresolved items requiring human judgment or missing source evidence.
- Risks from direct edits to generated table fragments.
```
