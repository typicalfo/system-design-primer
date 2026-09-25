---
title: "Blue/green"
summary: "Run two complete environments and switch traffic from the live color to the idle one."
tags: [delivery, release]
when_to_use: "Use when you can afford a second full stack and you want to cut back to the previous version quickly."
related:
  - canary.md
  - feature-flags.md
  - ../enterprise/delivery/progressive-delivery.md
---

# Blue/green

## Problem

In-place upgrades mix versions and make rollback a redeploy under pressure. Blue/green keeps the previous stack intact and switches the router.

## When to use

- The app is stateless or sessions survive the switch.
- You can pay for two stacks during the bake.
- Schema changes are backward compatible so the old color still works if you switch back.

## When not to use

- The database migration is destructive and the old color cannot read it. Switching the router back will not heal that.
- Two full production-sized stacks are too expensive and a canary of a few instances would teach you as much.
- Long-lived connections (websockets, consumers) are not drained.

## Tradeoffs

| You gain | You pay |
|---|---|
| Fast rollback to a stack that is still warm | Double capacity for the overlap |
| A clear 'which version is live' | Migrations must be compatible with both |
|  | Shared databases mean the switch is not a full isolation boundary |

## Failure modes

- The idle color was not receiving migrations or config and fails on switch.
- Both colors write incompatibly.
- Health checks pass on the new color before dependencies are ready, and you switch anyway.
- Caches and jobs were not part of the color and keep old behavior.

## Implementation notes

- Exercise the idle color (smoke tests) before the switch.
- Drain connections.
- Keep the old color until the bake window ends.
- Pair with expand/contract migrations.
- Guide: [progressive delivery](../enterprise/delivery/progressive-delivery.md).

## Related patterns

- [Canary](canary.md)
- [Feature flags](feature-flags.md)
