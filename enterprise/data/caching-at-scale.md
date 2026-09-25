---
title: "Caching at scale"
summary: "Place cache tiers, stop stampedes and hot keys, and size a shared cache without pretending it is the database."
tags: [data, caching, stampede, capacity]
when_to_use: "Use when a cache is already the right basic pattern and the problem is fan-in, hot keys, invalidation, cold starts, or tenant fairness."
related:
  - ../tenancy/data-and-keys.md
  - ../tenancy/noisy-neighbor.md
  - ../reliability/load-shedding.md
  - ../reliability/disaster-recovery.md
  - transactional-outbox.md
  - cdc.md
  - ../../patterns/cache-aside.md
  - ../../patterns/cache-invalidation.md
  - ../../patterns/refresh-ahead.md
  - ../../patterns/write-through.md
  - ../../patterns/write-behind.md
  - ../../patterns/cdn.md
  - ../../README.md#cache
last_reviewed: 2026-09-25
---

# Caching at scale

The fill and write patterns already have cards: [cache-aside](../../patterns/cache-aside.md), [write-through](../../patterns/write-through.md), [write-behind](../../patterns/write-behind.md), [refresh-ahead](../../patterns/refresh-ahead.md), and [invalidation](../../patterns/cache-invalidation.md). The Primer's [cache](../../README.md#cache) section is the interview sketch, including the [CDN](../../patterns/cdn.md). This page is what changes when many instances, tenants, and nodes share those patterns. It does not restate how a miss loads the database.

The database remains the source of truth unless you deliberately chose write-through or write-behind and accepted what those cards say they lose.

## Decide

| Problem | Use when | Avoid when |
|---|---|---|
| Another tier (client, CDN, process, distributed) | That tier sees repeated reads of data it is allowed to hold | You add a tier to hide a missing index. The miss path is still the bug |
| Single-flight or a lock | Many callers miss the same key at once | The recompute is cheap and rare. The lock is then the outage |
| Probabilistic early refresh or stale-while-revalidate | A popular key expires into a cliff, and a slightly early value is allowed | The value is an authorization decision that must die on time |
| Split or locally cache a hot key | One key is hotter than one cache node | The key is hot because it is a single counter you should have sharded in the product |
| Per-tenant cap | Tenants share the cache | Each tenant already has its own cache |

## Tiers

| Tier | What it is good for | What you accept |
|---|---|---|
| Client | Private repeats on one device. `Cache-Control` is the contract | You cannot reach in and delete it on the user's phone until TTL |
| CDN | The same public bytes for many users | A shared cache key that includes a secret or omits a Vary header leaks. See [CDN](../../patterns/cdn.md) |
| Edge or reverse proxy | Regional repeats in front of the app | Another TTL to own, and a purge that is eventually consistent |
| In-process | The hottest tiny values, microsecond hits, no network | Lost on deploy. Invisible to other instances. A stampede becomes one miss per process, which is still a lot of processes |
| Distributed | The working set shared by the fleet | A network hop, a memory ceiling, and an invalidation path |

Put the tenant in the key at every shared tier. [Data and keys](../tenancy/data-and-keys.md) is the rule. A process-local cache is still shared by every request in that process, so it needs the tenant too.

## Stampedes

A stampede is many misses rebuilding one key. Four brakes, from the one you want first:

