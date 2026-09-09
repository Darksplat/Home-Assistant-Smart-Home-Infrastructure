# Repository audit tools

Small standard-library checks used to keep the public Home Assistant repository maintainable and rebuild-ready.

## Markdown link audit

Run from the repository root:

```bash
python3 tools/repo-audit/check_markdown_links.py --repo .
```

The checker validates relative Markdown links while ignoring external URLs, anchors and fenced code blocks.

A clean run ends with:

```text
Broken relative links: 0
```

## Dashboard frontend dependency audit

Run:

```bash
python3 tools/repo-audit/dashboard_dependencies.py --repo .
```

It scans the public JSON Lovelace exports and writes:

```text
inventory/generated-live/FRONTEND-DEPENDENCIES.md
```

The export workflow also runs this audit automatically after the public-safety pass, so each refreshed live snapshot records the custom frontend components referenced by the public dashboards.

## Scope

These scripts do not contact Home Assistant and do not modify the live Samba share. They operate only on the repository checkout.
