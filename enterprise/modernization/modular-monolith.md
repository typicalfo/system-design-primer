---
title: "Modular monolith"
summary: "Keep one deployable, split it into modules with hard boundaries, and extract a service only when a team or a scale number requires it."
tags: [modernization, monolith, modularity]
when_to_use: "Use when a codebase is growing and a microservice split is the proposed cure, before you have a team or an operational reason to split."
related:
  - strangler-fig.md
  - anti-corruption-layer.md
  - ../organization/conways-law.md
  - ../organization/team-topologies.md
  - ../../patterns/strangler-fig.md
last_reviewed: 2026-09-25
---

# Modular monolith

A modular monolith is one deployable process (or one release train) whose internals are modules with explicit public interfaces. Modules do not reach into each other's tables. You get separate reasoning and a future extraction seam, without a distributed system.

The Primer notes that microservices add deployment and operational complexity. That disadvantage is the reason to wait. See [microservices](../../README.md#microservices) and [what's dated](../whats-dated.md).

## Decide

| Choose | Use when | Avoid when |
|---|---|---|
| Modular monolith | One or a few teams, unclear domain boundaries, no platform for many services, transactions still span the "future services" | A module has a genuinely different scale, compliance zone, or release cadence, and a team is ready to own it |
| Microservices | A team boundary, a scaling bottleneck, or an isolation requirement is already real | You want an architecture diagram to look modern. You will operate the network calls |
| Classic layered monolith | A small app with one team that can still find things | Any module can write any table and you are about to hire a second team |

## Defaults

- Each module exposes an interface (functions or an in-process port). Other modules use that interface. A lint or a build rule fails imports that reach into another module's internals.
- Each module owns its tables. Cross-module reads go through the interface or through an event, not through a join that becomes a secret API.
- One database is acceptable. Separate schemas are a stronger fence if you need it. Separate databases come when you extract the module.
- A shared kernel (identity, tenancy, time) stays small. If everything imports it, it is a couple point, not a platform.
- Tests can run one module without booting the world.
- When you extract, the interface becomes the network boundary. The [strangler](strangler-fig.md) is the move. The modular monolith was the rehearsal.
- On-call is still one rotation until you split. Do not invent per-module pagers with one engineer.

## Anti-patterns

- Folders named `services/` that share a database and deploy together, called microservices.
- A "module" boundary that is only a naming convention and is already widely violated.
- Extracting the first service by copying the tables and dual-writing, with no interface to compare.
- Waiting for the perfect module map before you stop new cross-table writes. Draw the worst offenders first.
