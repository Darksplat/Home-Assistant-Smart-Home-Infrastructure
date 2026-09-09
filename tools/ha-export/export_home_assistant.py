#!/usr/bin/env python3
"""Conservative Home Assistant -> public GitHub exporter.

Reads a mounted Home Assistant /config directory and writes only selected,
public-safe material into this repository. The live HA files are never modified.

The exporter intentionally does NOT copy .storage wholesale, databases, logs,
backups, secrets, certificates, raw ESPHome YAML, custom-component source code,
auth data, mobile-app data, Thread datasets, or integration credential stores.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


TEXT_EXTENSIONS = {".yaml", ".yml", ".jinja", ".md", ".json"}
TOP_LEVEL_CONFIG_FILES = (
    "configuration.yaml",
    "automations.yaml",
    "scripts.yaml",
    "scenes.yaml",
    "customize.yaml",
    "groups.yaml",
)
COPY_CONFIG_DIRS = ("packages", "themes")

SENSITIVE_KEY_RE = re.compile(
    r"(?:password|passwd|token|secret|api[_-]?key|access[_-]?token|"
    r"client[_-]?secret|authorization|credential|webhook)",
    re.IGNORECASE,
)
SENSITIVE_YAML_LINE_RE = re.compile(
    r"^(?P<prefix>\s*[^#\n:]*?(?:password|passwd|token|secret|api[_-]?key|"
    r"access[_-]?token|client[_-]?secret|authorization|credential|webhook)"
    r"[^:]*:\s*)(?P<value>.+)$",
    re.IGNORECASE,
)
BEARER_RE = re.compile(r"(?i)Bearer\s+[A-Za-z0-9._~+/=-]{16,}")
URL_SECRET_RE = re.compile(
    r"(?i)([?&](?:token|api[_-]?key|key|access[_-]?token|auth)=)[^&\s\"']+"
)
LONG_SECRET_RE = re.compile(r"\b[A-Za-z0-9_-]{64,}\b")
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)


class ExportReport:
    def __init__(self) -> None:
        self.copied: list[str] = []
        self.redactions: list[str] = []
        self.skipped: list[str] = []
        self.warnings: list[str] = []
        self.dashboard_rows: list[dict[str, Any]] = []
        self.counts: dict[str, int] = {}

    def note_redaction(self, path: str, line: int, reason: str) -> None:
        self.redactions.append(f"{path}:{line} — {reason}")


def load_storage(path: Path) -> dict[str, Any] | None:
    try:
        with path.open("r", encoding="utf-8") as handle:
            obj = json.load(handle)
        if isinstance(obj, dict):
            return obj
    except (OSError, json.JSONDecodeError):
        return None
    return None


def redact_text(text: str, rel_path: str, report: ExportReport) -> str:
    """Redact obvious credential-like values from text config conservatively."""
    output: list[str] = []
    for number, line in enumerate(text.splitlines(keepends=True), start=1):
        original = line

        # !secret references are already the correct public form.
        if "!secret" not in line:
            match = SENSITIVE_YAML_LINE_RE.match(line.rstrip("\n"))
            if match:
                newline = "\n" if line.endswith("\n") else ""
                line = f'{match.group("prefix")}"<REDACTED>"{newline}'
                report.note_redaction(rel_path, number, "credential-like YAML key")

        replaced = BEARER_RE.sub("Bearer <REDACTED>", line)
        if replaced != line:
            report.note_redaction(rel_path, number, "Bearer token")
            line = replaced

        replaced = URL_SECRET_RE.sub(r"\1<REDACTED>", line)
        if replaced != line:
            report.note_redaction(rel_path, number, "credential in URL query")
            line = replaced

        # Very long opaque strings are unusual in ordinary YAML and often tokens.
        # Do not alter lines that are clearly Jinja/templates or comments.
        if "{{" not in line and "{%" not in line and not line.lstrip().startswith("#"):
            replaced = LONG_SECRET_RE.sub("<REDACTED_LONG_VALUE>", line)
            if replaced != line:
                report.note_redaction(rel_path, number, "long opaque value")
                line = replaced

        # Email addresses can identify household members or cloud accounts.
        replaced = EMAIL_RE.sub("<REDACTED_EMAIL>", line)
        if replaced != line:
            report.note_redaction(rel_path, number, "email address")
            line = replaced

        output.append(line)

        if original != line and not line.endswith("\n") and original.endswith("\n"):
            output[-1] += "\n"

    return "".join(output)


def copy_sanitized_text(source: Path, destination: Path, source_root: Path, report: ExportReport) -> None:
    rel = source.relative_to(source_root).as_posix()
    try:
        text = source.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        report.skipped.append(f"{rel} — unreadable/non-text")
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(redact_text(text, rel, report), encoding="utf-8")
    report.copied.append(rel)


def dashboard_has_sensitive_content(value: Any, path: str = "root") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if SENSITIVE_KEY_RE.search(str(key)):
                findings.append(child_path)
            findings.extend(dashboard_has_sensitive_content(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(dashboard_has_sensitive_content(child, f"{path}[{index}]"))
    elif isinstance(value, str):
        if BEARER_RE.search(value) or URL_SECRET_RE.search(value):
            findings.append(path)
    return findings


def count_section_cards(config: dict[str, Any]) -> tuple[int, int, int]:
    views = config.get("views", []) if isinstance(config, dict) else []
    view_count = len(views) if isinstance(views, list) else 0
    section_count = 0
    card_count = 0
    if isinstance(views, list):
        for view in views:
            if not isinstance(view, dict):
                continue
            sections = view.get("sections", [])
            if isinstance(sections, list):
                section_count += len(sections)
                for section in sections:
                    if isinstance(section, dict) and isinstance(section.get("cards"), list):
                        card_count += len(section["cards"])
            cards = view.get("cards", [])
            if isinstance(cards, list):
                card_count += len(cards)
    return view_count, section_count, card_count


def export_dashboards(source_root: Path, repo_root: Path, report: ExportReport) -> None:
    storage = source_root / ".storage"
    destination_root = repo_root / "home-assistant" / "live-export" / "dashboards"
    destination_root.mkdir(parents=True, exist_ok=True)

    for source in sorted(storage.glob("lovelace.*")):
        obj = load_storage(source)
        if not obj:
            report.skipped.append(f".storage/{source.name} — invalid JSON")
            continue
        data = obj.get("data")
        if not isinstance(data, dict) or not isinstance(data.get("config"), dict):
            report.skipped.append(f".storage/{source.name} — no data.config dashboard")
            continue
        config = data["config"]
        findings = dashboard_has_sensitive_content(config)
        if findings:
            report.skipped.append(
                f".storage/{source.name} — credential-like content at {', '.join(findings[:5])}"
            )
            continue

        slug = source.name.removeprefix("lovelace.").replace("_", "-").replace(".", "-")
        json_text = json.dumps(config, indent=2, ensure_ascii=False) + "\n"
        (destination_root / f"{slug}.json").write_text(json_text, encoding="utf-8")
        # JSON syntax is YAML 1.2 compatible. This preserves the exact structure
        # without a PyYAML dependency or an unsafe rewrite during extraction.
        (destination_root / f"{slug}.yaml").write_text(json_text, encoding="utf-8")

        views, sections, cards = count_section_cards(config)
        report.dashboard_rows.append(
            {
                "source": source.name,
                "slug": slug,
                "title": config.get("title", ""),
                "views": views,
                "sections": sections,
                "cards": cards,
                "bytes": len(json_text.encode("utf-8")),
            }
        )


def get_storage_data(source_root: Path, filename: str, key: str) -> list[dict[str, Any]]:
    obj = load_storage(source_root / ".storage" / filename)
    if not obj:
        return []
    data = obj.get("data", {})
    if not isinstance(data, dict):
        return []
    value = data.get(key, [])
    return value if isinstance(value, list) else []


def markdown_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def export_inventory(source_root: Path, repo_root: Path, report: ExportReport) -> None:
    output = repo_root / "inventory" / "generated-live"
    output.mkdir(parents=True, exist_ok=True)

    areas = get_storage_data(source_root, "core.area_registry", "areas")
    devices = get_storage_data(source_root, "core.device_registry", "devices")
    entities = get_storage_data(source_root, "core.entity_registry", "entities")
    entries = get_storage_data(source_root, "core.config_entries", "entries")

    area_names = {
        a.get("id"): (a.get("name") or "")
        for a in areas
        if isinstance(a, dict) and a.get("id")
    }
    entry_domains = {
        e.get("entry_id"): e.get("domain")
        for e in entries
        if isinstance(e, dict) and e.get("entry_id")
    }

    device_refs: dict[str, str] = {}
    device_area: dict[str, str] = {}
    device_rows: list[list[str]] = []
    for index, device in enumerate(devices, start=1):
        if not isinstance(device, dict):
            continue
        device_id = device.get("id")
        ref = f"D{index:03d}"
        if device_id:
            device_refs[device_id] = ref
        area = area_names.get(device.get("area_id"), "")
        if device_id:
            device_area[device_id] = area
        config_entries = device.get("config_entries", [])
        domains = sorted(
            {
                entry_domains.get(entry_id)
                for entry_id in config_entries
                if entry_domains.get(entry_id)
            }
        ) if isinstance(config_entries, list) else []
        name = device.get("name_by_user") or device.get("name") or device.get("default_name") or ""
        device_rows.append(
            [ref, name, device.get("manufacturer") or "", device.get("model") or "", area, ", ".join(domains)]
        )

    areas_md = ["# Generated Home Assistant areas", "", "Generated from the live HA area registry.", ""]
    for area in sorted(area_names.values(), key=str.lower):
        areas_md.append(f"- {area}")
    (output / "areas.md").write_text("\n".join(areas_md) + "\n", encoding="utf-8")

    devices_md = [
        "# Generated Home Assistant device inventory",
        "",
        "Identifiers, MAC addresses, serial numbers, unique IDs and config-entry IDs are intentionally omitted.",
        "",
        "| Ref | Name | Manufacturer | Model | Area | Integration(s) |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in device_rows:
        devices_md.append("| " + " | ".join(markdown_escape(x) for x in row) + " |")
    (output / "devices.md").write_text("\n".join(devices_md) + "\n", encoding="utf-8")

    entities_md = [
        "# Generated Home Assistant entity inventory",
        "",
        "Unique IDs and raw registry device IDs are intentionally omitted.",
        "",
        "| Entity ID | Platform | Name | Area | Device | Disabled |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for entity in sorted(
        (e for e in entities if isinstance(e, dict)),
        key=lambda e: str(e.get("entity_id", "")),
    ):
        device_id = entity.get("device_id")
        area = area_names.get(entity.get("area_id"), "") or device_area.get(device_id, "")
        name = entity.get("name") or entity.get("original_name") or ""
        entities_md.append(
            "| "
            + " | ".join(
                markdown_escape(x)
                for x in (
                    entity.get("entity_id", ""),
                    entity.get("platform", ""),
                    name,
                    area,
                    device_refs.get(device_id, ""),
                    entity.get("disabled_by") or "",
                )
            )
            + " |"
        )
    (output / "entities.md").write_text("\n".join(entities_md) + "\n", encoding="utf-8")

    counts = Counter(
        e.get("domain")
        for e in entries
        if isinstance(e, dict) and e.get("domain")
    )
    integrations_md = [
        "# Generated Home Assistant integration inventory",
        "",
        "Only integration domains and counts are exported. Config-entry titles, IDs and credential-bearing data are omitted.",
        "",
        "| Integration domain | Config entries |",
        "| --- | ---: |",
    ]
    for domain, count in sorted(counts.items()):
        integrations_md.append(f"| {markdown_escape(domain)} | {count} |")
    (output / "integrations.md").write_text("\n".join(integrations_md) + "\n", encoding="utf-8")

    report.counts.update(
        {
            "areas": len(area_names),
            "devices": len(device_rows),
            "entities": len(entities),
            "integration_entries": sum(counts.values()),
            "integration_domains": len(counts),
        }
    )


def export_custom_component_inventory(source_root: Path, repo_root: Path, report: ExportReport) -> None:
    source = source_root / "custom_components"
    output = repo_root / "inventory" / "generated-live" / "custom-components.md"
    rows: list[list[str]] = []
    if source.is_dir():
        for component in sorted(p for p in source.iterdir() if p.is_dir()):
            manifest = component / "manifest.json"
            data: dict[str, Any] = {}
            if manifest.is_file():
                try:
                    data = json.loads(manifest.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError):
                    data = {}
            rows.append(
                [
                    component.name,
                    data.get("name", ""),
                    data.get("version", ""),
                    data.get("documentation", ""),
                    data.get("issue_tracker", ""),
                ]
            )
    lines = [
        "# Generated custom-component inventory",
        "",
        "Only manifest metadata is exported. Third-party/custom integration source code is not copied automatically.",
        "",
        "| Directory/domain | Name | Version | Documentation | Issue tracker |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(markdown_escape(x) for x in row) + " |")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report.counts["custom_components"] = len(rows)


def export_esphome_inventory(source_root: Path, repo_root: Path, report: ExportReport) -> None:
    source = source_root / "esphome"
    output = repo_root / "inventory" / "generated-live" / "esphome-files.md"
    names: list[str] = []
    if source.is_dir():
        for path in sorted(source.rglob("*.yaml")):
            try:
                names.append(path.relative_to(source).as_posix())
            except ValueError:
                continue
    lines = [
        "# Generated ESPHome file inventory",
        "",
        "Only filenames are exported automatically. ESPHome YAML is excluded because it may contain Wi-Fi/API/OTA credentials or other device secrets.",
        "",
    ]
    lines.extend(f"- `{name}`" for name in names)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report.counts["esphome_yaml_files"] = len(names)


def export_text_configuration(source_root: Path, repo_root: Path, report: ExportReport) -> None:
    destination_root = repo_root / "home-assistant" / "live-export" / "configuration"
    destination_root.mkdir(parents=True, exist_ok=True)

    for filename in TOP_LEVEL_CONFIG_FILES:
        source = source_root / filename
        if source.is_file():
            copy_sanitized_text(source, destination_root / filename, source_root, report)

    for dirname in COPY_CONFIG_DIRS:
        source_dir = source_root / dirname
        if not source_dir.is_dir():
            continue
        for source in sorted(source_dir.rglob("*")):
            if not source.is_file() or source.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            if source.name.endswith(".bak"):
                continue
            relative = source.relative_to(source_dir)
            destination = destination_root / dirname / relative
            copy_sanitized_text(source, destination, source_root, report)


def write_dashboard_index(repo_root: Path, report: ExportReport) -> None:
    output = repo_root / "home-assistant" / "live-export" / "dashboards" / "README.md"
    lines = [
        "# Live dashboard export",
        "",
        "Generated from Home Assistant storage-mode Lovelace files. The `.storage` wrappers are not committed.",
        "",
        "| Source key | Dashboard | Views | Sections | Cards | Export bytes |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in report.dashboard_rows:
        lines.append(
            f"| `{row['source']}` | {markdown_escape(row['title'] or row['slug'])} | "
            f"{row['views']} | {row['sections']} | {row['cards']} | {row['bytes']} |"
        )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report.counts["dashboards"] = len(report.dashboard_rows)


def write_export_readme(repo_root: Path) -> None:
    output = repo_root / "home-assistant" / "live-export" / "README.md"
    text = """# Sanitized live Home Assistant export

