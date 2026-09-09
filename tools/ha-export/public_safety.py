#!/usr/bin/env python3
"""Post-process and validate generated Home Assistant public export.

This script only touches files generated inside this repository. It never reads or
modifies the live Home Assistant source mount.
"""

from __future__ import annotations

import argparse
import ipaddress
import re
from pathlib import Path

MAC_RE = re.compile(r"\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b")
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
BEARER_RE = re.compile(r"(?i)Bearer\s+[A-Za-z0-9._~+/=-]{16,}")
URL_SECRET_RE = re.compile(
    r"(?i)([?&](?:token|api[_-]?key|key|secret|auth|password|access[_-]?token)=)[^&\s\"']+"
)
CREDENTIAL_ASSIGNMENT_RE = re.compile(
    r"(?i)^\s*[^#\n:]*?(?:password|passwd|secret|api[_-]?key|access[_-]?token|"
    r"refresh[_-]?token|client[_-]?secret|authorization|credential|webhook)[^:]*:\s*(?!.*!secret).+"
)
IPV4_TOKEN_RE = re.compile(r"(?<![0-9.])(?:\d{1,3}\.){3}\d{1,3}(?![0-9.])")
OPAQUE_HEX_RE = re.compile(
    r"(?<![0-9A-Fa-f])(?=[0-9A-Fa-f]{12,64}(?![0-9A-Fa-f]))"
    r"(?=[0-9A-Fa-f]*[A-Fa-f])[0-9A-Fa-f]{12,64}"
)
MOBILE_NOTIFY_RE = re.compile(r"\bnotify\.mobile_app_[a-z0-9_]+\b", re.IGNORECASE)

# These files are intentionally not suitable for a public repository. The
# household dashboard/package contains member-specific data, while complete
# device/entity registries disclose names, room associations and operational
# details far beyond what is needed for reproducibility.
PRIVATE_GENERATED_PATHS = (
    "home-assistant/live-export/configuration/packages/household_chores.yaml",
    "home-assistant/live-export/dashboards/dashboard-household.json",
    "home-assistant/live-export/dashboards/dashboard-household.yaml",
)
REGISTRY_INVENTORY_PATHS = (
    "inventory/generated-live/devices.md",
    "inventory/generated-live/entities.md",
)


def text_files(root: Path):
    if not root.exists():
        return
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".yaml", ".yml", ".json", ".jinja"}:
            yield path


def remove_paths(repo: Path, paths: tuple[str, ...]) -> int:
    removed = 0
    for rel in paths:
        path = repo / rel
        if path.is_file():
            path.unlink()
            removed += 1
    return removed


def remove_household_specific_files(repo: Path) -> int:
    removed = remove_paths(repo, PRIVATE_GENERATED_PATHS)

    index = repo / "home-assistant" / "live-export" / "dashboards" / "README.md"
    if index.is_file():
        lines = index.read_text(encoding="utf-8").splitlines()
        filtered = [line for line in lines if "lovelace.dashboard_household" not in line]
        if filtered != lines:
            index.write_text("\n".join(filtered) + "\n", encoding="utf-8")

    return removed


def redact_generated_identifiers(repo: Path) -> tuple[int, int, int, int]:
    roots = [repo / "home-assistant" / "live-export", repo / "inventory" / "generated-live"]
    mac_count = 0
    email_count = 0
    opaque_count = 0
    mobile_notify_count = 0

    opaque_aliases: dict[str, str] = {}
    mobile_aliases: dict[str, str] = {}

    def opaque_replacement(match: re.Match[str]) -> str:
        nonlocal opaque_count
        token = match.group(0)
        if token not in opaque_aliases:
            opaque_aliases[token] = f"deviceid_{len(opaque_aliases) + 1:03d}"
        opaque_count += 1
        return opaque_aliases[token]

    def mobile_replacement(match: re.Match[str]) -> str:
        nonlocal mobile_notify_count
        token = match.group(0)
        if token not in mobile_aliases:
            mobile_aliases[token] = f"notify.mobile_app_household_device_{len(mobile_aliases) + 1:02d}"
        mobile_notify_count += 1
        return mobile_aliases[token]

    for root in roots:
        for path in text_files(root) or []:
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue

            new_text, macs = MAC_RE.subn("<HARDWARE_ADDRESS_OMITTED>", text)
            new_text, emails = EMAIL_RE.subn("<EMAIL_OMITTED>", new_text)
            new_text = MOBILE_NOTIFY_RE.sub(mobile_replacement, new_text)
            new_text = OPAQUE_HEX_RE.sub(opaque_replacement, new_text)

            if new_text != text:
                path.write_text(new_text, encoding="utf-8")
            mac_count += macs
            email_count += emails

    return mac_count, email_count, opaque_count, mobile_notify_count


