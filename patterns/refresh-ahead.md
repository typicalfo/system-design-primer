---
title: "Refresh-ahead"
summary: "The cache reloads a hot entry before its TTL expires so the next reader does not pay for a miss."
tags: [caching, primer]
when_to_use: "Use when a small set of keys is predictably hot and a miss would spike latency."
related:
  - cache-aside.md
  - cache-invalidation.md
  - ../enterprise/data/caching-at-scale.md
last_reviewed: 2026-09-25
---

# Refresh-ahead

## Problem

TTL expiry on a popular key turns into a synchronous rebuild on the user path. Refresh-ahead reloads that key just before it expires.

The System Design Primer covers the underlying idea in [Refresh-ahead](../README.md#refresh-ahead). This card is the operational form. The Primer prose is unchanged.

## When to use

- You can predict which keys are hot.
- The reload is safe to do slightly early.
- Extra store reads are cheaper than a user-facing miss.

## When not to use

- The key set is large and unpredictable. You will refresh keys nobody reads.
- The value must not be refreshed early because it is a security or entitlement decision that must expire on time.
- The store is already overloaded. Refresh-ahead adds reads.

## Tradeoffs

| You gain | You pay |
|---|---|
| Fewer user-facing misses on hot keys | Extra load when the prediction is wrong |
| Smoother latency | A bug in refresh can stampede the store on a timer |

## Failure modes

- Refresh storms when many keys expire together. Jitter the refresh time.
- A refresh that fails leaves the key to expire into a miss anyway. Keep a stale-while-error policy only if the product allows it.
- Refreshing a key that was deleted resurrects it. Check the store's answer.

## Implementation notes

- Jitter TTLs.
- Refresh a fraction of traffic early rather than all keys on one clock.
- Combine with cache-aside so a missed prediction still works.

## Related patterns

- [Cache-aside](cache-aside.md)
- [Cache invalidation](cache-invalidation.md)
