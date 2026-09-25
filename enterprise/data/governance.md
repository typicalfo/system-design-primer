---
title: "Data governance"
summary: "Assign an owner, a classification, a lineage, and an access rule to data people will rely on."
tags: [data, governance, privacy, quality]
when_to_use: "Use when more than one team produces or consumes a dataset, or when personal or regulated data is copied out of the system of record."
related:
  - warehouse-lakehouse.md
  - schema-evolution.md
  - cdc.md
  - ../compliance/privacy.md
  - ../compliance/retention.md
  - ../organization/ownership.md
last_reviewed: 2026-09-25
---

# Data governance

Governance is the answer to four questions: who owns this data, what is in it, who may use it, and how it got here. Tools help. A catalog with no owners is a search box over a swamp.

## Defaults

- Every certified table, event stream, and production database has one owning team. Consumers open issues there. See [service ownership](../organization/ownership.md).
- Classification is simple and enforced: public, internal, confidential, regulated (personal, PHI, card). The class drives retention, residency, and who can query.
- A catalog entry names the grain, the freshness, the upstream source, and the SLA or the lack of one. "Best effort" is allowed. Pretending it is certified is not.
- Lineage at the dataset level is enough to start (this gold table comes from these CDC streams). Column-level lineage is worth it when you must delete or explain one field.
- Access is by group and purpose, not by shared passwords to the warehouse. Production operational roles are not the analyst role.
- Quality checks run on load: not-null keys, row counts within a band, accepted values, freshness. A failed check stops the certified table from updating, or it marks the partition bad. Silent bad data is worse than a late dashboard.
- A data contract between producer and consumer states the schema, the compatibility rule, and the retention. Breaking changes follow [schema evolution](schema-evolution.md).
- Personal-data copies are listed in the privacy inventory. A new export to a vendor updates that list. See [privacy](../compliance/privacy.md).

## Decide

| Practice | Use when | Avoid when |
|---|---|---|
| Central catalog with federated owners | Many domains publish data | You hope a central team will understand every domain's rows. They will not |
| Data mesh-style domain ownership | Domains are real teams with products | The "domain" is a layer in a diagram and nobody is on call |
| One enterprise data model | A small organization with one database | You freeze delivery on a model that tries to name every concept before shipping |

## Checklist

- [ ] The ten most-used analytical tables have a named owner and a freshness expectation.
- [ ] A new personal field cannot land in the warehouse without a classification.
- [ ] Access reviews include warehouse roles, not only production SSH.
- [ ] A producer can find its consumers before dropping a column.
- [ ] Quality failures page or ticket the owner, not the entire company.

## Anti-patterns

- A governance committee that approves models but does not own pipelines.
- Certified metrics with no test, changed by whoever edits the dashboard.
- Copying production to a personal laptop because the warehouse ticket takes a week. Fix the ticket path.
- Retention applied to the warehouse table and not to the raw files underneath.
