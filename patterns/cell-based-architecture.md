---
title: "Cell-based architecture"
summary: "Run the workload as several full stacks, each serving a slice of tenants, so one failure does not take the product down."
tags: [reliability, isolation, cells]
when_to_use: "Use when a single shared stack's blast radius is no longer acceptable and you can route each tenant to one cell."
related:
  - shuffle-sharding.md
  - sharding.md
  - bulkhead.md
  - ../enterprise/reliability/cell-based-architecture.md
  - ../enterprise/tenancy/isolation-models.md
last_reviewed: 2026-09-25
---

# Cell-based architecture

## Problem

One database, one cache, and one deploy train mean one bad migration, one hot tenant, or one zone failure is an outage for every customer. Replication inside that stack does not create a second product. It creates a second copy of the same fate.

## When to use

- Tenants or partitions can be placed so a request names its cell.
- You can afford more than one full stack, including its data store.
- You need a deploy and a failure domain smaller than the whole fleet.
- A cell-sized outage is an acceptable customer impact. A fleet-wide outage is not.

## When not to use

- The system is still one small service. A second cell is an operations tax before it is a safety property.
- Most requests must read or write every tenant. The router cannot pick a cell.
- You will not staff the control plane. A cell design whose router and placement service are a single shared box recreates the outage.

## Tradeoffs

| You gain | You pay |
|---|---|
| A failed cell leaves the other cells up | Several stacks to patch, observe, and pay for |
| Deploys can move cell by cell | A thin router, and a placement record, that must not share the cell's fate |
| A hot tenant can be moved, or boxed in | Moving a tenant is a data copy with a cutover, not a config flag |
| A natural limit on how big one incident gets | Cross-cell queries and global uniqueness become explicit problems |

## Failure modes

- The cell router or the control plane is one deployment. It fails, and every cell is unreachable even though each cell is healthy.
- Cells grow until "one cell" is a third of revenue. The blast radius you wanted is gone.
- A migration of a tenant dual-writes badly, and both the old and the new cell accept orders.
- A deploy wave includes every cell because the pipeline has one button. The wave was the point.
- A shared dependency (identity, a third-party API, the edge certificate) sits outside the cells and takes them all down together.

## Implementation notes

- A cell is a full data-plane stack for its tenants: app, store, cache, and queue. It does not call into another cell's store on the user path.
- The router is thin. It maps an identity to a cell and stops. Placement state is not the cell database.
- Size a cell by the failure you can explain to customers, and by the operational cost of another stack. Write the number down.
- Roll out by cell. The first cell is the canary. Do not start the next wave until that cell is healthy.
- Shuffle sharding is a finer split inside a shared fleet. It is not a cell. See [shuffle sharding](shuffle-sharding.md) and the [cell-based architecture guide](../enterprise/reliability/cell-based-architecture.md).

## Related patterns

- [Shuffle sharding](shuffle-sharding.md)
- [Sharding](sharding.md)
- [Bulkhead](bulkhead.md)
