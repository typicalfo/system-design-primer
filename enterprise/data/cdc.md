---
title: "Change data capture"
summary: "Stream committed database changes from the log when consumers need the row-level history the database already committed."
tags: [data, cdc, replication]
when_to_use: "Use when another system must follow committed changes and you cannot or should not add an outbox to every write path."
related:
  - transactional-outbox.md
  - event-driven.md
  - schema-evolution.md
  - warehouse-lakehouse.md
  - ../../patterns/cdc.md
  - ../../patterns/transactional-outbox.md
last_reviewed: 2026-09-25
---

# Change data capture

CDC reads the database's commit log (or an equivalent change stream) and emits inserts, updates, and deletes in commit order per key. The database is already the source of truth. CDC does not invent a second write in the request path.

Pattern card: [CDC](../../patterns/cdc.md).

## Decide

| Choose | Use when | Avoid when |
|---|---|---|
| Log-based CDC | The engine exposes a durable log (WAL, binlog, change stream) and you need committed rows | You need a domain event that is not "this row changed." An outbox carries intent. A row image does not |
| Outbox plus CDC | You want transactional domain events and a log reader instead of polling | The team cannot operate the connector. A simple poller on a small outbox is enough |
| Triggers that write a shadow table | The engine has no usable log | You can use the log. Triggers add write latency and fail in creative ways |
| Dual write from the app | Never as the CDC substitute | Always. It will diverge |

## Defaults

- Snapshot plus stream: new consumers need an initial copy, then the log from a recorded position. Document how the snapshot and the stream meet so you do not miss or double-apply without an idempotent consumer.
- Ordering is per primary key, not global across tables.
- Deletes must be delivered. A replica that only upserts will resurrect nothing, but it will also never forget a row the source deleted.
- The connector identity is a workload identity. The replication user can read the log and cannot be a human's daily login.
- Schema changes are coordinated with the stream. Adding a nullable column is usually safe. Renaming a column is a break. See [schema evolution](schema-evolution.md).
- Lag is a metric with an SLO if a user-visible projection depends on it.
- Do not expose the raw internal table stream as a public API. Put a versioned event in front of external consumers. Internal analytical pipelines can land raw CDC in a bronze area. See [warehouse and lakehouse](warehouse-lakehouse.md).

## Checklist

- [ ] You know the log retention. If the consumer falls behind past retention, the recovery is a new snapshot, and that procedure is written.
- [ ] A consumer can restart without corrupting state (idempotent apply, or transactional offset plus apply).
- [ ] High-volume tables are not accidentally included. CDC of a heartbeat table will dominate the stream.
- [ ] Tenant predicates or row filters are explicit if the downstream zone is not allowed to hold every tenant.

## Anti-patterns

- CDC straight into another service's tables with no owner and no version.
- Treating log order across two tables as a transaction boundary the consumer can ignore. Multi-table transactions need a story.
- Using CDC to bypass an API so a team can read another team's private schema. That coupling is the cost.
- No alert on connector failure, discovered when the warehouse is a week stale.
