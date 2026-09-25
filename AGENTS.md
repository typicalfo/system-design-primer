# How to use this repo (coding agents)

This is an enterprise-augmented fork of Donne Martin's System Design Primer. The original study guide is unchanged under [Original study guide](README.md#original-study-guide) in [README.md](README.md). Solutions and translations are untouched. New material is for designing and building production systems.

License of the original work: Creative Commons Attribution 4.0 International (CC BY 4.0), Copyright 2017 Donne Martin. See [LICENSE.txt](LICENSE.txt).

## Skills

Tool-agnostic skills live in [pack/](pack/README.md). Read the `SKILL.md` and the files it links. Do not paste the Primer README in as a substitute.

| Order | Skill | File |
|---|---|---|
| 1 | Architect | [pack/skills/system-architect/SKILL.md](pack/skills/system-architect/SKILL.md) |
| 2 | Threat model | [pack/skills/threat-modeler/SKILL.md](pack/skills/threat-modeler/SKILL.md) |
| 3 | Cost | [pack/skills/cost-estimator/SKILL.md](pack/skills/cost-estimator/SKILL.md) |
| 4 | Review | [pack/skills/design-reviewer/SKILL.md](pack/skills/design-reviewer/SKILL.md) |
| 5 | Record the decision | [pack/skills/adr-writer/SKILL.md](pack/skills/adr-writer/SKILL.md) |

Run them in that order when taking a request from a blank page to a decision. Threat model and cost can swap: both need the sketch, and both should finish before review. Skip a skill the request does not need. The review uses [checklist.md](pack/skills/design-reviewer/checklist.md). The ADR copies [template.md](pack/skills/adr-writer/template.md), which is the only ADR template.

## Design workflow

1. Restate the request, requirements, and estimates with the architect skill. Use [templates/design-doc.md](templates/design-doc.md) and [templates/capacity-estimate.md](templates/capacity-estimate.md).
2. Walk threats with the threat-modeler skill when the sketch has a trust boundary. If it calls a model, also use [ai-threats](pack/skills/threat-modeler/reference/ai-threats.md).
3. Estimate cost with the cost-estimator skill when the design has a driver you will pay for. Steps 2 and 3 can swap.
4. Review with the checklist. Findings are severity-ranked. Do not invent ASVS requirement ids. Chapter names are in [enterprise/security/owasp-asvs.md](enterprise/security/owasp-asvs.md).
5. Write one ADR per durable tradeoff. Do not reopen unrelated choices in the same file.
6. Pull pattern cards and enterprise pages for the decisions the design actually makes. A component with no requirement is cut.

## Which files to load

Load the row that matches the question. Do not load the whole Primer.

