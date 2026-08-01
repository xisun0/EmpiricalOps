#!/usr/bin/env python3
"""Collect compact Git context for drafting commit messages."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run_git(args: list[str]) -> tuple[int, str]:
    result = subprocess.run(
        ["git", *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    return result.returncode, result.stdout.strip()


def print_section(title: str, args: list[str]) -> None:
    code, output = run_git(args)
    print(f"\n## {title}")
    if code != 0:
        print(output or f"git {' '.join(args)} failed")
        return
    print(output or "(none)")


def main() -> int:
    if not (Path.cwd() / ".git").exists():
        code, top_level = run_git(["rev-parse", "--show-toplevel"])
        if code != 0:
            print("Not inside a Git repository.")
            return 1
        print(f"Repository: {top_level}")

    print_section("Status", ["status", "--short"])
    print_section("Staged Stat", ["diff", "--cached", "--stat"])
    print_section("Unstaged Stat", ["diff", "--stat"])
    print_section("Staged Files", ["diff", "--cached", "--name-status"])
    print_section("Unstaged Files", ["diff", "--name-status"])
    print_section("Untracked Files", ["ls-files", "--others", "--exclude-standard"])
    print_section("Recent Commits", ["log", "--oneline", "-n", "8"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
