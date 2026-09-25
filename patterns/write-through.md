---
title: "Write-through"
summary: "The application writes the cache and the cache writes the store before the write returns."
tags: [caching, primer]
when_to_use: "Use when reads must see the latest write and you can spend latency on the write path."
related:
  - cache-aside.md
  - write-behind.md
  - cache-invalidation.md
  - ../enterprise/data/caching-at-scale.md
last_reviewed: 2026-09-25
---

# Write-through

## Problem

Cache-aside leaves a window where the database is newer than the cache. Some reads cannot tolerate that window, and you still want the cache populated for the next read.

The System Design Primer covers the underlying idea in [Write-through](../README.md#write-through). This card is the operational form. The Primer prose is unchanged.

## When to use

- The same objects are read immediately after they are written.
- Write latency can include a synchronous database write.
- You want a failed store write to fail the caller. The cache must not acknowledge data the store rejected.

## When not to use

- Write volume is high and most written keys are never read. You will fill memory with cold data. Use a TTL.
- The store is slow and the user path cannot wait.
- You need to survive a cache crash without having written the store. Write-through does write the store, so this is the wrong worry. Write-behind is the one that loses data.

## Tradeoffs

| You gain | You pay |
|---|---|
| A successful write is in the cache and the store | Slower writes |
| Reads hit fresh data | Memory holds keys nobody will read unless you TTL them |
| Cache failure on write is visible | A new empty cache is cold until the next write of each key |

## Failure modes

- Store write succeeds and the cache process dies before it returns: the caller may retry. The store write must be idempotent.
- Two writers to the same key need an order. Last writer wins only if that is acceptable.
- Partial update of a structure in cache while the store holds a different shape.

## Implementation notes

- The write path is: write store and cache together, or write cache only via a library that writes the store synchronously and returns the store's error.
- Put a TTL on entries so unread keys decay.
- Do not use write-through as a durability mechanism beyond what the store provides.

## Related patterns

- [Cache-aside](cache-aside.md)
- [Write-behind](write-behind.md)
- [Cache invalidation](cache-invalidation.md)
