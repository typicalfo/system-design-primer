# Changelog

All notable changes to this fork are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project does not use version tags, so entries are not compared to tags.

## [Unreleased]

### Added

- Enterprise AI pages: LLM application architecture, RAG, agents and tools, LLM security, and evals and observability, plus the [AI systems](enterprise/ai/README.md) index.
- Reference architecture: multi-tenant RAG assistant. The index now lists five designs.
- Reliability, data, and API pages: cell-based architecture, workflow engines, search, caching at scale, API errors/pagination/async work, and realtime delivery.
- Identity, compliance, delivery, and organization pages: passkeys and MFA, SCIM, authorization engines, ISO/IEC 27001 and FedRAMP, EU regulations, build versus buy, software delivery metrics, production readiness, testing strategy, and post-quantum migration.
- Templates: RFC, vendor evaluation, production-readiness review, and DPIA.
- Skills: threat-modeler and cost-estimator. Pack order is architect, threat model, cost, review, then ADR. Threat model and cost can swap.
- Pattern cards: cell-based architecture, shuffle sharding, and durable workflow.
- `scripts/requirements.txt` pins PyYAML 6.0.2. `scripts/check_external_links.py` reports remote URL failures and exits 0 unless `--strict` is passed.
- CI: `.github/workflows/checks.yml` runs the link checker and `build_catalog.py --check` on pull requests and on pushes to `master`. `.github/workflows/external-links.yml` runs the external checker weekly and on demand, and writes the report to the job summary without failing on remote errors.
- `llms-full/` holds one full-text file per section, plus `primer.txt` (the root README, with a CC BY 4.0 attribution header). `llms-full.txt` is the index.
- Skill references `enterprise-checks.md` and `when-to-write.md`, so a copied skill can follow its core procedure without files outside its folder.
- `pack/corpora/INDEX.md` records bundle-able, share-alike, and link-only sources, including the 2025 and 2026 OWASP LLM lists and the 2026 agentic list. No text from those lists is copied.
- Citations on existing pages for NIST SP 800-207, SLSA, SPIFFE, the FinOps Framework, Martin Fowler's Strangler Fig article, Team Topologies, RFC 9700, RFC 9449, RFC 8594, RFC 9745, Standard Webhooks, and RFC 9457.
- Istio ambient mode on the sidecar and service mesh card.
- Fork note at the top of `TRANSLATIONS.md`, and "Enterprise update (fork)" callouts in the original study guide for translation scope and fork contact.
- `CHANGELOG.md`.

### Changed

- `catalog.json` is schema version 2: `schema_version`, `source_hash` (no commit id and no timestamp), `counts`, and `entries` with `last_reviewed`. Regenerate with `python3 scripts/build_catalog.py` after `pip install -r scripts/requirements.txt`. `--check` exits non-zero when a generated file drifts or when `llms-full/` contains a file this run would not generate, and it does not write.
- Catalogued docs carry `last_reviewed: 2026-09-25`. `SKILL.md` files stay limited to `name` and `description`, and the description starts with "Use this when".
- Full-text files are capped at 1,000,000 bytes. Enterprise stays one `llms-full/enterprise.txt` while that rendered file is within the cap. Over the cap, the generator splits by subfolder into `llms-full/enterprise-<subfolder>.txt`. A file that is still over the cap is an error. Nothing is deleted to get under the cap.
- Skill folders are self-contained. Links that leave a skill folder are absolute GitHub URLs. Symlink and copy install commands for Cursor and Claude Code match in the README and in `pack/README.md`.
- README landing page above "Original study guide": fork title, entry links, a 60-second skill install, and a generated counts table whose rows link to the indexes.
- OAuth guidance aligned with RFC 9700: PKCE for public clients (required) and confidential clients (recommended, and used here), no implicit grant, no resource-owner password credentials grant, sender-constrained tokens where the client can hold a key.
- API error bodies point at problem details (RFC 9457, which obsoletes RFC 7807).
- Webhook signatures follow the Standard Webhooks scheme (id, timestamp, and raw body).
- Deprecation and Sunset response headers named for API versioning.
- Event-driven orders saga order is authorize, then reserve inventory, then capture, with void and release as the compensations. `enterprise/data/sagas.md` uses the same order.
- Multi-tenant B2B SaaS durability: acknowledged writes have RPO 0 inside the region via synchronous replication. A region loss pauses the product and has no cross-region RPO.
- DORA attribution on the delivery-metrics page follows the dora.dev footer (site content licensed by Google LLC under CC BY 4.0 unless otherwise specified) and the FAQ note that research methods and survey questions are under a Creative Commons license and raw study data is not shared.
- EU AI Act dates follow Regulation (EU) 2024/1689 and Regulation (EU) 2026/1744. The deferred Article 5 points are (ba), (bb), (1a), and (1b), from 2 December 2026.
- MCP citations use specification revision 2026-07-28, the current revision on the spec site as of 2026-09-25.
- LLM security names both the 2025 and 2026 OWASP LLM editions with their ids, and the December 2025 agentic publication (ASI01–ASI10).

### Fixed

- Multi-tenant item storage: 4 × 25 × 365 × 3 = 109,500 writes per tenant, about 1.1 TB of rows, about 3.3 TB with 0.5× index overhead and one replica. The previous 219,000 / 2.2 TB / order of 7 TB double-counted that product.
- Internal platform build minutes: 250 × 5 × 10 = 12,500 build-minutes/day, about 275,000 per 22-day business month, about 375,000 if that daily rate holds for 30 calendar days. The previous figure was about 87,000 a month.
- Data platform curated storage is 20% of raw (5.84 TB/year), not 20% of the pre-amplification change rate (2.9 TB). The scan example uses the 7.2 TB raw window.
- Event-driven peak event rate is about 556/s, and provider concurrency counts authorize and capture (about 148 in flight at peak).
- Pack estimates: four-9s downtime per week is 1m 0.5s (60.48 s). The Primer prints 1m 5s.
- Audit-log object bytes include the second-region copy of the seven-year tier (83.95 TB stored, of which 58.4 TB is home-region logical).
- OWASP ASVS link is `https://owasp.org/projects/asvs`. No old OWASP API Security project URL was present to replace.

## 2026-09-25 — Enterprise augment (PR #1)

Added in [PR #1](https://github.com/typicalfo/system-design-primer/pull/1):

- Enterprise guide (`enterprise/`), including reference architectures.
- Pattern cards (`patterns/`).
- Templates (`templates/`).
- Agent skills pack (`pack/`).
- `AGENTS.md` and `CLAUDE.md`.
- `llms.txt` and `llms-full.txt`.
- `catalog.json`.
- `scripts/`.
- `CONTRIBUTING.md`.
