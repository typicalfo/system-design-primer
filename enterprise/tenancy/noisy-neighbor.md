---
title: "Noisy neighbors"
summary: "Cap one tenant's load so a shared pool stays fair, and move a tenant to a silo when caps are not enough."
tags: [tenancy, quotas, fairness, capacity]
when_to_use: "Use when tenants share a database, cache, queue, or worker pool and one tenant's spike can slow the others."
related:
  - isolation-models.md
  - routing.md
  - ../reliability/load-shedding.md
  - ../apis/rate-limiting.md
  - ../cost/capacity.md
  - ../../patterns/rate-limiting.md
  - ../../patterns/bulkhead.md
---

# Noisy neighbors

In a pool, the noisiest tenant sets the latency for everyone else unless you cap them. Fairness is a product decision: what you shed first, and whether a paying tier buys a higher cap or a silo.

## Decide

| Control | Use when | Avoid when |
|---|---|---|
| Rate limit per tenant | The cost is request count at the edge | One request can be a huge export. Count is the wrong unit |
| Concurrency and payload caps | A few heavy requests dominate CPU, memory, or row locks | Work is already small and uniform. A rate limit is simpler |
| Queue fair-share | Background work from one tenant fills a shared worker pool | The queue is per tenant already |
| Database statement timeout and row budget | A bad query can pin the primary | You use it as a substitute for an index. Fix the query too |
| Cell or shard by tenant tier | A class of tenants is predictably hot | You have not measured a hot tenant. Extra cells are idle cost |
| Move to silo | One tenant's contract or load justifies dedicated capacity | You silo everyone who complains once, and the pool economics die |

## Defaults

- Key limits on the authenticated tenant, not on IP. A tenant behind one NAT and an attacker with many IPs should not invert the control.
- Separate limits for interactive traffic and for exports or webhooks.
- When the tenant is over limit, reject that tenant with a clear retry hint. Do not stall the shared worker until the queue is huge.
- Reserve headroom on the shared database so the sum of tenant bursts cannot sit at 100% CPU. See [capacity](../cost/capacity.md).
- Watch saturation per tenant (CPU, rows read, queue age), not only cluster averages. The average hides the neighbor.
- Have a documented escape: temporary cap, then a bridge or silo if the tenant is legitimately larger than the pool.

## Checklist

- [ ] A load test with one tenant at 10× and the others at baseline shows the others staying inside their latency SLO, or shows the shed behavior you intended.
- [ ] Limits have owners and are visible to support, so a raised cap is not a secret edit.
- [ ] The cache and the connection pool cannot be filled by one tenant's keyspace.
- [ ] Alerts fire on one tenant burning the shared error budget, not only on the global SLO.

## Anti-patterns

- A global rate limit that locks out every customer because one integration looped.
- Unlimited "internal" jobs that skip the tenant cap and then scan that tenant's entire history on the primary.
- Autoscaling the whole fleet because one tenant is hot, and calling the bill a mystery.
- Best-effort fairness with no measurement.
