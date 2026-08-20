#!/usr/bin/env python3
"""Inventory active LaTeX table and figure environments."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


BEGIN_RE = re.compile(r"\\begin\{(table\*?|figure\*?)\}")
END_RE = re.compile(r"\\end\{(table\*?|figure\*?)\}")
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
CAPTION_RE = re.compile(r"\\caption(?:\[[^]]*\])?\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}")
INPUT_RE = re.compile(r"\\(?:input|[A-Za-z@]*tableinput)\{([^}]+)\}")
GRAPHIC_RE = re.compile(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}")
NEWLABEL_RE = re.compile(r"\\newlabel\{([^}]+)\}\{\{([^}]*)\}")


def strip_comment(line: str) -> str:
    for index, char in enumerate(line):
        if char != "%":
            continue
        backslashes = 0
        cursor = index - 1
        while cursor >= 0 and line[cursor] == "\\":
            backslashes += 1
            cursor -= 1
        if backslashes % 2 == 0:
            return line[:index]
    return line


def read_aux(aux_path: Path | None) -> dict[str, str]:
    if aux_path is None or not aux_path.exists():
        return {}
    numbers: dict[str, str] = {}
    for line in aux_path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = NEWLABEL_RE.search(line)
        if match:
            numbers[match.group(1)] = match.group(2)
    return numbers


def normalize_asset(value: str, suffix: str) -> str:
    value = value.strip()
    if not Path(value).suffix:
        value = f"{value}{suffix}"
    return value


def inventory(manuscript: Path, aux_path: Path | None = None) -> dict[str, object]:
    raw_lines = manuscript.read_text(encoding="utf-8", errors="replace").splitlines()
    lines = [strip_comment(line) for line in raw_lines]
    aux_numbers = read_aux(aux_path)
    appendix = False
    current: dict[str, object] | None = None
    artifacts: list[dict[str, object]] = []

    for line_number, line in enumerate(lines, start=1):
        if re.search(r"\\appendix\b|\\begin\{appendices\}", line):
            appendix = True

        if current is None:
            begin = BEGIN_RE.search(line)
            if not begin:
                continue
            environment = begin.group(1)
            current = {
                "kind": "table" if environment.startswith("table") else "figure",
                "environment": environment,
                "section": "appendix" if appendix else "main",
                "source": str(manuscript),
                "line_start": line_number,
                "line_end": None,
                "labels": [],
                "caption": "",
                "inputs": [],
                "graphics": [],
                "inline_body": False,
                "number": None,
                "continued_of": None,
            }

        assert current is not None
        current["labels"].extend(LABEL_RE.findall(line))
        captions = CAPTION_RE.findall(line)
        if captions and not current["caption"]:
            current["caption"] = captions[0].strip()
        current["inputs"].extend(normalize_asset(item, ".tex") for item in INPUT_RE.findall(line))
        current["graphics"].extend(normalize_asset(item, "") for item in GRAPHIC_RE.findall(line))
        if current["kind"] == "table" and re.search(r"\\begin\{(?:tabular\*?|tabularx|longtable)\}", line):
            current["inline_body"] = True

        end = END_RE.search(line)
        if end and end.group(1) == current["environment"]:
            current["line_end"] = line_number
            labels = current["labels"]
            current["number"] = next((aux_numbers[label] for label in labels if label in aux_numbers), None)
            current["inputs"] = list(dict.fromkeys(current["inputs"]))
            current["graphics"] = list(dict.fromkeys(current["graphics"]))
            current["labels"] = list(dict.fromkeys(labels))
            artifacts.append(current)
            current = None

    if current is not None:
        raise ValueError(f"Unclosed {current['environment']} beginning at line {current['line_start']}")

    previous_table: dict[str, object] | None = None
    for artifact in artifacts:
        if artifact["kind"] != "table":
            continue
        if (
            artifact["number"] is None
            and "continued" in artifact["caption"].lower()
            and previous_table is not None
            and previous_table["section"] == artifact["section"]
        ):
            artifact["number"] = previous_table["number"]
            artifact["continued_of"] = (
                previous_table["labels"][0] if previous_table["labels"] else previous_table["number"]
            )
        previous_table = artifact

    environment_counts = {
        section: {
            kind: sum(1 for item in artifacts if item["section"] == section and item["kind"] == kind)
            for kind in ("figure", "table")
        }
        for section in ("main", "appendix")
    }
    logical_counts = {
        section: {
            kind: sum(
                1
                for item in artifacts
                if item["section"] == section
                and item["kind"] == kind
                and item["continued_of"] is None
            )
            for kind in ("figure", "table")
        }
        for section in ("main", "appendix")
    }

    return {
        "manuscript": str(manuscript),
        "aux": str(aux_path) if aux_path else None,
        "artifacts": artifacts,
        "counts": {"environments": environment_counts, "logical": logical_counts},
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manuscript", type=Path, required=True)
    parser.add_argument("--aux", type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = inventory(args.manuscript.resolve(), args.aux.resolve() if args.aux else None)
    payload = json.dumps(result, indent=2, ensure_ascii=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
