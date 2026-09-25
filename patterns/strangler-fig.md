---
title: "Strangler fig"
summary: "Route capabilities one at a time from a legacy system to a new one behind a stable facade, then delete the old path."
tags: [modernization, migration]
when_to_use: "Use when a system must be replaced in production and a single cutover is too risky."
related:
  - anti-corruption-layer.md
  - feature-flags.md
  - api-gateway.md
  - ../enterprise/modernization/strangler-fig.md
last_reviewed: 2026-09-25
---

# Strangler fig

## Problem

A rewrite that big-bangs on launch day has no rollback except 'turn the old system back on' after the data has already moved. A strangler replaces the system in slices. The name is Martin Fowler's: [Strangler Fig Application](https://martinfowler.com/bliki/StranglerFigApplication.html). This card does not copy that article.

## When to use

- You can intercept traffic or calls at a seam.
- You can compare old and new behavior for a slice.
- The legacy system can stay alive during the migration.

## When not to use

- The legacy system cannot be left running and also cannot be called. You have a cutover, not a strangler. Plan it as a cutover.
- You want to change behavior and replace the system in one slice. You will not know which change broke users.
- There is no commitment to delete the old path.

## Tradeoffs

| You gain | You pay |
|---|---|
| Incremental risk and an easy route-back early on | Two systems to operate until you finish |
| Value delivered before the rewrite is done | A facade to keep thin |
|  | Dual-write periods that must end |

## Failure modes

- The facade grows business logic.
- Both systems write the same data indefinitely.
- A slice is 'done' while 5% of traffic still hits legacy and nobody looks.
- Characterization of legacy behavior was skipped and the new path is 'cleaner' and wrong.

## Implementation notes

- Route by capability or tenant.
- Keep a parity check for reads.
- Define done as zero traffic and deleted code.
- Guide: [strangler fig](../enterprise/modernization/strangler-fig.md).

## Related patterns

- [Anti-corruption layer](anti-corruption-layer.md)
- [Feature flags](feature-flags.md)
- [Modular monolith guide](../enterprise/modernization/modular-monolith.md)

## Further reading

- [Strangler Fig Application](https://martinfowler.com/bliki/StranglerFigApplication.html), Martin Fowler
