---
title: "Circuit breaker"
summary: "Stop calling a dependency that is failing, fail fast for a cool-down, then try a few probes."
tags: [reliability, resilience]
when_to_use: "Use when a dependency can be down or slow and callers would otherwise pile up threads waiting on timeouts."
related:
  - retry-with-backoff.md
  - bulkhead.md
  - load-shedding.md
  - ../enterprise/reliability/circuit-breaker-bulkhead.md
---

# Circuit breaker

## Problem

Retries against a sick dependency multiply load and hold caller resources until every timeout fires. Callers need a way to stop.

## When to use

- The dependency has a history of partial failure.
- You can define a fallback: an error, a cached value, or a skipped optional feature.
- Timeouts alone still let too many callers wait.

## When not to use

- Failures are business errors such as 'not found'. Do not trip on those.
- The dependency is on the critical path and failing fast is worse than waiting, and waiting is still bounded. Rare. Usually fail fast.
- One breaker wraps every outbound host. A single bad host will open the world.

## Tradeoffs

| You gain | You pay |
|---|---|
| The dependency gets room to recover | Some calls fail immediately that might have succeeded |
| Callers stay available for other work | Tuning: too sensitive flaps, too loose never opens |
| A clear metric (open or closed) | Half-open probes can become a thundering herd if you allow too many |

## Failure modes

- The breaker opens and every client retries another replica together.
- State is per process and you have so many processes that each one never sees enough failures to open, while the dependency is drowning.
- The breaker stays open because probes are not allowed through.
- A shared breaker across endpoints trips checkout because search is down.

## Implementation notes

- States: closed, open, half-open.
- Trip on an error rate over a minimum volume.
- Pair with a timeout shorter than the user deadline and with a [bulkhead](bulkhead.md).
- When open, do not queue unbounded work.
- Expose the state to metrics.
- Details and defaults: [circuit breakers and bulkheads](../enterprise/reliability/circuit-breaker-bulkhead.md).

## Related patterns

- [Retry with backoff](retry-with-backoff.md)
- [Bulkhead](bulkhead.md)
- [Load shedding](load-shedding.md)
