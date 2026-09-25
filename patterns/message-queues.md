---
title: "Message queues and async processing"
summary: "Accept work onto a durable queue and let a worker finish it after the user request returns."
tags: [messaging, primer, async]
when_to_use: "Use when the user does not need the result to complete the action, and the work must survive a process crash."
related:
  - transactional-outbox.md
  - retry-with-backoff.md
  - idempotency-keys.md
  - saga.md
  - load-shedding.md
---

# Message queues and async processing

## Problem

Doing the work inline makes the request slow or fragile. A queue moves the work off the request. The queue then becomes part of correctness.

The System Design Primer covers the underlying idea in [Message queues](../README.md#message-queues). This card is the operational form. The Primer prose is unchanged.

## When to use

- The user can be told 'accepted' and see completion later.
- You need retries, smoothing, or a worker pool separate from the web tier.
- The job is idempotent or transactional with the side effect.

## When not to use

- The caller needs the answer now and the work is cheap. The queue adds latency and a failure mode.
- You are using an in-memory buffer as if it were durable. The Primer's warning about Redis as a broker still applies: a crash can drop jobs.
- Ordering across all users is a requirement. That forces one partition.

## Tradeoffs

| You gain | You pay |
|---|---|
| A short user path | At-least-once delivery in most managed queues |
| Smoothing and retries | Operational surface: depth, poison messages, and lag |
| Independent worker scaling | The request's success is no longer the job's success. You need a status |

## Failure modes

- Duplicate delivery causes double charges or double emails unless the consumer is idempotent.
- A poison message blocks a partition, or is skipped and silently lost, depending on the configuration you forgot to set.
- The queue grows without a cap and delay becomes the outage.
- A worker dies after the side effect and before ack, and the retry repeats the side effect.

## Implementation notes

- Prefer a durable log or a managed queue when the job must not disappear.
- Bound depth. Past the cap, return a busy status and retry with backoff. That is the Primer's back-pressure note.
- Carry an idempotency key and a tenant id.
- Dead-letter after a capped number of attempts and alert.
- For replay and many independent consumers, use a log. For one worker pool, a queue is enough.
- Celery-style task queues are a library on top of a broker. The broker's durability is what matters, not the library.

## Related patterns

- [Transactional outbox](transactional-outbox.md)
- [Retry with backoff](retry-with-backoff.md)
- [Idempotency keys](idempotency-keys.md)
- [Saga](saga.md)
