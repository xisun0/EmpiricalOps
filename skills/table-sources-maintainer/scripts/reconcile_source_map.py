#!/usr/bin/env python3
"""Compare a fresh manuscript artifact inventory with a Markdown source map."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


LABEL_RE = re.compile(r"`((?:fig|tab):[^`]+)`")
ASSET_RE = re.compile(r"`([^`]+\.(?:tex|pdf|png|jpg|jpeg|svg))`", re.IGNORECASE)


def basename(value: str) -> str:
    return Path(value.strip()).name


def parse_source_map(path: Path) -> tuple[set[str], Counter[str], list[dict[str, object]]]:
    labels: set[str] = set()
    assets: Counter[str] = Counter()
    rows: list[dict[str, object]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith("|") or line.startswith("|---") or "LaTeX label" in line:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        row_labels = LABEL_RE.findall(cells[1])
        labels.update(row_labels)
        rows.append({"number": cells[0], "labels": row_labels})
        if "inlined in" in cells[2]:
            continue
        for match in ASSET_RE.findall(cells[2]):
            assets[basename(match)] += 1
    return labels, assets, rows


def parse_inventory(path: Path) -> tuple[set[str], Counter[str], list[dict[str, object]]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    labels: set[str] = set()
    assets: Counter[str] = Counter()
    for item in payload["artifacts"]:
        labels.update(label for label in item["labels"] if label.startswith(("fig:", "tab:")))
        for value in item["inputs"] + item["graphics"]:
            assets[basename(value)] += 1
    return labels, assets, payload["artifacts"]


def expected_number(item: dict[str, object]) -> str:
    number = str(item["number"])
    kind = str(item["kind"]).title()
    if item["section"] == "main":
        return f"{kind} {number}"
    if number.startswith("IA"):
        return f"IA {kind} {number[2:]}"
    return f"Appendix {kind} {number}"


def mapping_changes(
    artifacts: list[dict[str, object]], rows: list[dict[str, object]]
) -> tuple[list[str], list[str]]:
    label_to_artifact: dict[str, tuple[int, dict[str, object]]] = {}
    active_artifacts = [item for item in artifacts if item["continued_of"] is None]
    for index, item in enumerate(active_artifacts):
        for label in item["labels"]:
            if label.startswith(("fig:", "tab:")):
                label_to_artifact[label] = (index, item)

    number_mismatches: list[str] = []
    positions: list[tuple[int, str]] = []
    for row in rows:
        matches = [label_to_artifact[label] for label in row["labels"] if label in label_to_artifact]
        if not matches:
            continue
        index, item = matches[0]
        expected = expected_number(item)
        actual = str(row["number"])
        if actual != expected and not actual.startswith(f"{expected} Panel "):
            number_mismatches.append(f"{actual} -> {expected}")
        positions.append((index, actual))

    order_mismatches: list[str] = []
    for previous, current in zip(positions, positions[1:]):
        if current[0] < previous[0]:
            order_mismatches.append(f"{current[1]} follows {previous[1]}")
    return number_mismatches, order_mismatches


def print_group(title: str, values: list[str]) -> None:
    print(f"{title}: {len(values)}")
    for value in values:
        print(f"  - {value}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--source-map", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    inventory_labels, inventory_assets, artifacts = parse_inventory(args.inventory)
    map_labels, map_assets, rows = parse_source_map(args.source_map)

    missing_labels = sorted(inventory_labels - map_labels)
    stale_labels = sorted(map_labels - inventory_labels)
    missing_assets = sorted((inventory_assets - map_assets).elements())
    stale_assets = sorted((map_assets - inventory_assets).elements())
    number_mismatches, order_mismatches = mapping_changes(artifacts, rows)

    print_group("missing_from_map.labels", missing_labels)
    print_group("stale_in_map.labels", stale_labels)
    print_group("missing_from_map.assets", missing_assets)
    print_group("stale_in_map.assets", stale_assets)
    print_group("mapping_changed.numbering", number_mismatches)
    print_group("mapping_changed.order", order_mismatches)

    if (
        missing_labels
        or stale_labels
        or missing_assets
        or stale_assets
        or number_mismatches
        or order_mismatches
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
