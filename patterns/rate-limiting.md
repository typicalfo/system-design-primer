---
title: "Rate limiting"
summary: "Count or meter requests per identity and reject the excess before the service is overloaded."
tags: [api, fairness, reliability]
when_to_use: "Use when a caller, tenant, or job can submit work faster than its allowance."
related:
  - load-shedding.md
  - bulkhead.md
  - retry-with-backoff.md
  - ../enterprise/apis/rate-limiting.md
last_reviewed: 2026-09-25
---

# Rate limiting

## Problem

Without a limit, one client determines everyone else's latency and cost. Limits express the allowance before the process is on fire. Shedding is the last resort when it is already on fire.

## When to use

- The cost of a request is roughly predictable for that route class.
- You can key the limit on a credential or tenant.
- Clients can slow down when told.

## When not to use

- You need to protect a resource whose cost varies by a factor of a thousand per call. Add a concurrency or payload cap, not only a request count.
- The limit is enforced independently on each replica with a full budget, so the real limit is N times larger.
- You have no story for the limiter store being down.

## Tradeoffs

| Algorithm | Burst | Boundary behavior |
|---|---|---|
| Token bucket | Up to the bucket | Steady refill after |
| Leaky bucket | Smoothed away | Constant outflow |
| Fixed window | Depends | Double spike at the boundary |
| Sliding window | Configurable | Smoother than fixed, more state |

## Failure modes

- IP-only keys lock out a NAT or fail to see a botnet.
- Limits so high they never bind before the database does.
- `500` responses on limit, which clients retry immediately.
- A global limit consumed by one tenant.

## Implementation notes

- Key by tenant or token, with a separate anonymous IP limit.
- Return `429` and `Retry-After`.
- Share the counter or split the budget by replica count.
- Different numbers for reads, writes, and exports.
- Guide: [rate limiting](../enterprise/apis/rate-limiting.md).

## Related patterns

- [Load shedding](load-shedding.md)
- [Bulkhead](bulkhead.md)
- [Retry with backoff](retry-with-backoff.md)
