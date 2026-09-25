---
title: "Enterprise guide"
summary: "Production topics the System Design Primer does not cover, split into short decision-oriented pages."
tags: [enterprise, index]
when_to_use: "Use when you are designing or reviewing a real system and the Primer chapter stops at the interview sketch."
related:
  - whats-dated.md
  - ai/README.md
  - reference-architectures/README.md
  - ../patterns/README.md
  - ../templates/README.md
  - ../pack/README.md
  - ../AGENTS.md
last_reviewed: 2026-09-25
---

# Enterprise guide

These pages sit beside the Primer. They do not replace it. Each file is one decision: when to choose something, when not to, a default, and the failure you are taking on.

If a Primer section is old, start at [what's dated](whats-dated.md).

## Identity

| Page | Decision |
|---|---|
| [OIDC and OAuth 2.0](identity/oidc-oauth2.md) | Which flow and which token |
| [SSO and SAML](identity/saml-sso.md) | When a customer IdP speaks SAML |
| [Passkeys and MFA](identity/passkeys-mfa.md) | Phishing-resistant factors, recovery, and MFA at the IdP |
| [SCIM provisioning](identity/scim-provisioning.md) | Push user and group lifecycle, and disable versus delete |
| [Authorization models](identity/authorization-models.md) | RBAC, ABAC, or ReBAC |
| [Authorization engines](identity/authorization-engines.md) | Zanzibar-style checks, Cedar, and OPA, beside the models page |
| [Service-to-service auth](identity/service-to-service.md) | Workload identity, [SPIFFE](https://spiffe.io/), mTLS |
| [Secrets](identity/secrets.md) | Where credentials live and how they rotate |

## Security

| Page | Decision |
|---|---|
| [Threat modeling](security/threat-modeling.md) | STRIDE against the diagram you have |
| [OWASP ASVS](security/owasp-asvs.md) | Which chapter covers the control |
| [Zero trust](security/zero-trust.md) | Why a VPC is not an identity |
| [Software supply chain](security/supply-chain.md) | SBOM, signing, provenance |
| [Encryption and keys](security/encryption-keys.md) | TLS, envelope encryption, per-tenant keys |
| [Post-quantum migration](security/post-quantum.md) | Final FIPS versus draft transition dates |

## Multi-tenancy

| Page | Decision |
|---|---|
| [Isolation models](tenancy/isolation-models.md) | Silo, pool, or bridge |
| [Noisy neighbors](tenancy/noisy-neighbor.md) | Caps and when to move a tenant |
| [Data and keys](tenancy/data-and-keys.md) | Tenant on every record and key |
| [Routing](tenancy/routing.md) | Home region from the credential |
| [Onboarding and offboarding](tenancy/lifecycle.md) | Provision, suspend, delete |

## Compliance and audit

| Page | Decision |
|---|---|
| [SOC 2](compliance/soc2.md) | Evidence for an attestation |
| [ISO 27001 and FedRAMP](compliance/iso27001-fedramp.md) | 2022 ISMS, and FedRAMP Rev5 versus 20x |
| [EU regulations](compliance/eu-regulations.md) | AI Act after the Omnibus, DORA, NIS2, CRA |
| [GDPR and CCPA](compliance/privacy.md) | Inventory, export, deletion |
| [HIPAA and PCI DSS](compliance/hipaa-pci.md) | Shrink the systems that touch PHI or cards |
| [Audit logs](compliance/audit-logs.md) | Tamper-evident privileged actions |
| [Data residency](compliance/residency.md) | Where copies, backups, and operators sit |
| [Retention and deletion](compliance/retention.md) | Including backups |

## Observability and operations

| Page | Decision |
|---|---|
| [Logs, metrics, and traces](observability/telemetry.md) | Which signal answers which question |
| [OpenTelemetry](observability/opentelemetry.md) | SDK plus collector |
| [SLIs, SLOs, error budgets](observability/slos.md) | The user-visible target |
| [Alerting and on-call](observability/alerting-oncall.md) | What is allowed to page |
| [Incident response](observability/incidents.md) | Roles and mitigation first |
| [Postmortems](observability/postmortems.md) | Blameless write-ups |

## Reliability

| Page | Decision |
|---|---|
| [Retries and timeouts](reliability/retries-timeouts.md) | Bounds and backoff |
| [Circuit breakers and bulkheads](reliability/circuit-breaker-bulkhead.md) | Stop waiting, isolate pools |
| [Load shedding](reliability/load-shedding.md) | Reject early |
| [Disaster recovery](reliability/disaster-recovery.md) | RPO, RTO, and a real restore |
| [Multi-region](reliability/multi-region.md) | Active-passive or active-active |
| [Cell-based architecture](reliability/cell-based-architecture.md) | Full-stack cells, a thin router, and shuffle sharding |
| [Chaos testing](reliability/chaos.md) | A hypothesis and an abort switch |

## Data

| Page | Decision |
|---|---|
| [Event-driven architecture](data/event-driven.md) | Facts, not disguised RPC |
| [Transactional outbox](data/transactional-outbox.md) | One commit for state and message |
| [CDC](data/cdc.md) | Stream the log |
| [Sagas](data/sagas.md) | Choreography or orchestration |
| [Workflow engines](data/workflow-engines.md) | Durable execution versus sagas, queues, and cron |
| [Idempotency](data/idempotency.md) | Safe retries |
| [Schema evolution](data/schema-evolution.md) | Overlap old and new |
| [Warehouse and lakehouse](data/warehouse-lakehouse.md) | Where analytical copies go |
| [Data governance](data/governance.md) | Owner, class, lineage |
| [Search](data/search.md) | Lexical and vector indexes, sync, and relevance |
| [Caching at scale](data/caching-at-scale.md) | Tiers, stampedes, hot keys, and cache sizing |

## APIs and integration

| Page | Decision |
|---|---|
| [REST, gRPC, and GraphQL](apis/styles.md) | One style per boundary |
| [Versioning](apis/versioning.md) | Compatible change versus a break |
| [Gateways](apis/gateways.md) | What belongs at the edge |
| [Rate limiting](apis/rate-limiting.md) | Token bucket and friends |
| [Webhooks](apis/webhooks.md) | Sign, retry, dedupe |
| [Contract testing](apis/contract-testing.md) | Catch breaks in CI |
| [Errors, pagination, and async work](apis/errors-pagination-async.md) | Problem details, cursors, and long-running operations |
| [Realtime](apis/realtime.md) | WebSockets, SSE, long polling, push, and fan-out |

## Delivery and platform

| Page | Decision |
|---|---|
| [CI/CD](delivery/cicd.md) | Build once, promote the digest |
| [IaC and environments](delivery/iac-environments.md) | Reviewed desired state |
| [Feature flags](delivery/feature-flags.md) | Release is not deploy |
| [Progressive delivery](delivery/progressive-delivery.md) | Canary and blue/green |
| [Database migrations](delivery/database-migrations.md) | Expand then contract |
| [Production readiness](delivery/production-readiness.md) | Launch gates by service tier |
| [Testing strategy](delivery/testing-strategy.md) | Test portfolio and load tests tied to SLOs |

## Cost

| Page | Decision |
|---|---|
| [FinOps](cost/finops.md) | Spend as an engineering signal |
| [Capacity planning](cost/capacity.md) | Headroom and lead time |
| [Unit economics](cost/unit-economics.md) | Cost per tenant, order, or GB |
| [Cost allocation](cost/allocation.md) | Showback by team and tenant |

## Organization

| Page | Decision |
|---|---|
| [Team topologies](organization/team-topologies.md) | Stream-aligned, platform, enabling |
| [Service ownership](organization/ownership.md) | One team, one pager |
| [ADRs and RFCs](organization/decisions.md) | Proposal versus decision |
| [Build versus buy](organization/build-vs-buy.md) | Weighted decision, including exit cost |
| [Software delivery metrics](organization/delivery-metrics.md) | Five DORA delivery measures |
| [Platform teams](organization/platform-teams.md) | A product whose customer is other teams |
| [Conway's law](organization/conways-law.md) | The org chart is the architecture |

## Modernization

| Page | Decision |
|---|---|
| [Strangler fig](modernization/strangler-fig.md) | Replace one capability at a time |
| [Modular monolith](modernization/modular-monolith.md) | When not to split into services |
| [Anti-corruption layer](modernization/anti-corruption-layer.md) | Keep the legacy model at the edge |

## AI systems

| Page | Decision |
|---|---|
| [AI systems index](ai/README.md) | Index of the LLM, RAG, agent, security, and eval pages |
| [LLM application architecture](ai/llm-app-architecture.md) | Gateway, routing, fallbacks, token budgets, and prompt retention |
| [RAG](ai/rag.md) | Chunking, hybrid retrieval, permission filters, and deletion of every copy |
| [Agents and tools](ai/agents-and-tools.md) | User-scoped tools, MCP, approval gates, and loop budgets |
| [LLM security](ai/llm-security.md) | Injection, exfiltration, untrusted output, and OWASP GenAI ids |
| [Evals and observability](ai/evals-and-observability.md) | Golden sets, judges, RAG metrics, and GenAI traces |

## End to end

[Reference architectures](reference-architectures/README.md) apply the pages above to five systems and include a design-review pass.

Pattern cards: [patterns/](../patterns/README.md). Copyable outlines: [templates/](../templates/README.md). Agent workflow: [AGENTS.md](../AGENTS.md).
