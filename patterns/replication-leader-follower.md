---
title: "Leader-follower replication"
summary: "One leader accepts writes and replicates them to followers that serve reads."
tags: [data, primer, replication]
when_to_use: "Use when read traffic exceeds one node's capacity and you can tolerate replication lag on the read path."
related:
  - replication-multi-leader.md
  - availability-failover.md
  - consistency-patterns.md
  - sharding.md
last_reviewed: 2026-09-25
---

# Leader-follower replication

## Problem

One node can take the writes, but reads or availability require copies. The Primer calls this master-slave. Prefer leader-follower or primary-replica in new writing.

The System Design Primer covers the underlying idea in [Master-slave replication](../README.md#master-slave-replication). This card is the operational form. The Primer prose is unchanged.

## When to use

- There is a natural single writer per key.
- Read scaling or a failover target is the goal.
- You can send reads that must be current to the leader.

## When not to use

- You need every region to accept writes on the same key. That is multi-leader.
- The write rate itself exceeds one node. Replication does not increase write capacity on the leader.
- Followers are being asked to serve reads that cannot be stale (a permission change, a payment balance).

## Tradeoffs

| You gain | You pay |
|---|---|
| Read scale and a promotion target | Lag. A read may miss the latest write |
| Simpler conflicts than multi-leader | Failover can lose writes that never reached a follower |
|  | Followers spend capacity replaying writes, so adding followers is not free |
|  | Some engines apply the log serially, and the follower falls behind under parallel writes on the leader |

## Failure modes

- Promoting a follower that is behind drops the missing writes or requires them to be reconciled.
- Read-after-write bugs when the app reads a follower.
- Replication stops and the follower is silently ancient. Queries still succeed.
- A long-running analytical query on a follower is fine until it is not, and lag spikes.

## Implementation notes

- Monitor replication lag in seconds and in bytes. Alert before the RPO is breached.
- For read-your-writes, stick the reader to the leader for a short time after a write, or read the leader for that key.
- Automate promotion only with fencing so the old leader cannot still accept writes.
- Do not point schema migrations at a random follower.

## Related patterns

- [Multi-leader replication](replication-multi-leader.md)
- [Availability and failover](availability-failover.md)
- [Consistency patterns](consistency-patterns.md)
