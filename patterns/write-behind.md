---
title: "Write-behind"
summary: "The application writes the cache and the store is updated asynchronously after the caller has been told success."
tags: [caching, primer]
when_to_use: "Use when write latency must be tiny and you can lose or delay the latest writes if the cache dies."
related:
  - cache-aside.md
  - write-through.md
  - cache-invalidation.md
  - ../enterprise/data/caching-at-scale.md
last_reviewed: 2026-09-25
---

# Write-behind

## Problem

The store cannot absorb the write rate or the write latency on the user path, but you can buffer a short window of updates in memory.

The System Design Primer covers the underlying idea in [Write-behind (write-back)](../README.md#write-behind-write-back). This card is the operational form. The Primer prose is unchanged.

## When to use

- Acknowledged loss or delay of the buffered window is an explicit, accepted RPO.
- The write stream is bursty and the store can catch up.
- You have a bounded buffer and a plan when it fills.

## When not to use

- The write is a payment, an audit record, or anything you promised would survive a crash once you returned success.
- You cannot make the later store write idempotent.
- The cache is shared and untrusted. Buffered writes are a durability mechanism wearing a cache's clothes.

## Tradeoffs

| You gain | You pay |
|---|---|
| Fast writes | A crash before flush loses those writes |
| The store sees a smoothed write rate | Read-your-writes is only true against the cache, not against a peer that reads the store |
| Short user latency | Operational complexity: flush lag, replay, and a full buffer |

## Failure modes

- Process crash or eviction drops the dirty entries. That is data loss, not a slowdown.
- Flush lag grows until the store is the bottleneck again, with extra delay.
- Reordering flushes breaks last-write-wins if you are not careful.
- A second reader that bypasses the cache sees stale or missing data.

## Implementation notes

- Bound the dirty set. When it is full, refuse writes or slow the caller down. Do not grow without a cap.
- Flush in key order for a given id.
- Measure flush lag. It is your real RPO.
- If you cannot accept the loss window, use a durable log or an outbox, not a cache.

## Related patterns

- [Write-through](write-through.md)
- [Cache-aside](cache-aside.md)
- [Transactional outbox](transactional-outbox.md)
