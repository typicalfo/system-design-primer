---
title: "Event sourcing"
summary: "Store the state of an aggregate as an append-only sequence of domain events and derive current state by fold."
tags: [data, events]
when_to_use: "Use when you must keep the history of changes itself, not only the latest row, and you can operate projections."
related:
  - cqrs.md
  - cdc.md
  - transactional-outbox.md
  - ../enterprise/compliance/audit-logs.md
last_reviewed: 2026-09-25
---

# Event sourcing

## Problem

A row update destroys the previous state. Some domains (ledgers, audit, collaborative editing) need the history as the source of truth.

## When to use

- The business already thinks in events.
- You need to rebuild projections or answer 'how did this get here'.
- You have a snapshot strategy so rebuilds do not replay from the beginning of time on every read.

## When not to use

- The domain is plain CRUD and the 'history' need is an audit log beside an ordinary row. Store the row and the audit. Do not event-source the whole service.
- You cannot migrate a badly modeled event. Events last forever.
- External side effects run inside the fold. They will rerun on replay.

## Tradeoffs

| You gain | You pay |
|---|---|
| A real history and rebuildable projections | Event versioning forever |
| A natural outbox if consumers read the same log | Snapshots, upcasters, and a stricter modeling discipline |
|  | Temptation to put secrets and personal data into an immutable log |

## Failure modes

- A poisonous event blocks the fold of one aggregate.
- Replay re-sends emails.
- Personal data cannot be deleted because it is in the log. Plan crypto-shred or keep personal data out of the event payload.
- Consumers couple to internal events with no versioning.

## Implementation notes

- Events are past-tense and immutable. Fix a bug with a new event, not an edit.
- Snapshot periodically.
- Side effects live in projectors with their own idempotency.
- Version events from day one.
- An audit log can be event-sourced without event-sourcing the whole domain. See [audit logs](../enterprise/compliance/audit-logs.md).

## Related patterns

- [CQRS](cqrs.md)
- [Transactional outbox](transactional-outbox.md)
- [CDC](cdc.md)
