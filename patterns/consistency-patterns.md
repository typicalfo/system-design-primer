---
title: "Consistency patterns"
summary: "Choose weak, eventual, or strong consistency per path, and write the partition behavior separately from the healthy-path latency."
tags: [data, primer, consistency]
when_to_use: "Use when more than one copy of data exists and a reader might not see the latest write."
related:
  - replication-leader-follower.md
  - replication-multi-leader.md
  - availability-failover.md
  - cqrs.md
last_reviewed: 2026-09-25
---

# Consistency patterns

## Problem

Copies disagree until someone pays latency or accepts staleness. The design has to say which paths pay.

The System Design Primer covers the underlying idea in [Consistency patterns](../README.md#consistency-patterns). This card is the operational form. The Primer prose is unchanged.

## When to use

- You are choosing a store, a replica, or a projection.
- Different paths can have different answers. A write acknowledgement can be strong while search is eventual.

## When not to use

- You want one consistency label for the whole company. It will be wrong for half the paths.
- You are treating 'pick two of three' from CAP as a permanent property. During a partition you choose availability or consistency. While healthy you also choose latency or consistency (PACELC). See [what's dated](../enterprise/whats-dated.md).

## Tradeoffs

| Pattern | A later read | Price |
|---|---|---|
| Weak | May never see the write. Dropped updates are acceptable (realtime media, some games) | Lowest coordination |
| Eventual | Will see the write after a lag | Asynchronous replication. Conflicts if two writers exist |
| Strong | Sees the write after success, or the write did not succeed | Synchronous replication, higher latency, and refused operations during a partition |

## Failure modes

- A client reads a follower and misses its own write.
- A partition heals by dropping one side's writes with no alert.
- A projection is treated as strong and the product makes a decision on stale data (selling inventory you no longer have).
- Quorum settings copied from a blog without a failure test.

## Implementation notes

- Name the pattern per path in the design's tradeoffs.
- Send 'must be current' reads to the leader or a quorum read.
- Measure lag.
- The Primer's examples still help: DNS and mail are eventual; a transactional ledger wants strong writes.
- Do not describe a system as CP or AP and stop. State partition behavior and healthy-path latency.

## Related patterns

- [Leader-follower replication](replication-leader-follower.md)
- [Multi-leader replication](replication-multi-leader.md)
- [CQRS](cqrs.md)
