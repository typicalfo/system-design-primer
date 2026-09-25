---
title: "Load shedding"
summary: "Reject new work when the service is past a defined saturation point so accepted work can finish."
tags: [reliability, backpressure]
when_to_use: "Use when traffic can exceed capacity faster than scaling can react."
related:
  - rate-limiting.md
  - bulkhead.md
  - circuit-breaker.md
  - message-queues.md
  - ../enterprise/reliability/load-shedding.md
last_reviewed: 2026-09-25
---

# Load shedding

## Problem

A service that accepts every request queues them inside itself. Latency goes to the timeout, retries start, and throughput collapses.

## When to use

- You can measure overload in process (queue wait, in-flight, pool saturation).
- Some requests are more important than others, or all requests are equal and a fast `503` is better than a slow `500`.
- Clients honor backoff.

## When not to use

- You have not set a limit and are shedding at random CPU spikes. Fix the signal.
- The work is already accepted (a queue of record). Shedding new submits is still right. Dropping accepted durable work needs a product decision.
- Shedding is your only capacity plan. Also scale and also limit.

## Tradeoffs

| You gain | You pay |
|---|---|
| The process stays alive and latency stays bounded | Some users get a deliberate error |
| A chance for autoscaling to catch up | Clients that retry wrong will oscillate |
| Protection of the core path if you shed low priority first | Tuning the threshold |

## Failure modes

- Shedding health checks and getting restarted by the orchestrator.
- A threshold so high it trips after you are already stuck.
- No `Retry-After`, so clients hammer.
- Global shed triggered by one tenant.

## Implementation notes

- Shed based on a local saturation signal.
- Protect health checks and the core SLO path.
- Return `429` or `503` with `Retry-After`.
- Cap queues.
- Guide: [load shedding](../enterprise/reliability/load-shedding.md).

## Related patterns

- [Rate limiting](rate-limiting.md)
- [Bulkhead](bulkhead.md)
- [Message queues](message-queues.md)
