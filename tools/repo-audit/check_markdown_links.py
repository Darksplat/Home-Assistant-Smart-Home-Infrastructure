#!/usr/bin/env python3
"""Check relative Markdown links inside the repository."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import unquote

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
SCHEMES = ("http://", "https://", "mailto:", "tel:", "javascript:")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()

    failures: list[tuple[str, int, str]] = []
    checked = 0

    for md in sorted(repo.rglob("*.md")):
        if ".git" in md.parts:
            continue

        try:
            lines = md.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue

        in_fence = False
        for lineno, line in enumerate(lines, 1):
            stripped = line.lstrip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue

            for match in LINK_RE.finditer(line):
                raw = match.group(1).strip()
                if not raw or raw.startswith("#") or raw.startswith(SCHEMES):
                    continue

                # Remove optional Markdown title and fragment.
                target = raw.split("#", 1)[0].strip()
                if target.startswith("<") and target.endswith(">"):
                    target = target[1:-1]
                if ' "' in target:
                    target = target.split(' "', 1)[0]
                target = unquote(target)
                if not target:
                    continue

                checked += 1
                resolved = (repo / target.lstrip("/")) if target.startswith("/") else (md.parent / target)
                if not resolved.resolve().exists():
                    failures.append((md.relative_to(repo).as_posix(), lineno, raw))

    print("Markdown link audit")
    print(f"Relative links checked: {checked}")

    if failures:
        print(f"Broken relative links: {len(failures)}")
        for path, lineno, target in failures:
            print(f"- {path}:{lineno} -> {target}")
        return 1

    print("Broken relative links: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
