#!/usr/bin/env python3
"""Inject Codex session context before the commit-messager helper runs."""

from __future__ import annotations

import json
import sys


HELPER_NAME = "collect_commit_context.py"


def hook_output(additional_context: str) -> str:
    return json.dumps(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
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

    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return 0

    command = tool_input.get("command")
    if not isinstance(command, str) or HELPER_NAME not in command:
        return 0

    session_id = payload.get("session_id")
    if not isinstance(session_id, str) or not session_id.strip():
        return 0

    session_id = session_id.strip()
    print(
        hook_output(
            "Current Codex session id for commit-messager: "
            f"SESSION_ID={session_id}\n"
            "For commits drafted or made in this session, append "
            f"`codex resume {session_id}` as the final body line."
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
