---
title: "Bulkhead"
summary: "Give each dependency or tenant a separate concurrency limit so one failure cannot take every thread."
tags: [reliability, isolation]
when_to_use: "Use when one process calls several dependencies or serves several tenants and a slow one must not exhaust the shared pool."
related:
  - circuit-breaker.md
  - rate-limiting.md
  - load-shedding.md
  - ../enterprise/reliability/circuit-breaker-bulkhead.md
last_reviewed: 2026-09-25
---

# Bulkhead

## Problem

A shared thread pool or connection pool lets the slowest dependency occupy every slot. The process is then up and unable to do unrelated work.

## When to use

- You can name the dependencies or tenant tiers worth isolating.
- You know a rough concurrency limit for each.
- Losing the isolated feature is better than losing the process.

## When not to use

- There is only one dependency and one kind of work. A single limit is just the pool size.
- You set the bulkhead larger than the dependency can handle. You only moved the queue.
- Isolation would require a separate cluster and the cost is not justified. A pool limit may be enough.

## Tradeoffs

| You gain | You pay |
|---|---|
| A contained blast radius | Capacity reserved for a dependency you might not be using |
| The rest of the process survives | More knobs to set wrong |
|  | Requests over the limit fail even if the machine looks idle |

## Failure modes

- Every bulkhead is sized to the full pool, so the sum can still oversubscribe the process.
- Queueing inside the bulkhead with no timeout recreates the stuck threads.
- A tenant bulkhead so small that normal traffic trips it.

## Implementation notes

- Separate connection pools or semaphores per dependency.
- Time out waiters.
- For tenants, fair-share or a cap. See [noisy neighbors](../enterprise/tenancy/noisy-neighbor.md).
- Metric: in-use and rejected per bulkhead.

## Related patterns

- [Circuit breaker](circuit-breaker.md)
- [Rate limiting](rate-limiting.md)
- [Load shedding](load-shedding.md)
