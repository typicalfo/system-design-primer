---
title: "Change data capture"
summary: "Read committed row changes from the database log and stream them to other systems."
tags: [data, replication]
when_to_use: "Use when consumers need the committed row stream and you cannot add an outbox to every writer."
related:
  - transactional-outbox.md
  - event-sourcing.md
  - cqrs.md
  - ../enterprise/data/cdc.md
last_reviewed: 2026-09-25
---

# Change data capture

## Problem

Other systems need to follow a database they do not write: search indexes, warehouses, caches. Polling tables is late and heavy. Dual writes drift.

## When to use

- The database exposes a durable change log.
- The consumer wants row images, not a curated domain event. Or you CDC an outbox table of domain events.
- You can tolerate connector lag and can rebuild from a snapshot if the log expires.

## When not to use

- The downstream is an external API. Do not publish internal table rows as the public contract.
- You need intent the row does not contain ('user checked out' versus 'row updated').
- The team cannot operate a connector. A small outbox poller may be the better tool.

## Tradeoffs

| You gain | You pay |
|---|---|
| No extra write on the request path | A connector, log retention, and snapshot procedure |
| Committed changes only | Coupling to the internal schema |
| Deletes, if you emit them | Lag and a new failure domain |

## Failure modes

- Log retention expires before the consumer recovers, and the snapshot procedure was never written.
- Deletes are not emitted and the target keeps ghosts.
- A schema rename silently breaks the warehouse.
- The replication user is over-privileged and shared with humans.

## Implementation notes

- Snapshot, then stream from a stored position. Make apply idempotent.
- Monitor lag.
- Do not treat the raw stream as a public API.
- Guide: [CDC](../enterprise/data/cdc.md).

## Related patterns

- [Transactional outbox](transactional-outbox.md)
- [CQRS](cqrs.md)
- [Event sourcing](event-sourcing.md)
