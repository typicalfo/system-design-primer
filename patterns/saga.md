---
title: "Saga"
summary: "Complete a business transaction as a series of local commits with explicit compensations."
tags: [data, consistency, workflow]
when_to_use: "Use when a user action updates several services that do not share a transaction."
related:
  - transactional-outbox.md
  - idempotency-keys.md
  - message-queues.md
  - ../enterprise/data/sagas.md
---

# Saga

## Problem

A checkout that charges a card, reserves stock, and creates a shipment cannot do those in one database transaction once the data is split. Two-phase commit across services couples their availability.

## When to use

- Each step can commit locally and can be retried safely.
- You can compensate or honestly queue the steps you cannot compensate.
- The business can show an in-progress state.

## When not to use

- The data is still in one database. Use a transaction.
- You cannot compensate and you also cannot tolerate the inconsistency. Redesign the boundary.
- The flow has no timeout. A lost message will leave it running forever.

## Tradeoffs

| Style | You gain | You pay |
|---|---|---|
| Choreography | No central brain. Services react to events | The overall state is hard to see. Cycles are easy to create |
| Orchestration | One place for timeouts, status, and branches | An orchestrator to operate and to keep from absorbing everyone's rules |

## Failure modes

- Compensation runs twice and refunds twice.
- Compensation fails permanently and nobody is paged.
- An irreversible step (email, shipment) runs before a step that often fails.
- The orchestrator crashes and the saga has no durable state.

## Implementation notes

- Make steps and compensations idempotent.
- Persist saga state.
- Put irreversible steps late.
- Time out and reconcile.
- Guide: [sagas](../enterprise/data/sagas.md).

## Related patterns

- [Transactional outbox](transactional-outbox.md)
- [Idempotency keys](idempotency-keys.md)
- [Event-driven guide](../enterprise/data/event-driven.md)
