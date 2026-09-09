#!/usr/bin/env python3
"""Inventory custom frontend dependencies from exported Lovelace dashboards."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def walk(value, found: set[str], flags: set[str]) -> None:
    if isinstance(value, dict):
        if "card_mod" in value:
            flags.add("card-mod")
        for key, child in value.items():
            if key in {"type", "layout_type"} and isinstance(child, str) and child.startswith("custom:"):
                found.add(child.removeprefix("custom:"))
            walk(child, found, flags)
    elif isinstance(value, list):
        for child in value:
            walk(child, found, flags)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    dashboards = repo / "home-assistant" / "live-export" / "dashboards"
    output = repo / "inventory" / "generated-live" / "FRONTEND-DEPENDENCIES.md"

    by_component: dict[str, set[str]] = defaultdict(set)
    dashboard_count = 0

    if dashboards.exists():
        for path in sorted(dashboards.glob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                continue

            dashboard_count += 1
            found: set[str] = set()
            flags: set[str] = set()
            walk(data, found, flags)

            for component in found | flags:
                by_component[component].add(path.stem)

    lines = [
        "# Generated frontend dependency inventory",
        "",
        "Derived automatically from the public JSON Lovelace dashboard exports.",
        "",
        f"Dashboards scanned: **{dashboard_count}**",
        "",
        "| Custom frontend dependency | Dashboards using it |",
        "| --- | --- |",
    ]

    if by_component:
        for component in sorted(by_component, key=str.lower):
            names = ", ".join(f"`{name}`" for name in sorted(by_component[component]))
            lines.append(f"| `{component}` | {names} |")
    else:
        lines.append("| None detected | — |")

    lines += [
        "",
        "`card-mod` is detected from `card_mod` configuration blocks rather than a `custom:` card type.",
        "",
        "This report identifies frontend component names only. Install the maintained compatible release through HACS or the component's supported installation method.",
    ]

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print()
    print("Frontend dependency audit")
    print(f"Dashboards scanned: {dashboard_count}")
    print(f"Custom frontend dependencies: {len(by_component)}")
    print("Report: inventory/generated-live/FRONTEND-DEPENDENCIES.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
