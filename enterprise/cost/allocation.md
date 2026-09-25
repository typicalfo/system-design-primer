---
title: "Cost allocation"
summary: "Attribute shared spend to teams and tenants with tags and a written split, so showback is explainable."
tags: [cost, allocation, tenancy, finops]
when_to_use: "Use when more than one team or tenant shares a platform and someone asks who spent the money."
related:
  - finops.md
  - unit-economics.md
  - ../tenancy/isolation-models.md
  - ../organization/ownership.md
  - ../organization/platform-teams.md
last_reviewed: 2026-09-25
---

# Cost allocation

Allocation answers "whose bill is this." Showback reports the number to the team. Chargeback invoices them. Start with showback. Chargeback without trust in the number creates arguments, not efficiency.

## Defaults

- Tag resources with `service` and `team` at create time. IaC sets the tags. A policy denies untagged creates in production, or a bot flags them the same day.
- Shared platforms (the cluster, the log pipeline, the CI runners) split by a usage metric: CPU-hours, GB-days, build minutes, or request count. Headcount is a last resort and will be wrong for a small team that owns a huge index.
- Tenant-level allocation is required when tenants differ wildly or when a contract is cost-plus. Use the metering you already have (storage per tenant, request class per tenant) rather than a new exact system. Approximate and documented beats exact and unfinished.
- A silo tenant's dedicated resources tag with the tenant id. The pool's shared resources use the split rule, not a fake per-tenant precision you cannot defend.
- One owner reconciles "unallocated" each month. Unallocated should trend down. It will not be zero.
- Credits and commitments are allocated by the same rule as the underlying usage, or they distort every team's number the month they land.
- The platform team publishes the rule. Changing the rule is an [ADR](../organization/decisions.md), because it changes other teams' reported spend.

## Decide

| Cost | Attribute by |
|---|---|
| A service's own database | The owning team, 100% |
| Multi-tenant pool database | Usage share (storage or request), with the platform residual explicit |
| Observability pipeline | Ingested GB per service |
| Idle cluster headroom kept for failover | The platform or the SLO owner, named, not smeared invisibly |
| A tenant silo | That tenant, for margin decisions |

## Anti-patterns

- Re-billing shared Kubernetes costs by namespace request (the ask) when actual usage is the real driver and requests are padded.
- A tenant id tag on every object with millions of values, if the billing export cannot handle the cardinality. Aggregate metering in your own table instead.
- Chargeback to the cent with a model nobody can recompute.
- Punishing a team for the platform's idle replicas by hiding them inside the team's number.
