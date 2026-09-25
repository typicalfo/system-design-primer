---
title: "Design review checklist"
summary: "Ordered review questions from single points of failure through ownership, plus the ASVS 5.0.0 chapter names used as citations."
tags: [review, checklist, security]
when_to_use: "Use when walking a proposed design for production gaps, one checklist section at a time."
related:
  - SKILL.md
  - ../../corpora/INDEX.md
  - ../../../enterprise/README.md
  - ../../../enterprise/security/owasp-asvs.md
last_reviewed: 2026-09-25
---

# Design review checklist

Walk in order. Each item is a question about the design in front of you. The severity scale and the output shape live in [SKILL.md](SKILL.md). Primer patterns for caches, replication, and failover live in [the architect references](https://github.com/typicalfo/system-design-primer/blob/master/pack/skills/system-architect/reference/scalability.md) and as cards under [patterns/](https://github.com/typicalfo/system-design-primer/blob/master/patterns/README.md). ASVS chapter titles below are identifiers from the OWASP ASVS 5.0.0 English sources (CC BY-SA 4.0). Requirement text is not copied; the license and the link are in [corpora/INDEX.md](https://github.com/typicalfo/system-design-primer/blob/master/pack/corpora/INDEX.md). The same chapter names are in [enterprise/security/owasp-asvs.md](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/security/owasp-asvs.md).

Guides to open when a section is in play:

| Section | Guide |
|---|---|
| Single points of failure | [Disaster recovery](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/reliability/disaster-recovery.md), [availability and failover](https://github.com/typicalfo/system-design-primer/blob/master/patterns/availability-failover.md) |
| Cache invalidation | [Cache invalidation](https://github.com/typicalfo/system-design-primer/blob/master/patterns/cache-invalidation.md) |
| Consistency and replication | [Consistency patterns](https://github.com/typicalfo/system-design-primer/blob/master/patterns/consistency-patterns.md), [data reference](https://github.com/typicalfo/system-design-primer/blob/master/pack/skills/system-architect/reference/data.md) |
| Behavior at 10× load | [Capacity](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/cost/capacity.md), [load shedding](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/reliability/load-shedding.md) |
| Failure modes | [Retries and timeouts](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/reliability/retries-timeouts.md), [circuit breaker](https://github.com/typicalfo/system-design-primer/blob/master/patterns/circuit-breaker.md) |
| Authentication and authorization | [OIDC and OAuth 2.0](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/identity/oidc-oauth2.md), [authorization models](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/identity/authorization-models.md) |
| ASVS | [Chapter map](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/security/owasp-asvs.md) |
| Compliance and audit | [Audit logs](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/compliance/audit-logs.md) |
| Observability and on-call | [SLOs](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/observability/slos.md), [alerting](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/observability/alerting-oncall.md) |
| Retention and deletion | [Retention](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/compliance/retention.md) |
| Cost | [FinOps](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/cost/finops.md) |
| Migration and rollback | [Database migrations](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/delivery/database-migrations.md), [strangler fig](https://github.com/typicalfo/system-design-primer/blob/master/patterns/strangler-fig.md) |
| Ownership | [Service ownership](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/organization/ownership.md) |

## Single points of failure

- Which components have one instance, one availability zone, one account, or one pipeline? A standby that has never taken traffic is still a single path.
- Does the load balancer, the queue, the schema store, and the secret store each have a second copy and a tested promotion path?
- Does any "pair" share a deploy, a region, or a credential so one change takes both sides out?

## Cache invalidation

- For every cache or derived index: who writes it, who invalidates it, and what is the maximum staleness a caller can observe?
- Is the source of truth still readable if the cache is empty or corrupt? A projection that can be rebuilt is acceptable; a cache that is the only copy is not a cache.
- Do write-behind entries have a durability story, or can a crash drop them? (Primer: write-behind loses data that has not reached the store.)

## Consistency and replication

- For each store, is the choice weak, eventual, or strong, and does that match the requirement on that path?
- During a partition, does the design fail the call (CP) or answer with a local copy (AP)? While healthy, does it pay synchronous latency for consistency (PACELC)? See [data.md](https://github.com/typicalfo/system-design-primer/blob/master/pack/skills/system-architect/reference/data.md).
- What is the replication lag a read can see, and which writes are lost if the primary dies before a replica acknowledges?
- Are conflicts possible because two writers accept the same key? If yes, what is the resolution rule?

## Behavior at 10× load

Multiply the design's rate, bandwidth, and hot working set by 10 using [estimates.md](https://github.com/typicalfo/system-design-primer/blob/master/pack/skills/system-architect/reference/estimates.md).

- What hits a limit first: partition throughput, connection count, disk, lock, or quota?
- Is there a hot key (one tenant, one row, one queue partition) that does not split when the average looks fine?
- Is backpressure defined (bounded queue, busy response, retry with backoff), or does the queue grow without a cap?
- Does the design add instances and leave the database, cache, and connection pool at the original size?

## Failure modes and blast radius

- Instance loss, zone loss, and region loss: what stops, what continues, and what data is destroyed rather than delayed?
- A bad deploy of each service: how far does it spread, and how is it reversed?
- Dependency loss (identity provider, queue, object store): which user-visible behavior changes, and is that behavior specified?
- Does a retry storm against a sick dependency have a timeout, a limit, and a circuit that opens?

## Authentication and authorization

- Every caller (user, service, job) has an identity. Shared long-lived API keys across tenants or services are a finding.
- Authorization is checked on the server against the authenticated identity. The tenant or account id is taken from the credential, not from an unverified body or query field.
- Admin and data-plane actions use different permissions. A token that can ingest cannot read another tenant, and a token minted for one API is not accepted by another.
- Session and token lifetime, revocation, and what happens when the identity provider is down are decided.

## Security, mapped to OWASP ASVS 5.0.0

Cite the chapter in the finding when you use this section. Do not invent `V#.#.#` requirement ids.

| Concern in the design | ASVS 5.0.0 chapter |
|---|---|
| Injection, encoding, output in the right context | V1 Encoding and Sanitization |
| Input validation and business rules | V2 Validation and Business Logic |
| Browser app, cookies, frontend sinks | V3 Web Frontend Security |
| HTTP or RPC API shape, auth on each operation | V4 API and Web Service |
| Uploads, exports, archive files | V5 File Handling |
| Passwords, MFA, credential storage | V6 Authentication |
| Session cookies and server-side session state | V7 Session Management |
| Access control, tenant isolation, function-level checks | V8 Authorization |
| JWTs and other self-contained tokens | V9 Self-contained Tokens |
| OAuth 2.0 and OpenID Connect | V10 OAuth and OIDC |
| Hashing, encryption, key handling, integrity signatures | V11 Cryptography |
| TLS and internal encrypted transport | V12 Secure Communication |
| Secrets, hardening, default-deny config | V13 Configuration |
| Classification, retention, deletion, privacy | V14 Data Protection |
| Dependency and architecture-level secure design | V15 Secure Coding and Architecture |
| Security logs, audit logs, error responses that leak internals | V16 Security Logging and Error Handling |
| Only if the design carries realtime media | V17 WebRTC |

Minimum bar even when the design is internal: TLS in transit, encryption at rest, parameterized data access, least privilege on the data stores, and no secrets in the design doc or the image.

## Compliance and audit logging

- What regulation or contract is in scope (for example SOC 2, GDPR, PCI, HIPAA, a customer DPA)? If the design claims one, the controls below have to exist. If none is stated, flag the omission for any system that stores customer data.
- Who did what, to which object, when, from where, is recorded for privileged actions. The audit record is not only the product; admin actions on the system itself are in scope (ASVS V16).
- Clock source, retention of those records, and who can alter them are decided. An audit log the operator can edit quietly does not support the claim.
- Personal data in the record is classified. A free-form blob is a finding when the store is long-lived.

## Observability and on-call

- SLIs exist for the user-visible promise (success rate, lag, durability of accepted writes), with an SLO and a window.
- Alerts page a named owner when the SLO burns, not when a single CPU graph twitches. Dashboards without a page are not on-call.
- Logs and traces cross the request id from the edge to the data store. A caller can be told, after the fact, whether their write was accepted.
- Saturation is visible before the 10× case: queue depth, replication lag, error budget.

## Data retention and deletion

- Every store has a retention duration and a deletion mechanism, including backups, indexes, and exports.
- Deletion is possible when a person asks, including when the design also promised immutability. The usual resolution is a tombstone that keeps the chain and removes the personal payload; the design has to choose it, not imply both forever.
- Legal hold can pause deletion for one tenant without pausing it for everyone.
- Backups restore to a point in time, and a restore does not resurrect data that was deleted on purpose. Say which wins.

## Cost

- The estimate names the driver: stored bytes, request count, cross-region egress, or index replicas. A design with no driver cannot be compared to an alternative.
- A 10× traffic case and a long-retention case have a cost order of magnitude, not only a latency story.
- Something alarms when spend leaves the estimate (index retention set to the legal maximum, unbounded payload size, cross-region replication turned on for the hot path).

## Migration and rollback

- Existing callers move in a defined order. Dual-running has an end date and a check that the new path matches the old one.
- A bad version is reversible: feature flag, previous deploy, or a read-only mode. Rollback does not require deleting history the system promised to keep.
- Schema or contract changes are compatible with the previous writer and the previous reader for one release.
- A poison payload can be quarantined without stopping the whole ingest path.

## Multi-team ownership boundaries

- Each service and each store has one owning team. Shared databases with several writers and no owner are a finding.
- The contract between teams is the API or the event schema, not a shared table. A schema change has a reviewer from the owning team.
- On-call and the deploy pipeline follow the owner. A platform team that "just hosts it" while product teams push schema into it needs that split written down.
- A failure in team A's service is contained so team B's data keeps its integrity guarantee.
