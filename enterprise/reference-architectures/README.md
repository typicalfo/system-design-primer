---
title: "Reference architectures"
summary: "Five end-to-end designs with requirements, estimates, a diagram, tradeoffs, and a severity-ranked design review."
tags: [reference-architecture, index]
when_to_use: "Use when you want a worked design to compare against, not a blank template."
related:
  - multi-tenant-b2b-saas.md
  - event-driven-orders.md
  - internal-platform.md
  - data-platform.md
  - rag-assistant.md
  - ../../templates/design-doc.md
  - ../../pack/skills/design-reviewer/checklist.md
  - ../../pack/examples/multi-tenant-audit-log/README.md
last_reviewed: 2026-09-25
---

# Reference architectures

These are designs, not running systems. Each one states requirements, shows the arithmetic, picks components, and then records a design-review pass that disagrees with the design in specific places. A review that only restates the design is not using the [checklist](../../pack/skills/design-reviewer/checklist.md).

| Design | What it is for |
|---|---|
| [Multi-tenant B2B SaaS](multi-tenant-b2b-saas.md) | Pooled work management with a bridge tier, SSO, and webhooks |
| [Event-driven orders and payments](event-driven-orders.md) | Checkout saga across payments and inventory |
| [Internal platform with SSO and audit](internal-platform.md) | A control plane for deploys, ownership, and tamper-evident audit |
| [Data platform](data-platform.md) | CDC into a lakehouse with classification and deletion |
| [Multi-tenant RAG assistant](rag-assistant.md) | Pooled assistant over each tenant's documents, with filtered retrieval and citations |

Smaller worked example, from the skills pack: [multi-tenant audit log](../../pack/examples/multi-tenant-audit-log/README.md).