- Single-flight. Callers for the same key in one process share one recompute. Across processes, a lock in the cache (`SET` if absent, with a TTL) elects one filler. The TTL must outlive a slow recompute, and a dead holder must expire or everyone waits. Waiters that time out either serve stale or go to the database. Pick one and cap how many go to the database.
- Probabilistic early expiration. As the entry nears TTL, a rising fraction of readers refresh it, so expiry is not one instant. Combine it with jitter. [Refresh-ahead](../../patterns/refresh-ahead.md) is the scheduled form of the same idea for keys you already know are hot.
- A lock without single-flight still works when the others can serve a stale copy or get a "try again" quickly. A lock that blocks the user for the whole recompute piles up threads. That pile-up is the outage.
- Stale-while-revalidate. [RFC 5861](https://www.rfc-editor.org/rfc/rfc5861) defines `stale-while-revalidate` and `stale-if-error` as `Cache-Control` extensions. Serve the stale response and refresh off to the side. Use it when the product allows that staleness. The same RFC's stale-if-error path is how a dead origin keeps serving a known-good copy.

TTL jitter belongs on every tier: `ttl = base + random(0, spread)`, so keys written in one deploy do not expire in one second. Example: base 300 seconds, spread 60 seconds, so a key lives 300 to 360 seconds.

## Hot keys

Detect them on purpose. Per-key request rate, cache-node CPU pinned on one slot, or a latency outlier on one id. Cluster averages hide this. The same watch is in [noisy neighbors](../tenancy/noisy-neighbor.md).

Two structural fixes:

- A short in-process cache of the few hottest keys. Each instance misses once per local TTL instead of once per request. The distributed cache then sees instance-count traffic, not user traffic.
- Key replication. Write the value to `N` slots and read one at random. Read rate per slot is `1/N`. Every write updates all `N`.

Example: one key is read 40,000 times/s. A node stays healthy at 10,000 reads/s on a single key.

```text
N = 40,000 / 10,000 = 4
```

Four copies put 10,000 reads/s on each. Writes become 4 writes. If the write rate is 50/s, that is `50 * 4 = 200` writes/s, which is the cost of the split. If writes are as hot as reads, splitting reads makes the write path worse. Change the product (batch, sample, or shard the counter) instead.

## Invalidation

The invalidation card still holds: name the staleness, and keep a TTL as a backstop. At fleet scale add three mechanics.

- Event-driven deletes. The [outbox](transactional-outbox.md) or [CDC](cdc.md) emits the change. Consumers delete or replace the key. A lost event is why the TTL exists.
- Versioned keys. Readers load a small generation `g`, then the bulky value at `object:{id}:v{g}`. A write bumps `g`. Old values age out by TTL. A filler that races an older read stores an old generation, and readers who already saw the new `g` ignore it.
- Jitter, as above, so invalidation-by-expiry is not a synchronized miss.

Flushing the whole cache is a break-glass with a stampede plan, not a deploy step.

## Cold start

A new node, a failover, or a flush starts at hit rate zero. The database then sees the full read rate.

- Single-flight so each key is loaded once, not once per waiter.
- Preload only the keys the last hour actually read, from an access count you stored. Loading the whole database fills memory with cold rows and still misses the hot ones if you guess wrong.
- Ramp traffic, or [shed](../reliability/load-shedding.md), until the hit rate recovers. A failover that sends 100% of users at an empty cache fails the failover. See [disaster recovery](../reliability/disaster-recovery.md).

## Fairness and consistency

Namespace every shared key with the tenant. Cap how much memory and how many gets one tenant may use, or one tenant's export evicts the interactive working set. A silo tenant can have a silo cache. That is the cache form of [noisy neighbors](../tenancy/noisy-neighbor.md).

Say the consistency you mean, per tier:

- Client and CDN: stale up to the `Cache-Control` lifetime, longer if a proxy ignores you.
- In-process: stale up to its TTL, and different on each instance.
- Distributed cache-aside: stale until delete or TTL. A failed delete means the TTL is the real bound.
- Write-through: the write path waits for the store. A crash between store and cache is a retry problem, covered on that card.
- Write-behind: the cache is ahead of the store. Loss of the dirty set is data loss.

Do not promise read-your-writes through a CDN. Do not promise it across instances through a process-local cache.

## Sizing

Planning assumptions: 25,000,000 entries, 2,048-byte values, 64-byte keys, a 1.5× factor for allocator overhead and fragmentation, one replica, 50 GiB of cache data budgeted on each node.

```text
Bytes per entry = 2,048 + 64 = 2,112
Raw             = 25,000,000 * 2,112 = 52,800,000,000 bytes
With 1.5×       = 52,800,000,000 * 1.5 = 79,200,000,000 bytes = 73.761 GiB
Primary+replica = 2 * 79,200,000,000 = 158,400,000,000 bytes = 147.521 GiB
Nodes           = 147.521 / 50 = 2.950, so 3 nodes
```

GiB figures are the byte counts divided by 1024^3, rounded to three decimals.

Three nodes at 50 GiB budget `3 * 50 = 150` GiB, which covers 147.521 GiB. Check a node loss. Two nodes budget `100` GiB. One full copy is 73.761 GiB, so the surviving pair can hold a single copy. They cannot hold both replicas until you replace the node or you lower replication. Write that down next to the replica setting. The 1.5× factor is a planning allowance, not a measurement of a vendor. Replace it with the process's resident set from a load of this working set before you buy the fleet.

Hit rate is the other half. At 8,000 requests/s and a 90% hit rate the origin sees:

```text
8,000 * (1 - 0.90) = 800 requests/s
```

A stampede on one key does not care about the average. The hot-key sum above is the peak the origin must survive for that id.

## Checklist

- [ ] Each tier has a TTL, a key that includes the tenant, and a named staleness.
- [ ] The hottest keys have a single-flight or a stale-while-revalidate path.
- [ ] TTLs are jittered.
- [ ] Invalidation is an event plus a TTL, not a flush.
- [ ] Failover has a warm-up or a ramp. The empty-cache read rate is in the database budget.
- [ ] One tenant cannot fill the shared memory.

## Anti-patterns

- A cache tier with no TTL and no delete path.
- A distributed lock with no expiry around the recompute.
- Replicating a hot key and forgetting that writes must hit every copy.
- Version keys that readers do not check, so the old generation is still served.
- Warming every row after failover.
- Sharing one un-namespaced cache across tenants because "the ids are UUIDs."

## Related

- [Cache-aside](../../patterns/cache-aside.md), [invalidation](../../patterns/cache-invalidation.md), [refresh-ahead](../../patterns/refresh-ahead.md), [write-through](../../patterns/write-through.md), [write-behind](../../patterns/write-behind.md), [CDN](../../patterns/cdn.md)
- [Primer cache section](../../README.md#cache)
- [Data and keys](../tenancy/data-and-keys.md), [noisy neighbors](../tenancy/noisy-neighbor.md), [load shedding](../reliability/load-shedding.md), [disaster recovery](../reliability/disaster-recovery.md)
- [Outbox](transactional-outbox.md), [CDC](cdc.md)

## Sources

- [RFC 5861, HTTP Cache-Control extensions for stale content](https://www.rfc-editor.org/rfc/rfc5861)
- [Cache stampede](https://en.wikipedia.org/wiki/Cache_stampede) (link only)
- [Go singleflight](https://pkg.go.dev/golang.org/x/sync/singleflight)
