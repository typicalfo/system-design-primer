---
title: "Cache-aside"
summary: "The application reads the cache, and on a miss loads the store and fills the cache."
tags: [caching, primer]
when_to_use: "Use when reads repeat, the source of truth is a database, and a short staleness window is acceptable."
related:
  - write-through.md
  - write-behind.md
  - cache-invalidation.md
  - refresh-ahead.md
---

# Cache-aside

## Problem

A hot read path hits the database for the same object over and over. You want the database to stay the source of truth and the cache to be optional.

The System Design Primer covers the underlying idea in [Cache-aside](../README.md#cache-aside). This card is the operational form. The Primer prose is unchanged.

## When to use

- The object has a natural id and is read many times between writes.
- You can name the maximum staleness a caller may see.
- A cold cache must still be correct, because the database is readable.

## When not to use

- The write must be visible to the next read in the same request with no extra delete logic you are willing to write.
- The cached object is so large or so unique that the hit rate will not pay for the hop.
- You need the cache itself to be durable. It will not be.

## Tradeoffs

| You gain | You pay |
|---|---|
| Database load drops for repeated reads | A miss is a cache hop plus a database hop plus a fill |
| Cache can be emptied without data loss | Writes to the database do not update the cache unless you delete or overwrite the key |
| Simple failure mode (treat cache errors as misses) | A stampede on a popular miss can overload the database |

## Failure modes

- Cache stampede: many misses at once rebuild the same key. Coalesce or lock the rebuild.
- Stale reads after a write until TTL or explicit invalidation. See [cache invalidation](cache-invalidation.md).
- A wrong cache key (missing tenant id) leaks data across tenants.
- Caching a failed lookup without a short TTL turns a blip into a sticky outage.

## Implementation notes

- Key the entry by tenant and id.
- Set a TTL even if you also delete on write. The delete will be missed someday.
- On cache error, read the database. Do not fail the user request because the cache is down, unless you have decided the cache is mandatory capacity.
- Prefer caching the object, not an entire query string. The Primer's query-cache warning still holds.
- Negative caching, if you use it, has its own short TTL.

## Related patterns

- [Write-through](write-through.md)
- [Write-behind](write-behind.md)
- [Cache invalidation](cache-invalidation.md)
- [Refresh-ahead](refresh-ahead.md)
