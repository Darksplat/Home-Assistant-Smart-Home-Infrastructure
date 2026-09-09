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


def text_files(root: Path):
    if not root.exists():
        return
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".yaml", ".yml", ".json", ".jinja"}:
            yield path


def redact_generated_identifiers(repo: Path) -> tuple[int, int]:
    roots = [repo / "home-assistant" / "live-export", repo / "inventory" / "generated-live"]
    mac_count = 0
    email_count = 0
    for root in roots:
        for path in text_files(root) or []:
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            new_text, macs = MAC_RE.subn("<HARDWARE_ADDRESS_OMITTED>", text)
            new_text, emails = EMAIL_RE.subn("<EMAIL_OMITTED>", new_text)
            if macs or emails:
                path.write_text(new_text, encoding="utf-8")
                mac_count += macs
                email_count += emails
    return mac_count, email_count


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

                # Credential assignments are meaningful in deployable config/dashboard
                # files, but ordinary documentation words such as "credentials" are not.
                if rel.startswith("home-assistant/live-export/") and path.suffix.lower() in {".yaml", ".yml", ".json"}:
                    if CREDENTIAL_ASSIGNMENT_RE.search(line):
                        findings.append(("credential-like assignment", rel, lineno))

                # Only treat globally routable IPv4-looking values as warnings inside
                # exported HA configuration/dashboard data. Inventory metadata/version
                # strings are intentionally excluded to avoid e.g. 1.7.5.2 false positives.
                if rel.startswith("home-assistant/live-export/"):
                    for token in IPV4_TOKEN_RE.findall(line):
                        if is_global_ipv4(token):
                            findings.append(("possible public IPv4 address", rel, lineno))
                            break
    return findings


def write_report(repo: Path, mac_redactions: int, email_redactions: int, findings: list[tuple[str, str, int]]) -> None:
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

    mac_redactions, email_redactions = redact_generated_identifiers(repo)
    fix_export_report(repo)
    findings = scan(repo)
    write_report(repo, mac_redactions, email_redactions, findings)

    print()
    print("Public export safety pass")
    print(f"MAC/hardware addresses redacted: {mac_redactions}")
    print(f"Email addresses redacted: {email_redactions}")
    print(f"Remaining high-risk findings: {len(findings)}")
    print("Review: inventory/generated-live/PUBLIC-SAFETY-SCAN.md")

    if findings:
        print("EXPORT NOT READY FOR PUBLIC COMMIT")
        return 2

    print("PUBLIC SAFETY PASS: clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
