---
title: "Data residency"
summary: "Pin a tenant's data, backups, and operator access to the regions the contract allows."
tags: [compliance, residency, multi-region]
when_to_use: "Use when a customer or a law requires data to stay in a country or region, or when you replicate across regions by default."
related:
  - privacy.md
  - retention.md
  - ../tenancy/routing.md
  - ../tenancy/data-and-keys.md
  - ../reliability/multi-region.md
  - ../data/governance.md
---

# Data residency

Residency means the copies live where you said they would. A read replica, a backup, a CDN cache, a support attachment, and a vendor subprocessors' region all count. "The primary is in Frankfurt" is incomplete if the warehouse is in another continent.

This page is an engineering checklist. Which law applies is a legal question. See [privacy](privacy.md).

## Defaults

- The tenant record stores an allowed region set. Routing refuses to place new data elsewhere. See [tenant routing](../tenancy/routing.md).
- Backups, snapshots, and secrets for that tenant stay inside the set. A cross-region backup for disaster recovery is a product decision you disclose, or you offer in-region DR only.
- Queues, search indexes, and object storage follow the same pin. A global search cluster is a residency bug.
- CDN and edge caches do not hold personal data or authenticated responses, unless the edge location is inside the allowed set and the cache key is tenant-bound.
- Operator access from outside the region is a data flow. A support tool that copies rows to a US ticketing system is a transfer. Prefer remote query inside the region with exported aggregates that are not personal.
- Subprocessors are region-pinned or absent for that tenant. A status-page vendor is fine. A session-replay vendor that stores DOM content might not be.
- Replication topology is documented per store. "Multi-region active-active" and "EU-only" conflict unless the active regions are both in the allowed set.
- Moving a tenant between regions is offboarding plus onboarding with an export, not a silent replica promotion.

## Decide

| Requirement | Architecture that matches | Architecture that does not |
|---|---|---|
| Data stays in region R | Primary, replicas, backups, keys, and the search index in R | Primary in R, nightly snapshot copied to a global archive bucket |
| Fail over without leaving R | Two zones or two regions inside R | One region in R and a warm standby on another continent |
| No personal data at the edge | Cache static assets only | Cache API responses that include names or documents |
| Processing only in R | Workers in R | A central "global worker" that pulls jobs from every region |

## Checklist

- [ ] For one regulated tenant, you can list every store and vendor that holds their data and the region of each.
- [ ] A misrouted write is rejected, not repaired after the fact.
- [ ] Logs that contain personal data are regional. Central observability either stays in-region or receives redacted telemetry.
- [ ] A restore drill uses backups from the allowed region.
- [ ] The contract's region list matches the tenant record's allowed set.

## Anti-patterns

- Enabling a cloud feature that replicates "for durability" across regions by default and not reading the setting.
- Shipping full request logs to a single global vendor account.
- Using a worldwide LLM API to summarize customer documents without a regional processing story.
- Assuming encryption removes residency obligations. It usually does not. Ask counsel; do not decide it in a design doc.
