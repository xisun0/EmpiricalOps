#!/usr/bin/env python3
"""Codex SessionStart hook that injects Git commit-message context."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


MAX_SECTION_CHARS = 2500


def run_git(cwd: Path, args: list[str]) -> tuple[int, str]:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    return result.returncode, result.stdout.strip()


def section(cwd: Path, title: str, args: list[str]) -> str:
    code, output = run_git(cwd, args)
    if code != 0:
        return f"## {title}\n{output or 'unavailable'}"
    output = output or "(none)"
    if len(output) > MAX_SECTION_CHARS:
        output = output[:MAX_SECTION_CHARS].rstrip() + "\n... truncated ..."
    return f"## {title}\n{output}"


def has_changes(cwd: Path) -> bool:
    code, output = run_git(cwd, ["status", "--porcelain"])
    return code == 0 and bool(output.strip())


def is_git_repo(cwd: Path) -> bool:
    code, _ = run_git(cwd, ["rev-parse", "--is-inside-work-tree"])
    return code == 0


def hook_output(additional_context: str) -> str:
    return json.dumps(
        {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": additional_context,
            }
        },
        ensure_ascii=True,
    )


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return 0

    cwd_value = payload.get("cwd")
    if not cwd_value:
        return 0

    cwd = Path(cwd_value)
    if not cwd.exists() or not cwd.is_dir() or not is_git_repo(cwd):
        return 0

    if not has_changes(cwd):
        return 0

    session_id = payload.get("session_id")
    footer_note = ""
    if isinstance(session_id, str) and session_id.strip():
        footer_note = (
            f" For commits drafted or made in this session, append "
            f"`codex resume {session_id.strip()}` as the last body line."
        )

    parts = [
        "The current Git repository has uncommitted changes. If the user asks for a commit message, use $commit-messager and draft it with the Angular-style template `type(scope): short summary` after inspecting the relevant diffs."
        + footer_note,
        section(cwd, "Git Status", ["status", "--short"]),
        section(cwd, "Staged Stat", ["diff", "--cached", "--stat"]),
        section(cwd, "Unstaged Stat", ["diff", "--stat"]),
        section(cwd, "Untracked Files", ["ls-files", "--others", "--exclude-standard"]),
        section(cwd, "Recent Commits", ["log", "--oneline", "-n", "8"]),
    ]

    print(hook_output("\n\n".join(parts)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
