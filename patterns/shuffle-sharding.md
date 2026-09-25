---
title: "Shuffle sharding"
summary: "Assign each tenant a small random subset of a shared fleet so two tenants rarely share the exact same fate."
tags: [reliability, isolation, sharding]
when_to_use: "Use when you cannot give every tenant a cell, but one noisy tenant must not be able to sit on every node the others use."
related:
  - cell-based-architecture.md
  - sharding.md
  - bulkhead.md
  - ../enterprise/reliability/cell-based-architecture.md
last_reviewed: 2026-09-25
---

# Shuffle sharding

## Problem

A shared pool puts every tenant on every node. One abusive or poisoned client can touch the whole pool. Dedicated stacks (cells) avoid that and cost a stack per slice. Shuffle sharding sits between them: each tenant is pinned to k nodes chosen from n, and a different tenant usually gets a different subset.

## When to use

- The work is already spread across n equivalent nodes (workers, partitions, or cache shards).
- You can stick a tenant to a subset and route only there.
- Full overlap of two tenants should be rare. Partial overlap is acceptable.
- You can compute the combinations and live with the number. The formula is below.

## When not to use

- You need a hard guarantee that tenant A cannot affect tenant B. Overlap is still possible. Use a [cell](cell-based-architecture.md) or a silo.
- k is almost n. Then almost every tenant shares almost every node, and the combinatorics were a comfort.
- The client retries onto a node outside its subset. The assignment is then a suggestion.
- The assignment is "random" once at deploy and then a hot tenant is placed by hand onto the busiest nodes.

## Tradeoffs

| You gain | You pay |
|---|---|
| Many virtual shards without many physical clusters | Some tenants still share a node |
| A noisy tenant's damage is capped at its k nodes | The other tenants on those nodes still feel it |
| No extra full stack per tenant | The router must know the assignment and must enforce it |
| A fleet that still looks like one pool to operators | A bad assignment function clumps tenants onto one subset |

## Failure modes

- The router is a single shared failure, so the isolation never gets a chance to matter.
- Retry or a load balancer sends the tenant to any healthy node. Shuffle sharding is bypassed.
- k and n are chosen so C(n, k) looks large while the probability of sharing one node stays high. Read the overlap count, not only the combination count.
- A tenant larger than k nodes is forced into the pattern and overloads its subset. That tenant needs a cell or a bigger k, on purpose.

## Implementation notes

The number of distinct subsets of size k from n nodes is

C(n, k) = n! / (k! × (n − k)!)

for integers n and k with 0 ≤ k ≤ n. Outside that range the count is 0. Publish the exact integer. Do not round it.

**Example.** n = 8 nodes, k = 2.

C(8, 2) = 8! / (2! × 6!) = (8 × 7) / 2 = 28.

There are 28 shards. A second tenant drawn uniformly from those 28 lands on one fixed tenant's pair with probability 1/28.

One node down sits in C(7, 1) = 7 of those shards. 7 / 28 = 1/4. Those tenants still have their other node. They are degraded, not fully dark, if one member of the pair can serve.

Two specific nodes down, same n and k:

- Fully dark (the shard was exactly those two nodes): C(2, 2) = 1.
- Degraded (exactly one of the two failed nodes): C(2, 1) × C(6, 1) = 2 × 6 = 12.
- Untouched: C(6, 2) = (6 × 5) / 2 = 15.
- 1 + 12 + 15 = 28.

One shard in 28 is fully down. Twelve are degraded. Fifteen are untouched. The same 1, 12, and 15 count how a second assignment overlaps a fixed pair (identical, share one node, share none). Do not add those stories together. They are two readings of one partition of the 28.

Changing n or k changes the count. Recompute. The longer walk, including why a fixed pairing of the same 8 nodes is harsher, is in [cell-based architecture](../enterprise/reliability/cell-based-architecture.md).

Assign the subset from a stable hash of the tenant id, or store the assignment, so a restart does not move the tenant. Ordinary key sharding, which splits data rather than blast radius, is [sharding](sharding.md).

## Related patterns

- [Cell-based architecture](cell-based-architecture.md)
- [Sharding](sharding.md)
- [Bulkhead](bulkhead.md)
