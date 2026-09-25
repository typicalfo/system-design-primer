# How to use this repo (coding agents)

This is an enterprise-augmented fork of Donne Martin's System Design Primer. The original study guide is unchanged under [Original study guide](README.md#original-study-guide) in [README.md](README.md). Solutions and translations are untouched. New material is for designing and building production systems.

License of the original work: Creative Commons Attribution 4.0 International (CC BY 4.0), Copyright 2017 Donne Martin. See [LICENSE.txt](LICENSE.txt).

## Skills

Tool-agnostic skills live in [pack/](pack/README.md). Read the `SKILL.md` and the files it links. Do not paste the Primer README in as a substitute.

| Order | Skill | File |
|---|---|---|
| 1 | Architect | [pack/skills/system-architect/SKILL.md](pack/skills/system-architect/SKILL.md) |
| 2 | Review | [pack/skills/design-reviewer/SKILL.md](pack/skills/design-reviewer/SKILL.md) |
| 3 | Record the decision | [pack/skills/adr-writer/SKILL.md](pack/skills/adr-writer/SKILL.md) |

Run them in that order when taking a request from a blank page to a decision. The review uses [checklist.md](pack/skills/design-reviewer/checklist.md). The ADR copies [template.md](pack/skills/adr-writer/template.md), which is the only ADR template.

## Design workflow

1. Restate the request, requirements, and estimates with the architect skill. Use [templates/design-doc.md](templates/design-doc.md) and [templates/capacity-estimate.md](templates/capacity-estimate.md).
2. Review with the checklist. Findings are severity-ranked. Do not invent ASVS requirement ids. Chapter names are in [enterprise/security/owasp-asvs.md](enterprise/security/owasp-asvs.md).
3. Write one ADR per durable tradeoff. Do not reopen unrelated choices in the same file.
4. Pull pattern cards and enterprise pages for the decisions the design actually makes. A component with no requirement is cut.

## Which files to load

Load the row that matches the question. Do not load the whole Primer.

| Question | Load |
|---|---|
| How do I design this feature end to end? | [system-architect](pack/skills/system-architect/SKILL.md), [approach](pack/skills/system-architect/reference/approach.md), [estimates](pack/skills/system-architect/reference/estimates.md), [design doc template](templates/design-doc.md) |
| Is this design safe to build? | [design-reviewer](pack/skills/design-reviewer/SKILL.md), [checklist](pack/skills/design-reviewer/checklist.md) |
| Record a decision | [adr-writer](pack/skills/adr-writer/SKILL.md), [canonical ADR template](pack/skills/adr-writer/template.md) |
| How should users sign in? | [OIDC and OAuth 2.0](enterprise/identity/oidc-oauth2.md), [SSO and SAML](enterprise/identity/saml-sso.md) |
| Who may do this action? | [Authorization models](enterprise/identity/authorization-models.md) |
| How do services authenticate? | [Service-to-service auth](enterprise/identity/service-to-service.md), [secrets](enterprise/identity/secrets.md), [sidecar / mesh](patterns/sidecar-service-mesh.md) |
| What are the threats? | [STRIDE](enterprise/security/threat-modeling.md), [threat model template](templates/threat-model.md) |
| Which security requirement area? | [OWASP ASVS map](enterprise/security/owasp-asvs.md) |
| Multi-tenant isolation? | [Isolation models](enterprise/tenancy/isolation-models.md), [data and keys](enterprise/tenancy/data-and-keys.md), [noisy neighbors](enterprise/tenancy/noisy-neighbor.md) |
| Tenant routing, move, or delete? | [Routing](enterprise/tenancy/routing.md), [lifecycle](enterprise/tenancy/lifecycle.md), [retention](enterprise/compliance/retention.md) |
| SOC 2, privacy, HIPAA, PCI? | [SOC 2](enterprise/compliance/soc2.md), [privacy](enterprise/compliance/privacy.md), [HIPAA and PCI](enterprise/compliance/hipaa-pci.md) |
| Audit log? | [Audit logs](enterprise/compliance/audit-logs.md) |
| Residency or retention? | [Residency](enterprise/compliance/residency.md), [retention](enterprise/compliance/retention.md) |
| SLOs, paging, incidents? | [SLOs](enterprise/observability/slos.md), [alerting](enterprise/observability/alerting-oncall.md), [incidents](enterprise/observability/incidents.md), [templates](templates/README.md) |
| Retries, breakers, shedding? | [Retries](enterprise/reliability/retries-timeouts.md), [breakers and bulkheads](enterprise/reliability/circuit-breaker-bulkhead.md), [load shedding](enterprise/reliability/load-shedding.md) |
| RPO, RTO, second region? | [Disaster recovery](enterprise/reliability/disaster-recovery.md), [multi-region](enterprise/reliability/multi-region.md) |
| Events, outbox, CDC, sagas? | [Events](enterprise/data/event-driven.md), [outbox](enterprise/data/transactional-outbox.md), [CDC](enterprise/data/cdc.md), [sagas](enterprise/data/sagas.md), [idempotency](enterprise/data/idempotency.md) |
| Cache, shard, replicate? | [Pattern index](patterns/README.md) and the matching Primer section linked from the card |
| REST vs gRPC vs GraphQL? | [API styles](enterprise/apis/styles.md), [versioning](enterprise/apis/versioning.md) |
| Webhooks or rate limits? | [Webhooks](enterprise/apis/webhooks.md), [rate limiting](enterprise/apis/rate-limiting.md) |
| CI, flags, migrations? | [CI/CD](enterprise/delivery/cicd.md), [feature flags](enterprise/delivery/feature-flags.md), [migrations](enterprise/delivery/database-migrations.md) |
| Cost? | [FinOps](enterprise/cost/finops.md), [capacity](enterprise/cost/capacity.md), [allocation](enterprise/cost/allocation.md) |
| Team boundaries? | [Team topologies](enterprise/organization/team-topologies.md), [ownership](enterprise/organization/ownership.md), [Conway](enterprise/organization/conways-law.md) |
| Split a monolith? | [Modular monolith](enterprise/modernization/modular-monolith.md), [strangler fig](enterprise/modernization/strangler-fig.md) |
| Is the Primer section outdated? | [What's dated](enterprise/whats-dated.md) |
| Show me a full design | [Reference architectures](enterprise/reference-architectures/README.md) |

Machine-readable index of every catalogued doc: [catalog.json](catalog.json). Regenerate with `python3 scripts/build_catalog.py`. Short index for models: [llms.txt](llms.txt).

## Conventions

- New docs under `enterprise/`, `patterns/`, and `templates/` start with YAML frontmatter: `title`, `summary`, `tags`, `when_to_use`, `related`.
- Pattern cards keep the sections Problem, When to use, When not to use, Tradeoffs, Failure modes, Implementation notes, Related patterns.
- `catalog.json` is generated. Do not hand-edit it.
- Cite external sources by link. State a license only when it is already verified in [pack/corpora/INDEX.md](pack/corpora/INDEX.md). Do not copy non-redistributable text (Google SRE book and workbook are CC BY-NC-ND; microservices.io is all rights reserved).
- Original Primer prose, translations, and `solutions/` are not rewritten. Additions to the English README are the fork banner, the "how to use" section, and callouts that start with `Enterprise update (fork)`.
- How to contribute: [CONTRIBUTING.md](CONTRIBUTING.md). Pull requests only; GitHub Issues are off.

## Original Primer

Interview and study material, including diagrams and exercises, starts at [Original study guide](README.md#original-study-guide). Worked interview solutions stay in [solutions/](solutions/system_design/pastebin/README.md).
