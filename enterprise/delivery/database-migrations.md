---
title: "Database migrations and rollback"
summary: "Change schemas in expand and contract steps so the previous application version still runs, and so rollback does not require time travel."
tags: [delivery, migrations, database, rollback]
when_to_use: "Use when a release changes a table, index, or constraint that an older binary might still touch."
related:
  - cicd.md
  - progressive-delivery.md
  - ../data/schema-evolution.md
  - ../reliability/disaster-recovery.md
last_reviewed: 2026-09-25
---

# Database migrations and rollback

Application rollback is easy when the previous binary can still read and write the current schema. Expand/contract is how you keep that true. A migration that rewrites meaning in one step makes the previous binary wrong the moment it runs.

## Expand / contract

| Phase | Schema | Writers | Readers |
|---|---|---|---|
| Expand | Add the new column or table, nullable or defaulted, no read dependency | Still the old shape, or dual-write once the new binary is partially out | Old binary ignores the new column |
| Dual-write and backfill | Both shapes populated | New and old binaries write both, or a job backfills | Some reads move to the new shape after backfill checks pass |
| Contract | Old column unused | Only the new shape | Only the new shape |
| Drop | Later release removes the old column | New only | New only |

Do not combine drop with the release that starts the new write. Leave at least one release of slack so you can roll the binary back.

## Defaults

- Migrations are forward-only scripts in version control, applied by a job, not by whichever app instance starts first (unless you have exactly one writer and you like outages).
- A lock-heavy alter on a hot table is scheduled, batched, or done by a copy-and-swap. "It is fast on my laptop" is not a plan.
- Backfills are idempotent and throttled. They have a progress metric and a stop button.
- Constraints that reject old writers (a new `NOT NULL` with no default) land after every writer is new.
- Rollback of the app is redeploying the old digest while the expanded schema remains. Rollback of a destructive drop is a restore. Those are different runbooks.
- Data migrations and code deploys have an order written in the release note. The pipeline enforces it if you can.
- Test the migration on a production-shaped copy, including the time it takes.

## Decide

| Change | Safe with expand/contract | Needs extra care |
|---|---|---|
| Add nullable column | Yes | Backfill if readers will require it |
| Add index | Yes if the engine can build it without a long exclusive lock | Build concurrently where the engine allows |
| Rename column | No in place | Add new, copy, switch, drop old |
| Change type or units | No in place | New column, dual-write, convert |
| Delete a table | Only after a release that no longer reads it | Restore plan if you were wrong |

## Anti-patterns

- An ORM that "syncs" the schema on boot in production.
- A migration that cannot be rerun after a failure halfway through.
- Dropping a column in the same pull request as the code that stops using it, then rolling the code back.
- A unique index added before duplicate data is cleaned, failing the migrate in production only.
