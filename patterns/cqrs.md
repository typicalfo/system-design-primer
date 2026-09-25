---
title: "CQRS"
summary: "Use a write model shaped for commands and a read model shaped for queries, updated asynchronously."
tags: [data, architecture]
when_to_use: "Use when the read shape and the write shape fight each other, and read staleness is acceptable."
related:
  - event-sourcing.md
  - denormalization.md
  - cdc.md
  - cache-invalidation.md
last_reviewed: 2026-09-25
---

# CQRS

## Problem

One model is asked to be both a normalized write schema and a screen-shaped query. Indexes and joins pile up, or writes get slow to keep every screen current.

## When to use

- Reads and writes have different shapes, scale, or authorization.
- You can name the maximum lag of the read model.
- The write model remains the source of truth.

## When not to use

- A simple CRUD form. One model is fine.
- The user must read their write from the query model immediately and you will not also read the write model for that case.
- You are splitting models because a diagram said CQRS, with no measured pain.

## Tradeoffs

| You gain | You pay |
|---|---|
| Read models that match queries | Lag and a projector to operate |
| Writes that do not carry every index | Dual models to change when the domain changes |
| Independent read scale | Clients surprised by stale reads unless you say so |

## Failure modes

- The projector stops and the read model quietly rots.
- Two projectors disagree and there is no rebuild story.
- Commands are validated against the stale read model and reject valid writes or accept invalid ones.
- The read model is treated as the only copy. It is not a cache. It is a bug.

## Implementation notes

- Keep commands on the write model.
- Build the read model from events, an outbox, or CDC.
- Make the projector rebuildable.
- For read-your-writes, query the write model for the caller's own recent change or return the command result directly.
- microservices.io documents this pattern and is all rights reserved. Link the catalog. Do not copy it.

## Related patterns

- [Event sourcing](event-sourcing.md)
- [CDC](cdc.md)
- [Denormalization](denormalization.md)
