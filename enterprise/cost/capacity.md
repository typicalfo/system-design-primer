---
title: "Capacity planning"
summary: "Turn the traffic estimate into a resource plan with headroom, a lead time, and a date to revisit."
tags: [cost, capacity, estimates]
when_to_use: "Use when a launch, a tenant move, or a 10× concern needs more than a guess that the cloud will autoscale."
related:
  - finops.md
  - unit-economics.md
  - ../reliability/load-shedding.md
  - ../../templates/capacity-estimate.md
  - ../../pack/skills/system-architect/reference/estimates.md
  - ../../pack/skills/cost-estimator/SKILL.md
last_reviewed: 2026-09-25
---

# Capacity planning

Autoscaling reacts. Capacity planning decides whether the ceiling, the quota, and the database can react in time. The arithmetic belongs in [templates/capacity-estimate.md](../../templates/capacity-estimate.md). Formulas for rate, bandwidth, and storage are in the [estimates reference](../../pack/skills/system-architect/reference/estimates.md).

## Defaults

- Start from a stated peak, not from the annual average. Write the peak multiplier and why you believe it (last launch was 5×, or you are assuming 5×).
- Identify the first bottleneck with a number: primary write QPS, connection count, partition throughput, pool size, or a third-party quota.
- Headroom is explicit. A common starting point is to run steady peak at or below 50–70% of the resource that cannot scale in minutes (databases, quotas, regional caps). Stateless replicas can sit higher if scale-out is fast and you have load shedding for the gap.
- Lead time: quota increases, hardware, and shard splits are not instantaneous. File them before the launch week.
- The plan names what you will shed or degrade if the forecast is wrong. See [load shedding](../reliability/load-shedding.md).
- Revisit when traffic doubles or a large tenant arrives. A plan from last year is a souvenir.
- Load test the bottleneck at the forecasted peak before you promise the date. A test that only hits a mock proves the mock.

## Checklist

- [ ] Requests per second, payload size, storage growth, and the hot key are written down.
- [ ] The database, cache, and connection pools are sized for the scaled app tier, not for today's tier.
- [ ] A quota or account limit is listed with the current value and the requested value.
- [ ] Cost of the plan is in the same worksheet, so a 3× replica choice is visible.
- [ ] Someone owns raising the ceiling if the graph crosses 70% of the bottleneck.

## Anti-patterns

- "Kubernetes will scale" when the database is the limit and it will not.
- Planning for the mean and discovering the batch job's nightly peak.
- A single shard key you cannot split, found at the launch.
- Capacity owned by a spreadsheet no service team has opened.