This directory is generated by `tools/ha-export/export_home_assistant.py` from the mounted live Home Assistant `/config` share.

It is intentionally **not** a byte-for-byte backup of Home Assistant. It contains selected configuration and dashboard material that is useful for documentation/version control after conservative redaction.

Never use this directory as a substitute for a Home Assistant backup.

Excluded by design include secrets, `.storage` credential/authentication files, databases, logs, backups, certificates/keys, raw ESPHome configuration, Thread datasets, mobile-app/auth data and third-party custom-component source code.
"""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")


def write_report(repo_root: Path, source_root: Path, report: ExportReport) -> None:
    output = repo_root / "inventory" / "generated-live" / "EXPORT-REPORT.md"
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    lines = [
        "# Home Assistant export report",
        "",
        f"Generated: `{now}`",
        f"Source mount: `{source_root}`",
        "",
        "## Generated counts",
        "",
    ]
    for key, value in sorted(report.counts.items()):
        lines.append(f"- **{key.replace('_', ' ')}:** {value}")

    lines += ["", "## Copied/sanitized text configuration", ""]
    lines.extend(f"- `{item}`" for item in report.copied) or lines.append("- None")

    lines += ["", "## Redactions applied", ""]
    lines.extend(f"- {item}" for item in report.redactions) or lines.append("- None detected")

    lines += ["", "## Skipped items", ""]
    lines.extend(f"- {item}" for item in report.skipped) or lines.append("- None")

    lines += [
        "",
        "## Always excluded by design",
        "",
        "- `secrets.yaml`",
        "- `.storage/auth*`, `http.auth`, `mobile_app`, `person`",
        "- `.storage/thread.datasets`",
        "- `.storage/core.config_entries` raw contents (used only to count integration domains)",
        "- databases and WAL/SHM files",
        "- logs and fault logs",
        "- backups and ZIP/TAR archives",
        "- SSL/private keys/certificates",
        "- raw ESPHome YAML",
        "- raw custom-component source code",
        "- add-on/app credential stores",
        "",
        "## Review requirement",
        "",
        "This exporter is deliberately conservative, but generated files should still be reviewed before merging into a public repository.",
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def clear_previous_generated(repo_root: Path) -> None:
    for relative in (
        Path("home-assistant/live-export"),
        Path("inventory/generated-live"),
    ):
        target = repo_root / relative
        if target.exists():
            shutil.rmtree(target)


def main() -> int:
    parser = argparse.ArgumentParser(description="Export public-safe Home Assistant configuration")
    parser.add_argument("--source", default="/Volumes/config", help="Mounted Home Assistant config share")
    parser.add_argument("--repo", default=None, help="Repository root; defaults to two levels above this script")
    args = parser.parse_args()

    source_root = Path(args.source).expanduser().resolve()
    repo_root = (
        Path(args.repo).expanduser().resolve()
        if args.repo
        else Path(__file__).resolve().parents[2]
    )

    required = source_root / "configuration.yaml"
    storage = source_root / ".storage"
    if not required.is_file() or not storage.is_dir():
        raise SystemExit(
            f"Source does not look like a Home Assistant /config mount: {source_root}\n"
            "Expected configuration.yaml and .storage/."
        )

    git_dir = repo_root / ".git"
    if not git_dir.exists():
        raise SystemExit(f"Repository root does not contain .git: {repo_root}")

    report = ExportReport()
    clear_previous_generated(repo_root)
    write_export_readme(repo_root)
    export_text_configuration(source_root, repo_root, report)
    export_dashboards(source_root, repo_root, report)
    write_dashboard_index(repo_root, report)
    export_inventory(source_root, repo_root, report)
    export_custom_component_inventory(source_root, repo_root, report)
    export_esphome_inventory(source_root, repo_root, report)
    write_report(repo_root, source_root, report)

    print("Home Assistant export complete")
    print(f"Source: {source_root}")
    print(f"Repository: {repo_root}")
    print()
    for key, value in sorted(report.counts.items()):
        print(f"{key}: {value}")
    print(f"redactions: {len(report.redactions)}")
    print(f"skipped: {len(report.skipped)}")
    print()
    print("Review: inventory/generated-live/EXPORT-REPORT.md")
    print("Then run: git status --short")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
