---
title: "Idempotency keys"
summary: "Store the result of a write under a client-supplied key so a retry returns the same result and does not repeat the effect."
tags: [api, data, reliability]
when_to_use: "Use when a client or a worker may send the same write more than once."
related:
  - retry-with-backoff.md
  - transactional-outbox.md
  - message-queues.md
  - saga.md
  - ../enterprise/data/idempotency.md
last_reviewed: 2026-09-25
---

# Idempotency keys

## Problem

At-least-once delivery and timeouts create duplicates. The second request must not charge, ship, or insert a second time, and the caller still needs the original answer.

## When to use

- The client can generate a unique key per logical operation and send it again on retry.
- The side effect is not naturally unique, or you also need to replay the HTTP response.
- Concurrent duplicates are possible.

## When not to use

- A conditional update (`WHERE status = 'packed'`) already makes the transition idempotent and you do not need the original response body.
- The key includes a timestamp, so retries look new.
- You store the key in memory only.

## Tradeoffs

| You gain | You pay |
|---|---|
| Safe retries | A store of keys, hashes, and responses |
| A clear conflict if the same key is reused with a different body | TTL tuning: too short duplicates, too long fills storage |
|  | A careful transaction so two racers cannot both run the effect |

## Failure modes

- Key expires while the downstream provider is still retrying the callback.
- Same key, different body, and you run the second body anyway.
- Lookup without tenant id returns another tenant's response.
- `in_progress` stuck forever after a crash, blocking retries.

## Implementation notes

- Scope keys by tenant and operation.
- Store a hash of the canonical request.
- Same key and same hash returns the stored response. Different hash returns `409`.
- Commit the key with the side effect, or use `in_progress` then `completed`.
- Guide: [idempotency](../enterprise/data/idempotency.md).

## Related patterns

- [Retry with backoff](retry-with-backoff.md)
- [Transactional outbox](transactional-outbox.md)
- [Saga](saga.md)
