---
title: "Production readiness review template"
summary: "A launch checklist with an evidence column and a gate per service tier, covering ownership, SLOs, failure, security, data, rollout, cost, and audit."
tags: [templates, delivery, production-readiness]
when_to_use: "Use before a service or a major change is called production, when someone must show evidence rather than assert readiness."
related:
  - ../enterprise/delivery/production-readiness.md
  - slo.md
  - runbook.md
  - threat-model.md
  - capacity-estimate.md
  - ../enterprise/observability/slos.md
  - ../enterprise/observability/alerting-oncall.md
  - ../enterprise/security/threat-modeling.md
last_reviewed: 2026-09-25
---

# Production readiness review: <service>

*Tier names and which rows block launch are the gates in [production readiness](../enterprise/delivery/production-readiness.md). This file is the evidence sheet for that page.*

| Field | Value |
|---|---|
| Service | |
| Owner team | |
| Tier | 1, 2, or 3, from the table below |
| Reviewer | Not the only author |
| Date | |
| Launch or change | |

Evidence is a link to a dashboard, a test run, a doc, or a commit. "We will" is not evidence. Write **Missing** and a gap owner. A waiver has an expiry. A waiver with no date is a no.

## Tier gates

| Tier | What it is | Launch rule |
|---|---|---|
| 1 | Customer-facing, or money- or safety-bearing, or a hard dependency of another tier-1 service | Every row below has evidence, or a dated waiver the approver signs |
| 2 | Important, and able to degrade without taking a tier-1 service down | Rows marked tier 2 and tier 3 have evidence. Tier-1 gaps are waived with an owner and a date |
| 3 | Internal, low blast radius, easy to turn off | Rows marked tier 3 have evidence. The rest is recorded, not blocking |

A tier-3 job that writes data you cannot rebuild is at least tier 2. A "small" service that auth or checkout depends on is tier 1.

## Checklist

| Topic | Evidence | Required from | Gap owner |
|---|---|---|---|
| Owner. One team | | Tier 3 | |
| How to disable it. Flag, config, or "do not run." Say what a failed run does to data | | Tier 3 | |
| Where the logs are, and how to query one request | | Tier 3 | |
| On-call. A pager and a secondary. No pager means this is not tier 1 | | Tier 2 | |
| SLOs and alerts, or an explicit "no SLO" with the user impact written down. What must not page | Link the [SLO](slo.md) | Tier 2 | |
| Dashboards. The SLI, saturation, and the dependency | | Tier 2 | |
| Runbook for rollback. A person who did not write the service can follow it | Link the [runbook](runbook.md) | Tier 2 | |
| Dependencies and failure modes. Timeout, errors, and slowness for each one | | Tier 2 | |
| Rollback. Previous digest, a flag, or both. If a migration already destroyed data, say that redeploy is not rollback | | Tier 2 | |
| Backup story, if the service stores data you would miss | | Tier 2 | |
| Authorization on the new routes. Who can call them, checked on the server | | Tier 3 | |
| Threat model. Boundaries walked, open items closed or accepted | Link the [threat model](threat-model.md) | Tier 1 | |
| Capacity and load-test evidence at the peak in the [worksheet](capacity-estimate.md), pass/fail tied to the SLO. Or write that you have not run one and the launch is capped | | Tier 1 | |
| Restore test. The date it last worked, the RPO, and where the backup lives | | Tier 1 | |
| Staged rollout. Which slice sees it first, and what stops the next slice | | Tier 1 | |
| Feature flag for risky behavior. Default, and who can turn it off. Write "not used" if this launch has no flag | | Tier 1 when a flag is how you stage or kill it. Tier 3 already covers a plain disable | |
| Cost estimate. Driver, monthly order of magnitude, assumptions labeled, and what doubles it | | Tier 1 | |
| Audit logging. Admin actions and access to customer data have an actor, an object, and a time | | Tier 1 when the service touches privileged or customer data | |

## Accepted gaps

| Gap | Why it does not block this tier | Owner | Date to close | How we would notice |
|---|---|---|---|---|
| | | | | |

## Decision

| Role | Name | Ship, ship with gaps, or no |
|---|---|---|
| Service owner | | |
| Reviewer | | |
| Approver for tier 1 | | |
