---
title: "Enterprise checks for a design"
summary: "Production decisions the architect writes as requirements before the sketch, covering identity, tenancy, retention, operability, cost, and migration."
tags: [architecture, requirements, enterprise]
when_to_use: "Use when the system-architect skill is writing requirements for a system that will run in production."
related:
  - approach.md
  - ../SKILL.md
  - ../../design-reviewer/checklist.md
  - ../../../../enterprise/README.md
last_reviewed: 2026-09-25
---

# Enterprise checks for a design

[approach.md](approach.md) is the step order and the section headings. This page is the set of production decisions those requirements have to settle. Write each one as a requirement or as "not in scope", with the reason. Do not invent a control catalog. The [design reviewer](https://github.com/typicalfo/system-design-primer/blob/master/pack/skills/design-reviewer/SKILL.md) checks the same ground later.

The long-form pages live in the [enterprise guide](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/README.md). Open one when the decision is actually in play. A copied skill resolves those links on GitHub.

## Decide

| Decision | Use when | Avoid when |
|---|---|---|
| Name every caller | Users, services, and jobs all write or read | The hop is an in-process function call with no network |
| Authorize on the server | The action touches a tenant, a person, or an admin plane | You are about to trust a tenant id from the body or the query string |
| Pick an isolation model | More than one customer shares the deployment | The system is single-tenant and you say so |
| Set retention and deletion | The store keeps customer data, including backups and exports | The data is truly ephemeral and you name the TTL |
| Set residency | A contract or a law keeps data in a region | You have no such constraint, and you do not invent one |
| Name the SLO and the owner | A person will be paged, or a customer was promised a latency | The feature is a one-off script with no caller waiting |
| Name the cost driver | Stored bytes, request count, or cross-region egress can dominate | The design has no bill, and you are explicit that cost was not estimated |
| Plan the move | You are replacing a path that already has callers | The feature is new and has no old path to drain |

## Defaults

- Take the caller's identity from the credential. User-facing flows are in [OIDC and OAuth 2.0](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/identity/oidc-oauth2.md). Service callers are in [service-to-service auth](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/identity/service-to-service.md).
- Check authorization on the server for the specific action. Models are in [authorization models](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/identity/authorization-models.md).
- For a multi-tenant system, name silo, pool, or bridge, and how a noisy tenant is capped. See [isolation models](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/tenancy/isolation-models.md) and [noisy neighbors](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/tenancy/noisy-neighbor.md).
- Every store that keeps customer data gets a retention duration and a deletion path that includes backups, indexes, and exports. See [retention](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/compliance/retention.md).
- If data cannot leave a region, say which records and which region. See [residency](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/compliance/residency.md).
- Write one user-visible SLO (success, lag, or durability of an accepted write) and name the team that is paged. See [SLOs](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/observability/slos.md).
- The capacity worksheet names the cost driver. See [FinOps](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/cost/finops.md) and [capacity](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/cost/capacity.md).
- A replacement of an existing path names the drain order and how a bad version is reversed. See [database migrations](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/delivery/database-migrations.md) and [strangler fig](https://github.com/typicalfo/system-design-primer/blob/master/patterns/strangler-fig.md).

## Checklist

- Who calls this, and what proves it?
- Which permission is checked, and where does the tenant id come from?
- What is the isolation model, or why is tenancy out of scope?
- How long is data kept, and how is it deleted, including backups?
- Is there a region the data cannot leave?
- What SLO would a page fire on, and who owns that page?
- Which number on the bill grows when traffic or retention grows?
- If something already does this job, how do callers move, and how do you go back?

## Anti-patterns

- A security requirement that says "follow best practices" and names no credential, no check, and no tenant boundary.
- A retention promise of "forever" next to a deletion promise, with no tombstone or rewrite rule that makes both true.
- An SLO written as a CPU threshold, with no user-visible failure.
- A migration with no end date and no check that the new path matches the old one.
- A second region added for availability without a stated RPO. See [disaster recovery](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/reliability/disaster-recovery.md) and [multi-region](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/reliability/multi-region.md).
