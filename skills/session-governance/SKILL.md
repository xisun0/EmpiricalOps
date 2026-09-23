---
name: session-governance
description: Review, classify, rename, archive, or propose deletion of Codex tasks and conversations. Use when a user asks to clean up sessions, decide which work is complete, normalize titles, or manage a project's conversation backlog.
---

# Session Governance

Keep the user's active work easy to find without losing unfinished context or deleting useful records. The default workflow normalizes titles during review, then reports the recommended archive/delete actions; carry out archive and deletion only at the authorization level below.

## Inventory and evidence

- Establish scope first: current project, named project, all tasks, or a date range. Do not silently extend a request from one project to the whole account.
- By default, “all local conversations” means every **unarchived** local user task in the project. Archived tasks are outside the review universe: do not read, classify, rename, or list them unless the user explicitly asks for an archived-history audit.
- For a complete default review, use the available local task index read-only as the authoritative inventory. Filter on the exact current-project `cwd` and `archived = 0`, then exclude only records whose metadata establishes that they are platform-internal. Do not use an empty title as an exclusion rule.
- Treat `list_threads` and the project sidebar as live-state/detail sources, not complete inventory sources: their result set can be globally recency-limited. Use them to read a candidate's current status after the local index has identified every candidate, not to decide which candidates exist.
- Do not call `list_archived_threads` in the default workflow. It is allowed only for an explicitly requested archived-history audit, which is read-only by default.
- Exclude platform-internal approval, audit, evaluator, or other system-generated records from the user-session ledger. Do not use an absent title alone as the exclusion test: retain an untitled record when its metadata or transcript indicates that it is a user task. Report the number of excluded system records separately, without proposing any action on them.
- For each candidate, read the task's title, recent status, and enough of its final substantive turn to establish the actual objective, delivered result, open work, external follow-up, and whether it contains reusable decisions. Treat an old title, an apparently idle state, or a task that merely says "completed" as insufficient proof.
- Report uncertainty rather than guessing. Never infer that an external action, test, commit, delivery, or user decision happened without evidence.

## Classify by task state

Assign one recommendation and a short evidence-based reason:

| Recommendation | Meaning |
| --- | --- |
| Keep active | There is a concrete next action, pending user input, ongoing run, unresolved blocker, or the task is the designated home for recurring work. |
| Archive | Its stated objective and deliverable are complete, or it reached a documented stopping point, with no open in-task action. It remains useful as history. |
| Rename + keep/archive | The title is vague, misleading, duplicated, or auto-generated, but the task has enduring context. |
| Propose deletion | A record that satisfies every permanent-deletion condition below. |
| Needs review | Evidence is mixed, truncated, or the value of preserving context is unclear. |

## Temporary versus permanently deletable

A temporary task is a narrow, one-off interaction with no intended continuation. It can still merit archival: temporary does not mean disposable.

Propose permanent deletion only when every condition is established from the record:

- It is an accidental duplicate, an empty/abandoned start, a throwaway experiment, or a low-value one-off query/operation. Simple lookups, routine how-to questions, and completed basic actions are valid deletion candidates when they have few, shallow turns and their answer or outcome has no continuing value.
- It contains no unique decision, research evidence, user preference, handoff, source link, artifact, code/worktree change, or reasoning likely to be useful later.
- It has no concrete next action, pending user input, external follow-up, unresolved blocker, or ongoing execution.
- It is not pinned, a designated recurring/home task, or part of a task chain whose context remains needed.

Treat few and shallow turns as supporting evidence, not a mechanical threshold: a short conversation may still record an important decision or source. If any condition is false or cannot be verified, recommend **archive** or **needs review**, not deletion. Age, short length, an uninformative title, idle status, or a completed answer alone are never enough to recommend deletion. Permanent deletion additionally requires the user's explicit confirmation of the exact candidate set.

## Title standard

Use `范围｜具体问题或任务` in the user's working language. Project membership is already visible in the sidebar: do not repeat the project name in the title.

- When the task is mainly about a tracked Issue, the left side is `Issue #<number>`; the right side states the Issue's central, user-understandable problem or requested outcome.
- Otherwise, the left side is a short, stable scope within that project—such as `IPO`, `Asset Pricing`, or `Writing`—rather than a generic verb, tool name, or the project name.
- The right side names the concrete question, breakage, decision, or deliverable in plain language. Prefer the causal symptom or object over abstract labels such as “修正建议”, “优化”, “处理”, or “相关问题”.
- Use the objective and final substantive work to title the task, not incidental commands, models, or exploratory steps. Do not encode transient status such as “进行中” or “已完成” in the title.

Examples:

- `Issue #1｜项目 Skill 无法被当前会话发现`
- `IPO｜申请轮次财务变量回填`
- `Asset Pricing｜事件窗口收益的构造方式`
- `Writing｜结论段与实证结果不一致`

For deliberately recurring/daily tasks, retain the user's established convention rather than forcing this format. Avoid changing a title if the current one is already clearer or if a new title would conceal an unresolved state.

## Authorization and execution

- **Review mode (default):** apply a title change when the reviewed record has a clearer title under the title standard, then provide the four-group report in [the ledger](references/review-ledger.md). Report the previous and resulting titles. Do not rename when the existing title is already clearer or evidence is insufficient.
- **Rename mode:** use only when the user asks to rename a selected title despite the review classification; otherwise title normalization happens during review without per-task confirmation.
- **Archive mode:** archive only the explicitly selected/approved tasks. Preserve the review record and report the completed archive actions.
- **Delete mode:** deletion is destructive. First present each exact task proposed for deletion with its reason and ask for explicit confirmation of the exact set. Do not treat broad cleanup wording or approval to archive/rename as deletion permission. If no supported deletion capability exists, say so plainly and provide the smallest manual path; do not improvise filesystem deletion or UI automation that could affect other tasks.

When a requested action cannot be performed, distinguish a limitation of the available interface from the classification result. Re-run or refresh the inventory before acting when it is no longer current or the task state may have changed during review.

## Review output

Start with a one-line scope summary: the count of **unarchived** local user tasks in the project, excluded system records, and the count of titles changed. Then use the [four-group report](references/review-ledger.md), in this order: low-risk permanent-deletion candidates, archive candidates, tasks needing human confirmation, and ongoing tasks to keep. Put every reviewed user task in exactly one group; system records are counted but never grouped. Do not display task IDs unless titles are duplicated, the user asks for IDs, or an ID is necessary to disambiguate a destructive-action confirmation. Keep deletion candidates visually and semantically separate, state the evidence for each, and ask for a separate confirmation before any deletion attempt.