def fix_export_report(repo: Path) -> None:
    path = repo / "inventory" / "generated-live" / "EXPORT-REPORT.md"
    if not path.exists():
        return
    lines = path.read_text(encoding="utf-8").splitlines()
    try:
        start = lines.index("## Copied/sanitized text configuration")
        end = lines.index("## Redactions applied")
    except ValueError:
        return
    section = lines[start + 1 : end]
    real_items = [line for line in section if line.startswith("- `")]
    if real_items:
        section = [line for line in section if line != "- None"]
        lines = lines[: start + 1] + section + lines[end:]
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def is_global_ipv4(token: str) -> bool:
    try:
        addr = ipaddress.ip_address(token)
    except ValueError:
        return False
    return isinstance(addr, ipaddress.IPv4Address) and addr.is_global


def scan(repo: Path) -> list[tuple[str, str, int]]:
    findings: list[tuple[str, str, int]] = []
    roots = [repo / "home-assistant" / "live-export", repo / "inventory" / "generated-live"]

    for root in roots:
        for path in text_files(root) or []:
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeDecodeError):
                continue
            rel = path.relative_to(repo).as_posix()
            for lineno, line in enumerate(lines, 1):
                if MAC_RE.search(line):
                    findings.append(("MAC address", rel, lineno))
                if EMAIL_RE.search(line):
                    findings.append(("email address", rel, lineno))
                if BEARER_RE.search(line):
                    findings.append(("Bearer token", rel, lineno))
                if URL_SECRET_RE.search(line):
                    findings.append(("secret-bearing URL", rel, lineno))

                if rel.startswith("home-assistant/live-export/") and path.suffix.lower() in {
                    ".yaml",
                    ".yml",
                    ".json",
                }:
                    if CREDENTIAL_ASSIGNMENT_RE.search(line):
                        findings.append(("credential-like assignment", rel, lineno))

                if rel.startswith("home-assistant/live-export/"):
                    for token in IPV4_TOKEN_RE.findall(line):
                        if is_global_ipv4(token):
                            findings.append(("possible public IPv4 address", rel, lineno))
                            break
    return findings


def write_report(
    repo: Path,
    mac_redactions: int,
    email_redactions: int,
    opaque_redactions: int,
    mobile_notify_redactions: int,
    household_files_removed: int,
    registry_files_removed: int,
    findings: list[tuple[str, str, int]],
) -> None:
    path = repo / "inventory" / "generated-live" / "PUBLIC-SAFETY-SCAN.md"
    lines = [
        "# Public export safety scan",
        "",
        "Generated automatically after the Home Assistant export.",
        "",
        "## Automatic identifier redaction",
        "",
        f"- MAC/hardware addresses redacted: **{mac_redactions}**",
        f"- Email addresses redacted: **{email_redactions}**",
        f"- Opaque hardware/vendor identifiers aliased: **{opaque_redactions}**",
        f"- Mobile-app notification targets aliased: **{mobile_notify_redactions}**",
        "",
        "## Privacy exclusions",
        "",
        f"- Household-specific generated files removed: **{household_files_removed}**",
        f"- Full device/entity registry inventory files removed: **{registry_files_removed}**",
        "",
        "The live household chores package/dashboard and complete Home Assistant device/entity "
        "registries are intentionally excluded from the public snapshot. Aggregate counts, "
        "integration inventory, area inventory and curated subsystem documentation remain public.",
        "",
        "## Remaining high-risk findings",
        "",
    ]
    if findings:
        for label, rel, lineno in findings:
            lines.append(f"- **{label}:** `{rel}:{lineno}`")
    else:
        lines.append("- None detected")
    lines += [
        "",
        "This scan is a guardrail, not a substitute for review before merging into a public repository.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()

    household_files_removed = remove_household_specific_files(repo)
    registry_files_removed = remove_paths(repo, REGISTRY_INVENTORY_PATHS)
    (
        mac_redactions,
        email_redactions,
        opaque_redactions,
        mobile_notify_redactions,
    ) = redact_generated_identifiers(repo)
    fix_export_report(repo)
    findings = scan(repo)
    write_report(
        repo,
        mac_redactions,
        email_redactions,
        opaque_redactions,
        mobile_notify_redactions,
        household_files_removed,
        registry_files_removed,
        findings,
    )

    print()
    print("Public export safety pass")
    print(f"MAC/hardware addresses redacted: {mac_redactions}")
    print(f"Email addresses redacted: {email_redactions}")
    print(f"Opaque hardware/vendor identifiers aliased: {opaque_redactions}")
    print(f"Mobile-app notification targets aliased: {mobile_notify_redactions}")
    print(f"Household-specific generated files removed: {household_files_removed}")
    print(f"Full device/entity registry inventory files removed: {registry_files_removed}")
    print(f"Remaining high-risk findings: {len(findings)}")
    print("Review: inventory/generated-live/PUBLIC-SAFETY-SCAN.md")

    if findings:
        print("EXPORT NOT READY FOR PUBLIC COMMIT")
        return 2

    print("PUBLIC SAFETY PASS: clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
