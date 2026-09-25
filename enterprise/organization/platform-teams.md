---
title: "Platform teams"
summary: "Run an internal platform as a product with customers, a golden path, and a support model that is not a ticket black hole."
tags: [organization, platform, developer-experience]
when_to_use: "Use when several product teams would otherwise each build CI, clusters, observability, or tenancy primitives."
related:
  - team-topologies.md
  - ownership.md
  - ../delivery/cicd.md
  - ../delivery/iac-environments.md
  - ../cost/allocation.md
---

# Platform teams

A platform team provides a paved road: the default way to deploy, observe, authenticate, and store data. Product teams can step off the road, and when they do they own the consequences. The platform's customer is the product team, not the external end user.

## Defaults

- The platform has a roadmap and a backlog taken from internal customers, not only from the platform's own interests.
- Self-service is the goal. A human ticket is a gap in the tool or the docs. Measure ticket wait time.
- The golden path is opinionated and supported: one deploy pipeline, one telemetry SDK, one way to get a database. Alternatives exist and are documented as unsupported or as a higher tier.
- SLOs exist for the platform (deploy success, cluster availability, log ingest). Product teams page the platform only when that SLO is the cause. Product bugs stay with the product on-call.
- The platform does not merge business code for product teams. If it must touch their deploy, the interface is wrong.
- Adoption is voluntary where you can make the path clearly better. Mandates without a working path create shadow platforms.
- Cost of the platform is showback to consumers using a stated rule. See [allocation](../cost/allocation.md).
- Security and tenancy primitives (identity, audit, secrets) belong on the path so product teams do not invent a weaker copy.

## Decide

| Offer as a platform product | Leave with the stream-aligned team |
|---|---|
| Cluster, ingress, CI runners, secret injection, baseline dashboards | The service's domain model and its SLO |
| A paved database with backups and a restore drill | The schema, queries, and indexes |
| An audit pipeline | Which product actions are audited |
| A golden-path service template | The business logic created from that template |

## Anti-patterns

- A platform team measured by how many tickets it closed, with no self-service.
- A "platform" that is one overloaded person with production root.
- Forcing every team onto a golden path that cannot meet a real constraint (residency, a hard latency budget), and offering no escape.
- Building a general internal PaaS before two teams have the same pain.
