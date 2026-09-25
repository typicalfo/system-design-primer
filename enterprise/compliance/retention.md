---
title: "Retention and deletion"
summary: "Give every store a retention period and a deletion path that includes indexes, vendors, and backups."
tags: [compliance, retention, deletion, backups]
when_to_use: "Use when data is stored for more than the request that created it, including logs, backups, and derived indexes."
related:
  - privacy.md
  - audit-logs.md
  - residency.md
  - ../tenancy/lifecycle.md
  - ../security/encryption-keys.md
  - ../data/governance.md
---

# Retention and deletion

Retention is how long you keep a class of data. Deletion is the mechanism that makes that sentence true. A policy page with no job is a backlog.

## Defaults

- Classify stores: system of record, derived index, debug log, security audit, backup, analytics. Each class has a duration and an owner.
- Default retention is the shortest period that meets the product and the legal hold you know about. Extend per tenant by contract, not by forgetting to delete.
- Delete by an idempotent job keyed on tenant, person, or age. The job records a completion marker. Re-running it is safe.
- Derived data dies too: search documents, caches, CDN objects, warehouse tables, ML feature rows, support-tool copies.
- Legal hold sets a flag that the deletion job honors for that scope only.
- Backups: prefer expiry aligned to the retention window. If a backup must outlive a deletion (short backup cycle versus immediate erasure), document that a restore can resurrect data, and mitigate with crypto-shred (destroy the tenant or record key) or with a post-restore scrub that runs before the restore is served.
- Tombstones: use them when you need to replicate "this was deleted" to other consumers. The tombstone should not contain the personal payload.
- Immutability and erasure conflict. An append-only event log that contains personal data needs encryption per person or tenant, redaction by crypto-shred, or a design that keeps personal data out of the immutable payload (store an id, keep the profile in a deletable table).

## Decide

| Situation | Prefer | Avoid |
|---|---|---|
| User asks to erase their profile | Delete the profile row and scrub references; keep invoices if finance policy says so, with the minimum fields | Waiting for the annual backup to expire while the live row remains |
| Tenant closes the account | The offboarding workflow in [lifecycle](../tenancy/lifecycle.md) | A manual runbook someone runs if they remember |
| Debug logs | Days to a few weeks, scrubbed | Same retention as the financial ledger |
| Security audit | The examination or contract window, minimal personal data | Editable application tables |
| Backup versus erase | Key destruction or post-restore scrub, stated in the design | Claiming both "instant erasure" and "seven-year full backups" with no mechanism |

## Checklist

- [ ] Every new store in a design names retention and the deletion mechanism.
- [ ] A drill deletes one test person and a search proves the name is gone from the index.
- [ ] Backup expiry or crypto-shred is tested, not assumed.
- [ ] A hold on tenant A does not stop deletion for tenant B.
- [ ] Caches cannot serve a deleted object for longer than a stated bound.

## Anti-patterns

- Soft-delete flags that readers inconsistently honor, with no physical purge.
- A warehouse that ingests the production changelog and never applies deletes.
- Object versioning left on, so "delete" writes a delete marker and keeps the bytes.
- Retention "forever" on a log pipeline because the default was unset.
