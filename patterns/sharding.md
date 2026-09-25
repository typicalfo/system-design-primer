---
title: "Sharding"
summary: "Split one dataset so each node holds a subset of the keys, usually by hash or by range."
tags: [data, primer, sharding]
when_to_use: "Use when one dataset's size or write rate no longer fits one primary, and the access pattern is by a shard key."
related:
  - federation.md
  - replication-leader-follower.md
  - denormalization.md
---

# Sharding

## Problem

A single primary is out of disk, out of write throughput, or its index no longer fits memory. Vertical growth has stopped being the cheap option.

The System Design Primer covers the underlying idea in [Sharding](../README.md#sharding). This card is the operational form. The Primer prose is unchanged.

## When to use

- Queries include the shard key (tenant, user, or another high-cardinality id).
- Cross-shard transactions are rare and can be redesigned.
- You accept operational work: rebalancing, per-shard failure, and uneven keys.

## When not to use

- The workload is still fine on one primary with a replica. Sharding early is a tax.
- Every request joins across the whole dataset.
- You cannot choose a stable key. A key you must change later is a migration project.

## Tradeoffs

| You gain | You pay |
|---|---|
| Smaller indexes and parallel writes | The application must route to the right shard |
| One shard down does not take the others down | The rows on a down shard are unavailable unless that shard is also replicated |
| A path to more than one machine | Hot keys and rebalancing |
|  | Cross-shard queries and unique constraints become application problems |

## Failure modes

- A hot key (one tenant, one celebrity user) pins one shard. The average looks fine.
- A naive geographic or alphabetical key clumps. The Primer's warning on this still holds.
- Resharding moves more data than the cluster can copy before the disks fill.
- A unique email across shards needs a side index or the uniqueness is a lie.
- Transactions that spanned tables now span the network and will time out.

## Implementation notes

- Hash the key for even spread. Use consistent hashing or a directory so adding a shard does not move every row.
- Replicate each shard. Sharding is not backup and is not high availability by itself.
- Put the shard key in every index you query.
- Load-test the hottest key you expect, not only the mean.
- Plan the split before the disk is 80% full. Splits need free space.

## Related patterns

- [Federation](federation.md)
- [Leader-follower replication](replication-leader-follower.md)
- [Denormalization](denormalization.md)
