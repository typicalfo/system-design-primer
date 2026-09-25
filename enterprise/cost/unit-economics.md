---
title: "Unit economics"
summary: "Express cost per business unit so a design change can be compared to the revenue or the budget it serves."
tags: [cost, unit-economics, finops]
when_to_use: "Use when you need to know whether a feature, a tenant, or a plan tier pays for the infrastructure it consumes."
related:
  - finops.md
  - allocation.md
  - capacity.md
  - ../tenancy/noisy-neighbor.md
last_reviewed: 2026-09-25
---

# Unit economics

Unit economics here means infrastructure and direct vendor cost divided by a unit the business recognizes: an active tenant, an order, a gigabyte ingested, a seated user. It is not a full company P&L. It is the number that tells you a design is absurd before finance does.

## Defaults

- Pick one primary unit per product. Write the formula. Example: monthly cost of the search cluster divided by monthly active tenants, plus the marginal object-storage cost per stored gigabyte.
- Include the drivers that move: storage, requests, egress, support-only third parties. Exclude allocated corporate overhead unless finance requires it. Do not mix them silently.
- Recompute when the architecture changes, not only when the invoice arrives. A design review can estimate the unit cost from the same arithmetic as capacity.
- Compare tiers. If the free tier costs more per active tenant than the paid tier's price, the free tier needs a cap. That cap is a product requirement, enforced in [rate limits](../apis/rate-limiting.md) or storage quotas.
- Watch the distribution. The mean tenant can be cheap while the top tenant is the whole bill. The top tenant is either a sales conversation or a noisy-neighbor move to a silo.
- A unit cost that rises as you grow usually means a quadratic query, a fan-out, or a retained-forever log. Fix the shape. Discounting the invoice will not.

## Decide

| Unit | Reveals | Hides |
|---|---|---|
| Cost per tenant | Whether large customers are subsidized | Idle platform cost, if you only average active tenants |
| Cost per request | A hot endpoint | Storage that grows even when traffic does not |
| Cost per GB ingested | A data platform | The human cost of a broken pipeline |
| Cost per order | Commerce margins | Fixed cost of the control plane at low volume |

## Anti-patterns

- A single company-wide "cost per user" that averages a free mobile app with a regulated enterprise tenant.
- Ignoring egress because it is not in the compute budget you own.
- Optimizing unit cost by dropping the replica that the SLO requires.
- A precise model of a 2% cost and no measurement of the warehouse scan that doubled last month.
