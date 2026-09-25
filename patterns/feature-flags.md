---
title: "Feature flags"
summary: "Branch behavior at runtime so you can ship code dark, open it gradually, or turn it off without a redeploy."
tags: [delivery, release]
when_to_use: "Use when deploy and release should be different events, or when a path needs a fast kill switch."
related:
  - canary.md
  - blue-green.md
  - strangler-fig.md
  - ../enterprise/delivery/feature-flags.md
last_reviewed: 2026-09-25
---

# Feature flags

## Problem

A deploy that immediately exposes every code path makes rollback depend on a rebuild. A flag makes exposure a decision you can reverse.

## When to use

- The off path is safe and tested.
- You need a cohort, a tenant allow-list, or an instant off switch.
- The flag has an owner and a removal date if it is a release flag.

## When not to use

- The 'flag' is an entitlement or a permission. Store that as authorization data.
- The flag service being down would take the user path with it, and you have not defined a default.
- You are accumulating long-lived branches nobody can reason about.

## Tradeoffs

| You gain | You pay |
|---|---|
| Decoupling release from deploy | A matrix of behaviors to test |
| Fast mitigation | Stale flags if you do not delete them |
| Targeted rollout | A new runtime dependency |

## Failure modes

- Evaluating a security decision only in the client.
- A percentage rollout that flips for the same user on every request.
- Flag service outage fails closed on the whole product by accident.
- A kill switch that does not wrap the worker that is doing the damage.

## Implementation notes

- Server-side evaluation for anything that matters.
- Audit who changed a flag.
- Default explicitly when evaluation fails.
- Delete release flags.
- Guide: [feature flags](../enterprise/delivery/feature-flags.md).

## Related patterns

- [Canary](canary.md)
- [Blue/green](blue-green.md)
- [Strangler fig](strangler-fig.md)
