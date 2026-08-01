# Git Hygiene

Use this reference when the target repository has no project-local commit scope or Git hygiene guidance.

Before applying these fallback rules, check the target repository root for `GIT_HYGIENE.md`. Use `AGENTS.md`, `CLAUDE.md`, `.commit-scopes.md`, `.commit-message.md`, or similar documents only as compatibility fallbacks. Project-local scope guidance wins over this reference.

## Subject

Use the Angular-style subject:

```text
type(scope): short summary
```

Keep the summary imperative, specific, and under 72 characters when practical.

## Types

- `feat`: user-visible capability or meaningful new workflow
- `fix`: bug fix or correction of broken behavior
- `refactor`: behavior-preserving restructuring
- `docs`: documentation-only change
- `test`: test-only change
- `chore`: tooling, maintenance, configuration, or repository housekeeping
- `style`: formatting-only change

Prefer the type that describes the main behavioral intent, not the largest file count.

## Scopes

Choose one short lowercase scope from the changed area. Prefer stable project vocabulary over one-off names. If the project has a root-level scope record, reuse its vocabulary.

Scope priority:

1. Feature or user-facing workflow: `auth`, `search`, `checkout`
2. Package, module, or command: `api`, `cli`, `worker`
3. Shared layer or tool: `hooks`, `scripts`, `config`, `deps`
4. Documentation group: `docs`, `readme`
5. Repository-wide fallback: `repo`

Use the same scope for related follow-up commits unless the changed area clearly moves elsewhere.

If no project-local scope record exists and the user is formalizing commit hygiene, suggest creating `GIT_HYGIENE.md` in the repository root so future agents can reuse the same scope vocabulary.

Avoid:

- File extensions as scopes, such as `py` or `md`
- Overly broad scopes, such as `app`, when a narrower stable area exists
- New synonyms for an existing scope
- `repo` when a specific scope is defensible

## Body Sections

Use body sections only when they add useful context beyond the subject.

```text
[aim]
<why this change is needed>

[approach]
- <implementation choice or changed area>
- <another implementation point, if needed>

[attention]
- <risk, migration note, test gap, or reviewer note>
- <another note, if needed>
```

Use bullets in `[approach]` and `[attention]` when there is more than one point. A single point may be one sentence without a bullet. Omit empty sections.

Use `[attention]` for information that affects reviewer judgment:

- known risk or unresolved edge case
- migration, rollback, or data-boundary note
- skipped, failed, blocked, or meaningfully limited validation
- manual follow-up that must not be missed

Do not include routine successful checks just to record execution. For example, omit statements such as "Verified Python syntax" unless the verification result changes how reviewers should assess the commit.

## Footers

For commits drafted or made in an AI agent session, put the resume footer near the end:

```text
codex resume <SESSION_ID>
```

Use `claude resume <SESSION_ID>` only when the active agent context is Claude rather than Codex. If `SESSION_ID` is unavailable, omit the footer rather than inventing an ID.

When an issue id is directly relevant and known, put it after the resume footer:

```text
Refs: #<ISSUE_ID>
```
