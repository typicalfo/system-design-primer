---
title: "Transactional outbox"
summary: "Commit the business write and the outbound message in one database transaction, then publish asynchronously."
tags: [data, messaging]
when_to_use: "Use when you must update your database and notify another system without a dual write."
related:
  - message-queues.md
  - cdc.md
  - idempotency-keys.md
  - saga.md
  - ../enterprise/data/transactional-outbox.md
last_reviewed: 2026-09-25
---

# Transactional outbox

## Problem

Publishing after commit can crash in between. Publishing before commit can emit a message for a transaction that rolls back. Either hole corrupts downstream state.

## When to use

- The business write and the message share a database that has transactions.
- Consumers can dedupe.
- A small lag between commit and publish is acceptable.

## When not to use

- You need the broker ack before you respond to the user. The outbox responds after the database commit. Say so if that is not enough, and design a different wait.
- The message belongs to a different database than the write. Then it is not one transaction.
- Volume is a full table CDC problem and you do not control the write path. Use CDC on the tables you have.

## Tradeoffs

| You gain | You pay |
|---|---|
| No lost message and no ghost message relative to the commit | A publisher to operate, and lag to alert on |
| Normal database tools for the pending messages | At-least-once publish. Consumers still dedupe |
|  | Outbox growth if the publisher stalls |

## Failure modes

- Publisher marks the row published before the broker accepts.
- Two publishers send duplicates. Consumers must still dedupe. Publishers should also lease rows.
- A poison payload blocks the whole table because you did not partition by aggregate.
- The outbox is in a second database.

## Implementation notes

- Insert the outbox row in the same transaction as the business change.
- Publish, then mark, and tolerate republish.
- Alert on the age of the oldest unpublished row.
- Prune published rows.
- Guide: [transactional outbox](../enterprise/data/transactional-outbox.md).

## Related patterns

- [CDC](cdc.md)
- [Message queues](message-queues.md)
- [Idempotency keys](idempotency-keys.md)
