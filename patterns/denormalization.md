---
title: "Denormalization"
summary: "Store a copy of a field next to the data that reads it, so a hot path does not join."
tags: [data, primer]
when_to_use: "Use when a measured read path is too slow or too frequent because of a join, and you can name how the copy stays fresh."
related:
  - federation.md
  - cqrs.md
  - cache-aside.md
  - cache-invalidation.md
last_reviewed: 2026-09-25
---

# Denormalization

## Problem

The normalized schema is correct and the join is too expensive at the read rate you actually have.

The System Design Primer covers the underlying idea in [Denormalization](../README.md#denormalization). This card is the operational form. The Primer prose is unchanged.

## When to use

- You have measured the join, not guessed it.
- The copied value changes rarely, or you have an invalidation path.
- The read path is on the critical latency budget.

## When not to use

- Writes update the value constantly and readers need it transactionally consistent.
- You are denormalizing in advance of a problem. Keep the join.
- The copy would become a second source of truth with no owner.

## Tradeoffs

| You gain | You pay |
|---|---|
| Faster reads, fewer joins | Writes must update every copy |
| A read model that matches the screen | Stale copies and repair jobs |
|  | More storage and a harder schema change |

## Failure modes

- One copy updates and the other does not. Users see two prices.
- A backfill misses rows and the bug lasts until someone counts.
- Cascading updates fan out and the write path becomes the incident.

## Implementation notes

- List every copy in the design.
- Update copies in the same transaction when they share a database. Across databases, use an event and accept lag.
- A periodic reconciliation catches missed updates.
- The Primer's guidance stands: denormalize when the read ratio makes the join too expensive, not by habit.

## Related patterns

- [Federation](federation.md)
- [CQRS](cqrs.md)
- [Cache invalidation](cache-invalidation.md)
