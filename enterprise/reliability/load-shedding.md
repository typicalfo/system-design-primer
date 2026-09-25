---
title: "Load shedding"
summary: "Reject excess work early, with a clear retry signal, before the process collapses under queueing delay."
tags: [reliability, load-shedding, backpressure]
when_to_use: "Use when traffic can exceed capacity faster than you can scale, or when one class of request must be sacrificed to keep another alive."
related:
  - retries-timeouts.md
  - circuit-breaker-bulkhead.md
  - ../apis/rate-limiting.md
  - ../tenancy/noisy-neighbor.md
  - ../observability/slos.md
  - ../../patterns/rate-limiting.md
last_reviewed: 2026-09-25
---

# Load shedding

Shedding is a deliberate refusal. The alternative is a queue that grows until every request is slow, then times out, then retries, then makes the overload worse. A small system that returns `503` quickly is more available, in the SLO sense, than a large one that accepts work it cannot finish.

The Primer's back-pressure note (limit the queue, return busy, retry later) is the same idea. See [message queues](../../patterns/message-queues.md).

## Defaults

- Define overload on a signal you can measure in process: queue wait, event-loop lag, pool saturation, or max in-flight requests. CPU at 100% is a late signal.
- Shed at the edge, before you have spent a database transaction. Cheap rejection beats expensive failure.
- Priority: keep health checks and the core write path; shed reports, exports, and anonymous traffic first if the product agrees.
- Return `429` or `503` with `Retry-After`. Include a stable error code so clients can branch.
- Bound every queue. When full, reject the producer. Do not spill without a limit onto disk and call it durability.
- Autoscaling is the slow response. Shedding is the fast one. Use both. Scale-up that takes minutes does not save a 10-second stampede.
- Per-tenant caps shed the noisy tenant before the global shedder fires. See [noisy neighbors](../tenancy/noisy-neighbor.md).
- Load tests must show the shed point. A limiter you have never seen trip will trip wrong in production.

## Decide

| Overload source | Shed how |
|---|---|
| Too many legitimate users | Global in-flight limit plus autoscale; prioritize the core SLO |
| One tenant or token | Per-tenant limit; everyone else stays |
| Retry storm from your own clients | Retry budget and a breaker; shedding alone will oscillate if clients retry immediately |
| Expensive query shape | Separate concurrency cap on that route |
| Dependency slow, not you | Stop accepting work that needs it. Do not buffer unbounded "for later" |

## Checklist

- [ ] The maximum queue time is part of the latency budget, or the queue is bounded by count.
- [ ] Shed responses are excluded or labeled so they do not look like a mystery 500 in the SLO, and they are still visible.
- [ ] Clients back off. Your own jobs do too.
- [ ] A game day or a test has crossed the limit once.

## Anti-patterns

- An unbounded executor service in front of a database with a fixed pool.
- Shedding health checks first, so the orchestrator restarts you while you are merely busy.
- Accepting every request into a "pending" table that grows without a worker plan.
- Fairness math that is global across tenants when one integration is the entire spike.
