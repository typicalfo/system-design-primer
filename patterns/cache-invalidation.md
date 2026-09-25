---
title: "Cache invalidation"
summary: "Define who may overwrite or delete a cached entry and the maximum staleness a caller can observe."
tags: [caching, primer, consistency]
when_to_use: "Use whenever a cache or derived index exists. Invalidation is part of adopting the cache, not a follow-up."
related:
  - cache-aside.md
  - write-through.md
  - write-behind.md
  - cdn.md
---

# Cache invalidation

## Problem

Caches diverge from the source of truth. Something has to bound that divergence, or the cache becomes a second, accidental source of truth.

The System Design Primer covers the underlying idea in [When to update the cache](../README.md#when-to-update-the-cache). This card is the operational form. The Primer prose is unchanged.

## When to use

- You ship any cache, CDN response, or search projection.
- Callers can name how stale a read may be.
- You can name the writer that is allowed to change the underlying object.

## When not to use

- You cannot identify the key from the write. Caching a query whose invalidation set you do not know is the problem. Cache a smaller object instead.
- You need strong reads. Skip the cache on that path.

## Tradeoffs

| Approach | Staleness | Cost |
|---|---|---|
| TTL only | Up to the TTL, longer if the clock is wrong | Simple, imprecise |
| Delete on write | Bounded by delete failures and races | A missed delete serves stale data until TTL |
| Version or generation on the key | Readers ignore older generations | Extra coordination |
| Rebuild the projection from the log | Lag of the consumer | Operable if the projection is disposable |

## Failure modes

- Delete is lost and the TTL is long. Readers see old authorization or old prices.
- Writer updates the store, then deletes the cache, while a concurrent reader fills the cache with the old value. Order the fill so a newer write wins, or use a version.
- Invalidating by prefix on a shared cache locks or storms.
- CDN and app cache have different TTLs and nobody owns the longer one.

## Implementation notes

- Write the staleness budget next to the cache in the design.
- Always set a TTL as a backstop.
- Include tenant id in the key so invalidation cannot target another tenant by mistake, and so a missed tenant prefix cannot be broad.
- If the entry can be rebuilt entirely from the store, say so and treat a flush as safe.
- Do not invalidate by flushing the entire cache in production except as a break-glass with a stampede plan.

## Related patterns

- [Cache-aside](cache-aside.md)
- [CDN](cdn.md)
- [CQRS](cqrs.md)
