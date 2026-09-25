---
title: "Rate limiting"
summary: "Choose a limiter algorithm from whether bursts are allowed, and key it on the identity that should pay the cost."
tags: [api, rate-limiting, fairness]
when_to_use: "Use when a caller can send work faster than you intend to serve it, including your own jobs."
related:
  - gateways.md
  - ../reliability/load-shedding.md
  - ../tenancy/noisy-neighbor.md
  - ../cost/capacity.md
  - ../../patterns/rate-limiting.md
---

# Rate limiting

A rate limit is a fairness and cost control. Load shedding is what you do when the process is already in trouble. Limits should trip before the process is in trouble. Pattern card: [rate limiting](../../patterns/rate-limiting.md).

## Algorithms

| Algorithm | Behavior | Use when | Avoid when |
|---|---|---|---|
| Token bucket | Allows a burst up to the bucket size, then a steady refill | Interactive APIs where a short burst is fine | A burst of expensive work is exactly the outage |
| Leaky bucket | Smooths to a constant rate | You must protect a downstream that cannot burst | Clients need a legitimate spike (a user loading a page that fans out) |
| Fixed window | Counts per clock window | Rough caps, cheap to implement | Traffic at the window boundary can double (the end of one window plus the start of the next) |
| Sliding window | Counts over a rolling interval | You want fixed-window simplicity without the boundary spike | The extra storage for the window is not worth it at your scale. Token bucket is usually enough |

## Defaults

- Key by credential or tenant, plus the route class. Anonymous traffic can additionally key by IP. IP alone is wrong for authenticated APIs.
- Different limits for cheap reads, writes, and exports. One global number will be either too tight for reads or too loose for exports.
- Return `429` with `Retry-After` and a machine-readable code. Tell the client which limit, in words a customer integrator can act on.
- Enforce in one place per key or accept that two limiters can each allow the full budget. If you run many gateway replicas, the counter has to be shared or proportionally split. A local counter per replica multiplies the allowed rate by the replica count.
- Log limit breaches with the key and the route. They are an abuse signal and a capacity signal.
- Internal callers get their own key and limit. "Internal" with no limit is how a job takes the API down.
- When the limit store is down, choose explicitly: fail open for availability or fail closed for safety. Payments and auth endpoints often fail closed. A marketing read might fail open. Write it down.

## Checklist

- [ ] The most expensive endpoint has a limit you have load-tested.
- [ ] A single tenant cannot consume the global budget.
- [ ] Replica count does not silently multiply the allowance.
- [ ] Client SDKs you ship honor `Retry-After`.

## Anti-patterns

- Limiting only by IP, so one corporate NAT shares a budget and an attacker with a botnet does not.
- A limit so high it never trips before the database falls over.
- Returning `500` on limit so clients retry harder.
- Per-user limits with no per-tenant limit, so a tenant with many users is unlimited.