| Question | Load |
|---|---|
| How do I design this feature end to end? | [system-architect](pack/skills/system-architect/SKILL.md), [approach](pack/skills/system-architect/reference/approach.md), [estimates](pack/skills/system-architect/reference/estimates.md), [design doc template](templates/design-doc.md) |
| Is this design safe to build? | [design-reviewer](pack/skills/design-reviewer/SKILL.md), [checklist](pack/skills/design-reviewer/checklist.md) |
| Record a decision | [adr-writer](pack/skills/adr-writer/SKILL.md), [canonical ADR template](pack/skills/adr-writer/template.md) |
| How should users sign in? | [OIDC and OAuth 2.0](enterprise/identity/oidc-oauth2.md), [SSO and SAML](enterprise/identity/saml-sso.md) |
| Passkeys, MFA, or step-up? | [Passkeys and MFA](enterprise/identity/passkeys-mfa.md), [OIDC and OAuth 2.0](enterprise/identity/oidc-oauth2.md) |
| Provision or deprovision from an IdP? | [SCIM](enterprise/identity/scim-provisioning.md), [tenant lifecycle](enterprise/tenancy/lifecycle.md) |
| Who may do this action? | [Authorization models](enterprise/identity/authorization-models.md) |
| Policy engine or relationship checks? | [Authorization engines](enterprise/identity/authorization-engines.md), [authorization models](enterprise/identity/authorization-models.md) |
| How do services authenticate? | [Service-to-service auth](enterprise/identity/service-to-service.md), [secrets](enterprise/identity/secrets.md), [sidecar / mesh](patterns/sidecar-service-mesh.md) |
| What are the threats? | [threat-modeler](pack/skills/threat-modeler/SKILL.md), [STRIDE reference](pack/skills/threat-modeler/reference/stride.md), [threat model template](templates/threat-model.md), [threat modeling](enterprise/security/threat-modeling.md). If the design calls a model, also [AI threats](pack/skills/threat-modeler/reference/ai-threats.md) and [LLM security](enterprise/ai/llm-security.md) |
| Which security requirement area? | [OWASP ASVS map](enterprise/security/owasp-asvs.md) |
| Post-quantum or hybrid TLS? | [Post-quantum migration](enterprise/security/post-quantum.md), [encryption and keys](enterprise/security/encryption-keys.md) |
| Multi-tenant isolation? | [Isolation models](enterprise/tenancy/isolation-models.md), [data and keys](enterprise/tenancy/data-and-keys.md), [noisy neighbors](enterprise/tenancy/noisy-neighbor.md) |
| Tenant routing, move, or delete? | [Routing](enterprise/tenancy/routing.md), [lifecycle](enterprise/tenancy/lifecycle.md), [retention](enterprise/compliance/retention.md) |
| SOC 2, privacy, HIPAA, PCI? | [SOC 2](enterprise/compliance/soc2.md), [privacy](enterprise/compliance/privacy.md), [HIPAA and PCI](enterprise/compliance/hipaa-pci.md) |
| ISO 27001 or FedRAMP? | [ISO 27001 and FedRAMP](enterprise/compliance/iso27001-fedramp.md), [SOC 2](enterprise/compliance/soc2.md) |
| EU AI Act, DORA, NIS2, or the Cyber Resilience Act? | [EU regulations](enterprise/compliance/eu-regulations.md), [privacy](enterprise/compliance/privacy.md) |
| DPIA or high-risk personal data? | [DPIA template](templates/dpia.md), [privacy](enterprise/compliance/privacy.md), [EU regulations](enterprise/compliance/eu-regulations.md) |
| Audit log? | [Audit logs](enterprise/compliance/audit-logs.md) |
| Residency or retention? | [Residency](enterprise/compliance/residency.md), [retention](enterprise/compliance/retention.md) |
| SLOs, paging, incidents? | [SLOs](enterprise/observability/slos.md), [alerting](enterprise/observability/alerting-oncall.md), [incidents](enterprise/observability/incidents.md), [templates](templates/README.md) |
| Retries, breakers, shedding? | [Retries](enterprise/reliability/retries-timeouts.md), [breakers and bulkheads](enterprise/reliability/circuit-breaker-bulkhead.md), [load shedding](enterprise/reliability/load-shedding.md) |
| RPO, RTO, second region? | [Disaster recovery](enterprise/reliability/disaster-recovery.md), [multi-region](enterprise/reliability/multi-region.md) |
| Cells or shuffle sharding? | [Cell-based architecture](enterprise/reliability/cell-based-architecture.md), [cell card](patterns/cell-based-architecture.md), [shuffle sharding](patterns/shuffle-sharding.md) |
| Events, outbox, CDC, sagas? | [Events](enterprise/data/event-driven.md), [outbox](enterprise/data/transactional-outbox.md), [CDC](enterprise/data/cdc.md), [sagas](enterprise/data/sagas.md), [idempotency](enterprise/data/idempotency.md) |
| Durable workflows versus queues? | [Workflow engines](enterprise/data/workflow-engines.md), [sagas](enterprise/data/sagas.md), [durable workflow](patterns/durable-workflow.md) |
| Search or a vector index? | [Search](enterprise/data/search.md), [RAG](enterprise/ai/rag.md) |
| Cache, shard, replicate? | [Pattern index](patterns/README.md) and the matching Primer section linked from the card |
| Cache stampedes, hot keys, or cache size? | [Caching at scale](enterprise/data/caching-at-scale.md) plus the cache pattern cards |
| REST vs gRPC vs GraphQL? | [API styles](enterprise/apis/styles.md), [versioning](enterprise/apis/versioning.md) |
| Webhooks or rate limits? | [Webhooks](enterprise/apis/webhooks.md), [rate limiting](enterprise/apis/rate-limiting.md) |
| API errors, pagination, or long-running calls? | [Errors, pagination, and async operations](enterprise/apis/errors-pagination-async.md) |
| WebSockets, SSE, or mobile push? | [Realtime](enterprise/apis/realtime.md) |
| CI, flags, migrations? | [CI/CD](enterprise/delivery/cicd.md), [feature flags](enterprise/delivery/feature-flags.md), [migrations](enterprise/delivery/database-migrations.md) |
| Ready for production? | [Production readiness](enterprise/delivery/production-readiness.md), [review template](templates/production-readiness-review.md) |
| Which tests, or a load test? | [Testing strategy](enterprise/delivery/testing-strategy.md), [contract testing](enterprise/apis/contract-testing.md) |
| What will this cost? | [cost-estimator](pack/skills/cost-estimator/SKILL.md), [method](pack/skills/cost-estimator/reference/method.md), [capacity worksheet](templates/capacity-estimate.md), [unit economics](enterprise/cost/unit-economics.md), [FinOps](enterprise/cost/finops.md) |
| Team boundaries? | [Team topologies](enterprise/organization/team-topologies.md), [ownership](enterprise/organization/ownership.md), [Conway](enterprise/organization/conways-law.md) |
| Build or buy? | [Build versus buy](enterprise/organization/build-vs-buy.md), [vendor evaluation](templates/vendor-evaluation.md) |
| Write an RFC? | [RFC template](templates/rfc.md), [ADRs and RFCs](enterprise/organization/decisions.md) |
| Delivery performance metrics? | [Software delivery metrics](enterprise/organization/delivery-metrics.md), [SLOs](enterprise/observability/slos.md) |
| An LLM application (gateway, tokens, cache)? | [LLM application architecture](enterprise/ai/llm-app-architecture.md), [AI systems](enterprise/ai/README.md) |
| RAG or grounded answers? | [RAG](enterprise/ai/rag.md), [search](enterprise/data/search.md), [RAG assistant](enterprise/reference-architectures/rag-assistant.md) |
| Agents, tools, or MCP? | [Agents and tools](enterprise/ai/agents-and-tools.md), [LLM security](enterprise/ai/llm-security.md) |
| LLM security or prompt injection? | [LLM security](enterprise/ai/llm-security.md), [AI threat prompts](pack/skills/threat-modeler/reference/ai-threats.md) |
| Evals or model traces? | [Evals and observability](enterprise/ai/evals-and-observability.md), [OpenTelemetry](enterprise/observability/opentelemetry.md) |
| Split a monolith? | [Modular monolith](enterprise/modernization/modular-monolith.md), [strangler fig](enterprise/modernization/strangler-fig.md) |
| Is the Primer section outdated? | [What's dated](enterprise/whats-dated.md) |
| Show me a full design | [Reference architectures](enterprise/reference-architectures/README.md) |

Machine-readable index: [catalog.json](catalog.json), schema version 2. It has `schema_version`, a `source_hash` over the catalogued file bytes (no commit id and no timestamp), `counts` (total, by type, and by top-level section), and `entries` sorted by path. Each entry has `path`, `type`, `section`, `title`, `summary`, `tags`, `when_to_use`, `related` (repo-relative), and `last_reviewed`. `SKILL.md` does not carry `last_reviewed`; the catalog uses the latest `last_reviewed` among the other Markdown files in that skill folder. Install [PyYAML](scripts/requirements.txt) with `pip install -r scripts/requirements.txt`, then regenerate with `python3 scripts/build_catalog.py`. That command also rewrites [llms.txt](llms.txt), [llms-full.txt](llms-full.txt), `llms-full/`, and the counts table in [README.md](README.md). `python3 scripts/build_catalog.py --check` exits non-zero if any of those drift, and it does not write. Short index for models: [llms.txt](llms.txt). Full text is indexed from [llms-full.txt](llms-full.txt). One file per section, capped at 1,000,000 bytes. Enterprise stays in `llms-full/enterprise.txt` while that rendered file is within the cap. If the rendered bundle would exceed the cap, the generator writes `llms-full/enterprise-<subfolder>.txt` and keeps docs that sit directly in `enterprise/` in `enterprise.txt`. A file that is still over the cap is an error. Nothing is deleted to get under the cap. `--check` also fails if `llms-full/` contains a file this run would not generate.

## Conventions

- New docs under `enterprise/`, `patterns/`, `templates/`, and `pack/` (except `SKILL.md`) start with YAML frontmatter: `title`, `summary`, `tags`, `when_to_use`, `related`, and `last_reviewed` as `YYYY-MM-DD`. Update `last_reviewed` when you change the page. `SKILL.md` keeps only `name` and `description`, and the description starts with "Use this when".
- Pattern cards keep the sections Problem, When to use, When not to use, Tradeoffs, Failure modes, Implementation notes, Related patterns.
- `catalog.json`, `llms.txt`, `llms-full.txt`, and `llms-full/` are generated. Do not hand-edit them.
- Cite external sources by link. State a license only when it is already verified in [pack/corpora/INDEX.md](pack/corpora/INDEX.md). Do not copy non-redistributable text (Google SRE book and workbook are CC BY-NC-ND; microservices.io is all rights reserved).
- Original Primer prose, translations, and `solutions/` are not rewritten. Additions to the English README are the fork banner, the "how to use" section, and callouts that start with `Enterprise update (fork)`.
- How to contribute: [CONTRIBUTING.md](CONTRIBUTING.md). Pull requests only; GitHub Issues are off.

## Original Primer

Interview and study material, including diagrams and exercises, starts at [Original study guide](README.md#original-study-guide). Worked interview solutions stay in [solutions/](solutions/system_design/pastebin/README.md).
