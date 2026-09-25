---
title: "Anti-corruption layer"
summary: "Translate between a new model and a legacy or external model so foreign concepts stay at the edge."
tags: [modernization, integration]
when_to_use: "Use when a new component must integrate with a system whose model should not become your model."
related:
  - strangler-fig.md
  - api-gateway.md
  - ../enterprise/modernization/anti-corruption-layer.md
last_reviewed: 2026-09-25
---

# Anti-corruption layer

## Problem

If the new code imports the legacy types, the legacy system has moved into the new one. Every quirk becomes permanent.

## When to use

- The other side is legacy you are replacing, or a partner you do not control.
- You can name the mapping and the owner.
- The new model has its own ids and language.

## When not to use

- The two models are genuinely the same and the mapping would be a pass-through. Call the API.
- You are hiding a dual-write inside the translator. The consistency problem remains.
- Several teams each build a mapper for the same system.

## Tradeoffs

| You gain | You pay |
|---|---|
| A new model that can evolve | A component to test and to delete later if the legacy system dies |
| One place for legacy quirks | A risk that business logic hides in the mapper |

## Failure modes

- Legacy ids become the new primary keys and can never change.
- Unknown enum values crash the new system.
- Two mappers drift.
- The layer exposes the raw legacy payload.

## Implementation notes

- One ACL per external system.
- Map unknown values to an explicit case and alert.
- Contract-test the legacy behaviors you depend on.
- Guide: [anti-corruption layer](../enterprise/modernization/anti-corruption-layer.md).
- The microservices.io write-up is all rights reserved. Link it. Do not copy it.

## Related patterns

- [Strangler fig](strangler-fig.md)
- [API gateway](api-gateway.md)
