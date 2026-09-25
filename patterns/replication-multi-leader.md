---
title: "Multi-leader replication"
summary: "More than one node accepts writes, and the nodes converge, with conflicts when they write the same key."
tags: [data, primer, replication]
when_to_use: "Use when a single writer is an availability problem you have measured, and you have a conflict rule."
related:
  - replication-leader-follower.md
  - consistency-patterns.md
  - availability-failover.md
  - idempotency-keys.md
last_reviewed: 2026-09-25
---

# Multi-leader replication

## Problem

A single leader is a single writer. If that node or its region is down, writes stop. A second writer keeps writes available and creates conflicts.

The System Design Primer covers the underlying idea in [Master-master replication](../README.md#master-master-replication). This card is the operational form. The Primer prose is unchanged.

## When to use

- Writers are partitioned by key in practice (each tenant has a home) and conflicts are rare.
- The data structure merges safely (a counter with a defined merge, a set).
- Regional latency forbids a remote leader on the user path, and stale or merged writes are acceptable.

## When not to use

- The data is a balance, an inventory count, or a unique constraint with no merge.
- You can put a leader in one region and the product still meets its latency SLO.
- You do not have an operator who can explain the conflict rule at 2 a.m.

## Tradeoffs

| You gain | You pay |
|---|---|
| Writes survive the loss of one writer | Conflicts, or synchronous latency to avoid them |
| Local write latency in each region | Operational load: split brain, fencing, and 'which write won' |
|  | Most systems are then loosely consistent, which the Primer already warns |

## Failure modes

- Split brain: both sides accept writes during a partition, then both claim to be authoritative.
- Last-write-wins drops a counter update or a permission revoke.
- Clock skew makes 'last' meaningless.
- A unique index exists on only one side.

## Implementation notes

- Prefer one writer per key (home region) so the topology looks multi-leader but conflicts do not happen.
- If conflicts can happen, pick a rule that is not last-write-wins for business data: reject, merge, or reserve.
- Fence a demoted writer.
- Test a partition. Do not only test a clean failover.

## Related patterns

- [Leader-follower replication](replication-leader-follower.md)
- [Consistency patterns](consistency-patterns.md)
- [Idempotency keys](idempotency-keys.md)
