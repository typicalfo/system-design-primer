---
title: "Federation"
summary: "Split databases by function so each domain has its own store and its own write path."
tags: [data, primer, federation]
when_to_use: "Use when different domains have different load or ownership, and joins across them can become application calls."
related:
  - sharding.md
  - denormalization.md
  - cqrs.md
last_reviewed: 2026-09-25
---

# Federation

## Problem

One database serves every domain, so unrelated features share a primary, a failover, and a migration window. Functional partitioning gives each domain its own store.

The System Design Primer covers the underlying idea in [Federation](../README.md#federation). This card is the operational form. The Primer prose is unchanged.

## When to use

- Domains are real (identity, billing, catalog) and owned by different teams or different SLOs.
- Cross-domain joins are infrequent.
- One table is not the entire load. If it is, shard that table instead.

## When not to use

- You still need strong transactions across the proposed split. Keep one database, or design a saga knowingly.
- The split is by table nickname with the same team and the same transaction. You added network calls for nothing.
- Operational maturity is one database backed up well. Two poorly backed-up databases are a downgrade.

## Tradeoffs

| You gain | You pay |
|---|---|
| Independent scaling and blast radius | Joins become calls or denormalized copies |
| A smaller blast radius for a bad migration | Distributed transactions or sagas |
| Clearer ownership | More backups, more connection pools, more failure modes |

## Failure modes

- A feature needs both databases and writes them independently. They diverge.
- An implicit join in a report is now a stale copy nobody owns.
- Identity of a user differs across stores.

## Implementation notes

- Draw the boundary where transactions already do not cross.
- Give each store an owner.
- Copy data across the boundary with an event or CDC, not with a shared table.
- The Primer notes federation fails when one function is huge. Shard that function.

## Related patterns

- [Sharding](sharding.md)
- [Saga](saga.md)
- [CQRS](cqrs.md)
