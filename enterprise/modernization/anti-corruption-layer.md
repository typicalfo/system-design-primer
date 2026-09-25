---
title: "Anti-corruption layer"
summary: "Translate between a legacy model and a new model in one place, so the new model does not grow the legacy system's concepts."
tags: [modernization, anti-corruption-layer, integration]
when_to_use: "Use when a new component must talk to a legacy or external system whose model you do not want to adopt as your own."
related:
  - strangler-fig.md
  - modular-monolith.md
  - ../apis/styles.md
  - ../../patterns/anti-corruption-layer.md
  - ../../patterns/strangler-fig.md
last_reviewed: 2026-09-25
---

# Anti-corruption layer

An anti-corruption layer (ACL) is a translation boundary. The new system speaks its own types. The ACL maps them to the legacy API, database, or event, and back. Legacy nouns do not leak into new tables and new public APIs.

The pattern is part of Eric Evans's domain-driven design vocabulary and is also catalogued by microservices.io (all rights reserved, link only): <https://microservices.io/patterns/index.html>. Pattern card: [anti-corruption layer](../../patterns/anti-corruption-layer.md).

## Defaults

- One ACL per legacy system, owned by the team that is migrating or integrating. It is not a shared "utils" package everyone edits.
- Map ids explicitly. If the legacy id must be stored, store it as an external reference, not as the new aggregate's primary key, unless you have decided they are the same forever.
- The ACL owns retries, timeouts, and the legacy system's quirks (a `null` date that means "open," a status code reused for two meanings). The new domain model does not grow a field for that quirk.
- Translate at the edge, once. Do not map halfway in the gateway and halfway in the service.
- Contract tests freeze the legacy behavior the ACL depends on, so a legacy patch fails CI instead of corrupting new data.
- The ACL is temporary when it fronts a system you are replacing. Deleting it is a milestone of the [strangler](strangler-fig.md). It is permanent when the other side is a partner you do not control.
- Keep the ACL thin. Business rules that are truly yours live in the new model. If the ACL starts deciding policy, it has become a second product.

## Decide

| Leak you are tempted to allow | What to do instead |
|---|---|
| Legacy status enum in the new API | Map to the new enum. Unknown values become an explicit `unmapped` case with an alert |
| Reading the legacy database from the new service | Read through the ACL or a replica owned as an interface. A private table is not a contract |
| "Just this once" legacy field on the new entity | A separate mapping table inside the ACL's store |

## Anti-patterns

- An ACL that exposes the legacy payload as a JSON blob "for flexibility."
- Two ACLs maintained by different teams for the same legacy system, drifting apart.
- Business logic duplicated in the ACL and the new service, with no test that they match.
- Treating the ACL as a place to hide a dual-write. The transactional problem remains. See [outbox](../data/transactional-outbox.md).
