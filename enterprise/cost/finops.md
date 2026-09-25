---
title: "FinOps"
summary: "Make spend visible to the teams who cause it, and review it on a cadence with the same seriousness as an SLO."
tags: [cost, finops]
when_to_use: "Use when cloud or vendor spend is large enough that a surprise invoice is an incident."
related:
  - capacity.md
  - unit-economics.md
  - allocation.md
  - ../observability/slos.md
  - ../organization/ownership.md
  - ../../pack/skills/cost-estimator/SKILL.md
last_reviewed: 2026-09-25
---

# FinOps

FinOps is the practice of managing cloud spend as an engineering concern: see it, attribute it, and change the design when the unit cost is wrong. It is not a finance team renaming the invoice.

The [FinOps Foundation](https://www.finops.org/framework/) publishes the FinOps Framework. This page does not copy it. The engineering defaults below are enough to start.

## Defaults

- Tag or label every resource with service and team. Untagged spend is a defect, not a rounding error. See [allocation](allocation.md).
- Budgets and anomaly alerts exist per team. A 2× weekend spike should page someone who can stop it, not appear in a monthly spreadsheet.
- Engineers see their own service's cost next to its SLO. A cheaper design that misses the SLO is not a win. A design that doubles cost for no SLO gain is not a win either.
- Commitments (reserved capacity, savings plans) follow a measured baseline. Do not prepay a shape you are about to delete.
- Idle resources have an owner and a reaping rule: unattached disks, old snapshots, dev clusters left over a weekend.
- Architecture reviews include a cost line: the driver (requests, GB stored, egress, replicas) and what happens at 10×. The design reviewer already asks. See [checklist](../../pack/skills/design-reviewer/checklist.md).
- A monthly review looks at the top movers, not every line item. Action items get owners.

## Decide

| Lever | Pull it when | Leave it when |
|---|---|---|
| Rightsizing | Utilization is steadily low | The headroom is the failover capacity you promised |
| Spot or preemptible workers | Work can restart | The job holds unreplicated state |
| Storage class and retention | Logs and backups outlive their use | The retention is a contractual minimum |
| Fewer cross-region copies | Egress and replica cost dominate and residency allows | The second copy is the RPO |
| Caching | The same read is paid for on every request | The cache will be colder than the cost it adds |

## Anti-patterns

- A central team that approves every instance type and becomes the ticket queue.
- Dashboards in a currency nobody on the on-call understands, with no link to a service.
- Turning off redundancy to make a quarter's number, without changing the SLO you still advertise.
- Optimizing a 1% line item while an unbounded log pipeline is the bill.

## Further reading

- [FinOps Framework](https://www.finops.org/framework/)
