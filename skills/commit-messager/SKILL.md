---
name: commit-messager
description: "Draft high-quality Angular-style Git commit messages from repository changes using the template type(scope): short summary. Use when Codex needs to inspect staged or unstaged diffs, summarize the intent and impact of code changes, propose commit messages, split changes into multiple commits, or refine an existing commit message before committing."
---

# Commit Messager

## Workflow

1. Inspect repository state before drafting:
   - Run `git status --short`.
   - Prefer staged changes with `git diff --cached --stat` and `git diff --cached`.
   - If nothing is staged, inspect unstaged changes with `git diff --stat` and `git diff`.
   - Check recent style with `git log --oneline -n 8` when the repository has history.
2. Do not stage, unstage, commit, amend, or reset changes unless the user explicitly asks.
3. Identify whether changes form one commit or several coherent commits.
4. Check the target repository root for project-local scope guidance before choosing `scope`. Prefer `GIT_HYGIENE.md`; use `AGENTS.md`, `CLAUDE.md`, `.commit-scopes.md`, `.commit-message.md`, or similar files only as compatibility fallbacks.
5. Read `references/git_hygiene.md` as the fallback convention for `type`, `scope`, body sections, and footers when the target repository has no local guidance.
6. Before drafting or making a commit, explicitly check whether a current Codex session id is available from injected `SESSION_ID` context or a session-id hook artifact. If no session id is available, state that before committing.
7. Draft message candidates using the Angular-style template `type(scope): short summary`.
8. Keep the subject line imperative, specific, and under 72 characters when practical.
9. Add a body only when it clarifies non-obvious intent, behavior changes, migration notes, risk, or reviewer-relevant test gaps.
10. For commits made or drafted in the current Codex session, append `codex resume <SESSION_ID>` as the final body line when `SESSION_ID` is available.
11. Do not include routine successful verification in the commit body. Mention testing only when a failure, skipped check, untested path, or limitation affects reviewer judgment.

## Helper Script

Use `scripts/collect_commit_context.py` to gather a compact summary before drafting:

```bash
python3 scripts/collect_commit_context.py
```

Resolve the script path relative to this skill directory, but run it from the target Git repository. The script reports status, staged and unstaged stats, untracked files, recent commits, and file-level diff names. Read full diffs with `git diff` or `git diff --cached` when the summary is not enough to understand intent.

## Optional Codex Hook

Use `scripts/session_start_commit_context.py` as a Codex `SessionStart` hook when the user wants commit-message context injected automatically at session startup or resume.

Use `scripts/pre_tool_use_session_context.py` as an optional Codex `PreToolUse` hook when the user wants the current session id re-injected only when the commit-messager helper is about to run. Configure it with a `Bash` matcher; the script exits without output unless the pending command calls `collect_commit_context.py`.

Add a command hook like this to the user's Codex config, replacing the path with this skill's installed location:

```toml
[hooks]
SessionStart = [
  { hooks = [
    { type = "command", command = "/absolute/path/to/commit-messager/scripts/session_start_commit_context.py", async = false, timeoutSec = 5 }
  ] }
]
PreToolUse = [
  { matcher = "Bash", hooks = [
    { type = "command", command = "/absolute/path/to/commit-messager/scripts/pre_tool_use_session_context.py", async = false, timeoutSec = 5 }
  ] }
]
```

The hook reads the Codex hook payload from stdin, checks the payload `cwd`, and emits `additionalContext` only when that directory is a Git worktree with uncommitted changes. It injects a compact status summary, the `codex resume <SESSION_ID>` footer when `session_id` is present, and a reminder to use `$commit-messager`; it does not stage, commit, amend, or modify files.
The `PreToolUse` hook reads the current hook payload and injects session context only for pending Bash commands that call `collect_commit_context.py`; it does not persist session ids or modify repository files.

## Output Shape

Use project-local scope guidance as the source of truth when present. Use `references/git_hygiene.md` only as the fallback convention for type, scope, body section, and footer conventions.

For a single commit, provide:

```text
type(scope): short summary

[aim]
<why this change is needed>

[approach]
- <implementation choice or changed area>
- <another implementation point, if needed>

[attention]
- <risk, migration note, test gap, or reviewer note>
- <another note, if needed>

codex resume <SESSION_ID>
Refs: #<ISSUE_ID>
```

For multiple possible commits, provide each message under a short heading naming the change group. Include the files or change theme that belong in each commit.

When the user asks for alternatives, give 2-4 candidates with different emphasis rather than tiny wording variations.

- Use `[aim]`, `[approach]`, and `[attention]` only when they add useful context beyond the subject.
- Write `[approach]` and `[attention]` as bullet lists when there is more than one point. A single point may be one sentence without a bullet.
- Use `[attention]` for risks, migration notes, reviewer notes, or meaningful validation gaps. Do not put routine successful checks there.
- Omit empty sections.
- If `codex resume <SESSION_ID>` is included, keep it as the final body line unless the user explicitly requests another footer after it.

## Judgment Rules

- If the repository has no project-local scope record, mention that the chosen scope follows the fallback convention and suggest adding one when the user is formalizing commit hygiene.
- When suggesting a project-local scope record, recommend `GIT_HYGIENE.md` in the repository root.
- Avoid vague subjects such as `update files`, `fix bug`, `misc changes`, or `refactor code` unless the diff truly gives no more information.
- Do not include ticket IDs, co-author trailers, breaking-change trailers, or generated-by lines unless the repository already uses them or the user asks.
- If the diff is too large or ambiguous, state what is unclear and draft the safest message from observable changes.
- If staged and unstaged changes differ, clearly say which set the message covers.
