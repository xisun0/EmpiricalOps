#!/usr/bin/env python3
"""Validate that an EmpiricalOps project setup is complete."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required to validate EmpiricalOps setup") from exc


FULL_COMMIT = re.compile(r"^[0-9a-f]{40}$")
SCOPE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
REQUIRED = (
    "project.kind",
    "install.scope",
    "git.base_branch",
    "git.merge_strategy",
    "git.commit_style",
    "git.identity.mode",
    "writing.mode",
    "outputs.exploratory_policy",
    "data.restricted_policy",
    "reflection.activation",
    "reflection.public_repo",
    "reflection.save_local_reports",
)
CHOICES = {
    "install.scope": {"project", "user"},
    "git.merge_strategy": {"squash", "merge", "rebase"},
    "git.identity.mode": {"inherit", "dedicated"},
    "writing.mode": {"same_repo", "submodule", "separate_repo", "none"},
    "reflection.activation": {"explicit", "suggest_after_complex_task"},
}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return data


def dotted(data: dict[str, Any], key: str) -> Any:
    value: Any = data
    for part in key.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def validate(profile: dict[str, Any], lock: dict[str, Any], root: Path) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED:
        if dotted(profile, key) is None:
            errors.append(f"unresolved required decision: {key}")

    for key, allowed in CHOICES.items():
        value = dotted(profile, key)
        if value is not None and value not in allowed:
            errors.append(f"invalid {key}: {value}")

    if dotted(profile, "git.identity.mode") == "dedicated":
        for key in ("git.identity.name", "git.identity.email"):
            if not dotted(profile, key):
                errors.append(f"dedicated identity requires: {key}")

    if dotted(profile, "data.restricted_policy") == "external_untracked":
        if not dotted(profile, "data.external_root"):
            errors.append("external data policy requires: data.external_root")

    source_commit = dotted(lock, "source.commit")
    if not isinstance(source_commit, str) or not FULL_COMMIT.fullmatch(source_commit):
        errors.append("lockfile source.commit must be a full lowercase Git commit")

    skills = lock.get("skills")
    if not isinstance(skills, dict) or not skills:
        errors.append("lockfile must contain at least one installed skill")
        skills = {}

    for name, entry in skills.items():
        if not isinstance(entry, dict):
            errors.append(f"invalid lock entry: {name}")
            continue
        install_path = entry.get("install_path")
        if not install_path:
            errors.append(f"missing install_path for skill: {name}")
            continue
        skill_dir = root / install_path
        if not (skill_dir / "SKILL.md").is_file():
            errors.append(f"installed skill is missing SKILL.md: {name}")

    if "commit-messager" in skills:
        scopes = dotted(profile, "git.scopes")
        if not isinstance(scopes, list) or not scopes:
            errors.append("commit-messager requires a non-empty git.scopes list")
        elif any(not isinstance(scope, str) or not SCOPE.fullmatch(scope) for scope in scopes):
            errors.append("git.scopes entries must use lowercase letters, digits, or hyphens")

        hygiene = root / "GIT_HYGIENE.md"
        agents = root / "AGENTS.md"
        if not hygiene.is_file():
            errors.append("commit-messager requires GIT_HYGIENE.md")
        if not agents.is_file():
            errors.append("commit-messager requires AGENTS.md")
        elif "GIT_HYGIENE.md" not in agents.read_text(encoding="utf-8", errors="replace"):
            errors.append("AGENTS.md must route Git work to GIT_HYGIENE.md")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--profile", type=Path)
    parser.add_argument("--lock", type=Path)
    args = parser.parse_args()

    root = args.project_root.resolve()
    profile_path = (args.profile or root / ".empiricalops" / "project.yml").resolve()
    lock_path = (args.lock or root / ".empiricalops" / "skills.lock").resolve()

    try:
        profile = load_yaml(profile_path)
        lock = load_yaml(lock_path)
        errors = validate(profile, lock, root)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        errors = [str(exc)]

    if errors:
        print("profile_draft")
        for error in errors:
            print(f"- {error}")
        return 1

    print("setup_complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
