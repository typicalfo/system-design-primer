---
title: "Availability and failover"
summary: "Stand up a second copy and a tested promotion path so one failure does not end the service."
tags: [availability, primer, failover]
when_to_use: "Use when the availability target is tighter than a single machine or a single zone can honestly meet."
related:
  - replication-leader-follower.md
  - load-balancing.md
  - circuit-breaker.md
last_reviewed: 2026-09-25
---

# Availability and failover

## Problem

One copy dies, and without a second copy that can take traffic you are down until you rebuild. Failover is the procedure that moves traffic. Replication is how the second copy got the data.

The System Design Primer covers the underlying idea in [Availability patterns](../README.md#availability-patterns). This card is the operational form. The Primer prose is unchanged.

## When to use

- The SLO requires surviving instance or zone loss.
- You can lose the writes that had not replicated, and that loss is inside the RPO, or you replicate synchronously.
- Someone can run the promotion, or automation can, and you have fenced the old primary.

## When not to use

- You have never promoted the standby. It is not a standby.
- Both copies share a deploy, a power domain, or a credential. One change removes both.
- You are buying failover hardware to avoid a backup restore drill. Failover does not save you from a bad delete.

## Tradeoffs

| Topology | Behavior | Cost |
|---|---|---|
| Active-passive | Standby takes the address when heartbeats stop. Hot standby fails faster than cold | Idle or underused capacity. Writes not replicated are lost |
| Active-active | Both take traffic | Conflicts if both write the same key. Clients must know both |
| Multi-zone single writer | Zones fail, writer moves inside the region | Does not cover a region loss |

## Failure modes

- Split brain after a partial network failure.
- DNS TTL keeps clients on the dead address.
- The standby's schema or config drifted and promotion fails.
- Heartbeats fail because the check is wrong, and you fail over a healthy system.

## Implementation notes

- Test promotion on a schedule, including the data layer, not only the app container.
- The Primer's downtime table is the language for the SLO. A second nine is a much smaller time budget.
- Prefer active-passive until you have a conflict story.
- Heartbeats must use a path that fails when the user path would fail.

## Related patterns

- [Leader-follower replication](replication-leader-follower.md)
- [Load balancing](load-balancing.md)
- [Multi-region guide](../enterprise/reliability/multi-region.md)
