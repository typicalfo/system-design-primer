# Changelog

All notable changes to this fork are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project does not use version tags, so entries are not compared to tags.

## [Unreleased]

### Added

- `scripts/requirements.txt` pins PyYAML 6.0.2 for the catalog generator.
- `scripts/check_external_links.py` requests external URLs and exits 0 unless `--strict` is passed.
- `.github/workflows/checks.yml` runs the link checker and `build_catalog.py --check` on pull requests and on pushes to `master`.
- `.github/workflows/external-links.yml` runs the external link checker weekly and on demand, and writes the report to the job summary without failing on remote errors.
- `llms-full/` holds one full-text file per section, plus `primer.txt` (the root README, with a CC BY 4.0 attribution header). `llms-full.txt` is the index.
- `pack/skills/system-architect/reference/enterprise-checks.md` and `pack/skills/adr-writer/reference/when-to-write.md`, so a copied skill can follow its core procedure without files outside its folder.
- Citations for NIST SP 800-207, SLSA, SPIFFE, the FinOps Framework, Martin Fowler's Strangler Fig article, Team Topologies, RFC 9700, RFC 9449, RFC 8594, RFC 9745, Standard Webhooks, and RFC 9457, each checked to return HTTP 200.
- Istio ambient mode (ztunnel and optional waypoints) on the sidecar and service mesh card, with the 1.24 GA announcement linked.
- Fork note at the top of `TRANSLATIONS.md`.
- "Enterprise update (fork)" callouts in the original study guide for translation scope and fork contact.
- Placeholder `enterprise/ai/README.md` so the README link resolves.

### Changed

- `catalog.json` is schema version 2: `schema_version`, `source_hash`, `counts`, and `entries` with `last_reviewed`. `scripts/build_catalog.py` reads frontmatter with PyYAML, writes `llms.txt` and the README counts table, and `--check` fails if a generated file drifts.
- Catalogued docs carry `last_reviewed: 2026-09-25`. `SKILL.md` files stay limited to `name` and `description`.
- Skill folders are self-contained. Links that leave a skill folder are absolute GitHub URLs. Symlink and copy install commands for Cursor and Claude Code match in the README and in `pack/README.md`.
- README landing page above "Original study guide": pitch, three entry links, a 60-second skill install, and a counts table.
- OAuth guidance aligned with RFC 9700: PKCE for public clients (required) and confidential clients (recommended, and used here), no implicit grant, no resource-owner password credentials grant, sender-constrained tokens where the client can hold a key.
- API error bodies point at problem details (RFC 9457, which obsoletes RFC 7807).
- Webhook signatures follow the Standard Webhooks scheme (id, timestamp, and raw body).
- Deprecation and Sunset response headers named for API versioning.
- Event-driven orders saga order is authorize, then reserve inventory, then capture, with void and release as the compensations. `enterprise/data/sagas.md` uses the same order.
- Multi-tenant B2B SaaS durability: acknowledged writes have RPO 0 inside the region via synchronous replication. A region loss pauses the product and has no cross-region RPO.

### Fixed

- Multi-tenant item storage: 4 × 25 × 365 × 3 = 109,500 writes per tenant, about 1.1 TB of rows, about 3.3 TB with 0.5× index overhead and one replica. The previous 219,000 / 2.2 TB / order of 7 TB double-counted that product.
- Internal platform build minutes: 250 × 5 × 10 = 12,500 build-minutes/day, 275,000 per 22-day month, 375,000 per 30-day month, with runner concurrency derived from that daily total. The previous figure was about 87,000 a month.
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
