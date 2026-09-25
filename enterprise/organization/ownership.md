---
title: "Service ownership"
summary: "Give every service and store one owning team that ships it, runs it, and answers for its data."
tags: [organization, ownership, oncall]
when_to_use: "Use when more than one team touches a system and you need to know who is paged and who may change the schema."
related:
  - team-topologies.md
  - platform-teams.md
  - decisions.md
  - ../observability/alerting-oncall.md
  - ../data/governance.md
  - delivery-metrics.md
  - ../delivery/production-readiness.md
last_reviewed: 2026-09-25
---

# Service ownership

Ownership means one team can change the service, is paged for its SLO, and is accountable for the data it stores. Shared ownership without a named team is how incidents stall while people debate whose queue it is.

## Defaults

- One service, one on-call team. Dependencies are called, not co-owned.
- The contract is the API or the event, not a table other teams write. A second writer is a second owner you did not staff.
- Schema changes are reviewed by the owning team. See [schema evolution](../data/schema-evolution.md).
- The deploy pipeline and the pager route name the same team. A platform that deploys your code while you hold the pager is acceptable only if both sides have agreed the split, including who rolls back.
- Libraries are not services. A shared library has owners and a release process, but it does not have an SLO. The service that linked it does.
- "You build it, you run it" applies inside the team's boundary. It does not mean every team builds a database. The platform owns the database product. The service team owns the schema and the queries.
- Handoffs to a separate operations team, if they exist, are documented: what is automated, what still needs the product team at 2 a.m., and which runbook is whose.
- Orphan services (no commits, no owner in the catalog) are either assigned or turned off. They are not left routing traffic.

## Checklist

- [ ] The service catalog lists an owner and a pager for every production deployable and every production datastore.
- [ ] Two teams do not migrate the same table.
- [ ] A failing dependency has a team to escalate to, and that path is in the runbook.
- [ ] Ownership survives reorganizations because it is recorded next to the code, not only in a slide.

## Anti-patterns

- A codeowners file that lists a defunct mailing list.
- "The committee owns it."
- A shared database with a different team per table and no migration owner.
- On-call assigned to whoever most recently touched the repo.
