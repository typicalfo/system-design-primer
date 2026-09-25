---
title: "Canary"
summary: "Send a small fraction of traffic to the new version and expand only if the user-visible metrics hold."
tags: [delivery, release]
when_to_use: "Use when a bad deploy should hurt a small slice first and you have a metric that will show it."
related:
  - blue-green.md
  - feature-flags.md
  - load-balancing.md
  - ../enterprise/delivery/progressive-delivery.md
---

# Canary

## Problem

Replacing every instance at once makes every user the tester. A canary makes a few percent the tester, with an automatic or human rollback.

## When to use

- Traffic is large enough that a small slice is statistically meaningful.
- The failure shows up in error rate, latency, or a business SLI quickly.
- You can route a percentage or a header to the new version.

## When not to use

- The bug is a rare data corruption that a 5% slice for ten minutes will not catch. You need a different check (a migration dry run, a backfill counter).
- Sessions break if two versions interleave and you cannot pin them.
- You do not have a baseline, so the canary is a vibe.

## Tradeoffs

| You gain | You pay |
|---|---|
| Limited blast radius | Two versions live at once |
| Evidence before full rollout | Analysis time and a router that can do weighted routes |
|  | False confidence if the slice is not representative |

## Failure modes

- The canary cohort is not representative (only internal users, or only one region).
- Automatic promotion continues while the canary is red.
- Metrics average the canary away because it is 1% of the chart. Compare the canary to the baseline explicitly.
- Workers are not canaried, and the bad job runs at 100%.

## Implementation notes

- Compare canary and baseline SLIs, not a global average.
- Set a minimum sample and a maximum bake.
- Pin multi-step sessions if versions differ.
- Include workers in the plan.
- Guide: [progressive delivery](../enterprise/delivery/progressive-delivery.md).

## Related patterns

- [Blue/green](blue-green.md)
- [Feature flags](feature-flags.md)
- [Load balancing](load-balancing.md)
