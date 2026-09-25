---
title: "Retry with backoff"
summary: "Repeat a failed idempotent call with exponential delay and jitter, and stop at a budget."
tags: [reliability, retries]
when_to_use: "Use when a call can fail transiently and repeating it does not double the side effect."
related:
  - circuit-breaker.md
  - idempotency-keys.md
  - message-queues.md
  - ../enterprise/reliability/retries-timeouts.md
last_reviewed: 2026-09-25
---

# Retry with backoff

## Problem

Networks drop calls and dependencies restart. A single attempt makes those blips user-visible. Unbounded immediate retries make them an outage.

## When to use

- The operation is idempotent or protected by an idempotency key.
- The error is a timeout, a connection reset, or an explicit overload response.
- You have a deadline so retries stop.

## When not to use

- The error is a validation or authorization failure.
- The call reserves money or sends a message and you have no idempotency key.
- The dependency is already overloaded. Retrying adds load. Open the circuit and shed instead.

## Tradeoffs

| You gain | You pay |
|---|---|
| Fewer user-visible blips | Extra load on the dependency |
| Clients spread out if you add jitter | Tail latency grows with the retry budget |
|  | Layers of retries (browser, gateway, service) multiply |

## Failure modes

- Synchronized retries: every client backs off to the same second and you get waves.
- Retrying a write that partially succeeded.
- A retry budget larger than the user's patience, so the user retries too.
- Ignoring `Retry-After`.

## Implementation notes

- Exponential backoff with full jitter: sleep `random(0, min(cap, base * 2^attempt))`.
- Cap attempts and total time.
- Retry budgets (only a fraction of calls may be retries).
- Propagate deadlines.
- Guide: [retries and timeouts](../enterprise/reliability/retries-timeouts.md).

## Related patterns

- [Idempotency keys](idempotency-keys.md)
- [Circuit breaker](circuit-breaker.md)
- [Rate limiting](rate-limiting.md)
