---
title: "Warehouse and lakehouse"
summary: "Keep operational stores for transactions, and land analytical copies in a warehouse or a table format on object storage."
tags: [data, warehouse, lakehouse, analytics]
when_to_use: "Use when people need historical, cross-cutting queries that must not run on the transactional database."
related:
  - cdc.md
  - governance.md
  - schema-evolution.md
  - ../compliance/retention.md
  - ../compliance/privacy.md
  - ../cost/unit-economics.md
last_reviewed: 2026-09-25
---

# Warehouse and lakehouse

The operational database serves the product's transactions. Analytical queries (long scans, joins across domains, data science) belong on a copy. A warehouse is a managed analytical store with its own tables and SQL. A lake is object storage holding files. A lakehouse puts a table format (Iceberg, Delta, or Hudi are the common ones) on that storage so you get schema, transactional-ish commits, and time travel without loading everything into a proprietary warehouse engine.

## Decide

| Shape | Use when | Avoid when |
|---|---|---|
| Replica of the OLTP database | A few operational reports, same schema, modest scan size | Analysts will run ad hoc joins that compete with product traffic. Even a replica can hurt the primary via the log |
| Warehouse | BI users, governed metrics, mostly SQL, you accept the vendor's storage model | You must land raw files cheaply and process them with engines you swap |
| Lake of files only | Raw landing and data-science experiments | The business needs stable tables, grants, and incremental updates. Files alone become a swamp |
| Lakehouse table format | Large data on object storage, multiple engines (SQL, Spark), incremental CDC merges | The team is small and a single warehouse would answer the questions with less machinery |

## Defaults

- Land CDC or events into a raw zone (often called bronze). Do not treat raw as a certified dataset.
- Curate a cleaned zone (silver) and a business-facing zone (gold, or a metrics layer) with owners and tests. Names are a convention. Ownership is the requirement.
- The product's API is not "connect your BI tool to the primary." Give analysts the curated tables.
- Incremental loads are idempotent (merge on primary key, or replace a partition by date). Re-running a day does not double the revenue chart.
- Partition by a date or another coarse key you actually filter on. Partitioning by tenant when you have millions of tenants creates a metadata problem. Filter tenant inside a coarser partition, or isolate only the tenants that require it.
- Time travel and snapshots help reproduce a report. They also retain deleted personal data unless you expire snapshots. Align that with [retention](../compliance/retention.md).
- Cost is per scan or per byte stored. A dashboard that full-scans a year of events every five minutes is a capacity bug. See [unit economics](../cost/unit-economics.md).

## Checklist

- [ ] The transactional p99 does not depend on an analytical query.
- [ ] Every certified table has an owner and a definition for its grain (one row per order, per user-day, and so on).
- [ ] A re-run of the loader is safe.
- [ ] Personal data in the raw zone has a deletion path.
- [ ] Freshness is an SLO if someone will act on the table during the day.

## Anti-patterns

- One shared "analytics" database user with access to every raw tenant payload.
- Building the lakehouse before anyone has a question the replica cannot answer.
- Metrics defined differently in each dashboard because there is no owned gold table.
- ETL that fails silently and serves yesterday's partition as if it were today.
