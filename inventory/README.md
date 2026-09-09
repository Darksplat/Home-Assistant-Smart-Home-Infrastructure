# Infrastructure Inventory

This directory is the authoritative **public-safe inventory** for the Home Assistant installation and the infrastructure that supports it.

The inventory records the role, hardware type, protocol, Home Assistant relationship and documentation status of each important subsystem. It intentionally excludes credentials, authentication tokens, unnecessary serial numbers, personal information and other data that should not be published.

## Inventory files

- [`system-inventory.md`](system-inventory.md) — master inventory of the known smart-home systems, infrastructure and integrations.

## Inventory policy

Each item should eventually record:

- system or device role;
- manufacturer/model where useful;
- communication method or protocol;
- Home Assistant integration path;
- relevant dashboards and automations;
- related standalone repository, if applicable;
- deployment status;
- documentation status;
- known limitations or outstanding work.

## Status terminology

| Status | Meaning |
|---|---|
| **Deployed** | Present in the working home installation. |
| **Field tested** | Behaviour has been confirmed on the installed hardware. |
| **Partial** | Present and working, but documentation or functionality is incomplete. |
| **Legacy** | Previously used and retained only for migration/history. |
| **Planned** | Intended work that is not yet fully deployed. |
| **Needs verification** | Known from prior work, but a current live-system check is still required before treating it as authoritative. |

## Private installation data

The public repository should not become a credential store or an unrestricted copy of the live Home Assistant `/config` directory.

Private addressing, MAC addresses, access tokens, passwords and other installation-specific data should only be published where there is a clear technical reason and the information has been reviewed for public disclosure.
