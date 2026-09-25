---
title: "Production readiness"
summary: "Gate a service on ownership, SLOs, failure modes, restore, and rollback before it is allowed to take tier-1 traffic."
tags: [delivery, production-readiness, operations, release]
when_to_use: "Use when a new service, or a large change to one, is about to take real traffic and you need a review instead of a launch checklist in someone's head."
related:
  - cicd.md
  - testing-strategy.md
  - ../observability/slos.md
  - ../observability/alerting-oncall.md
  - ../observability/incidents.md
  - ../reliability/disaster-recovery.md
  - ../security/threat-modeling.md
  - ../../templates/production-readiness-review.md
last_reviewed: 2026-09-25
---

# Production readiness

A production readiness review asks whether this service can be operated on the day after launch, by someone who did not write it. The copyable questions live in the [production readiness review](../../templates/production-readiness-review.md) template. This page is the gate: what is required at which tier, and what "done" means.

Tiers here are this guide's defaults, not a law.

| Tier | What it is | Examples |
|---|---|---|
| 1 | Customer-facing or money- or safety-bearing, or a hard dependency of another tier-1 service | Checkout, auth, the primary datastore |
| 2 | Important, and able to degrade without taking tier 1 down | Search ranking, a notification fanout |
| 3 | Internal, low blast radius, easy to turn off | A admin report, a batch job with a retry |

## Decide

| Gate | Use when | Avoid when |
|---|---|---|
| Full tier-1 review | The service matches the tier-1 row, including a "small" service that auth depends on | You apply the full packet to a tier-3 cron and the review becomes theater |
| Tier-2 review | Failure is visible and recoverable, and another path still serves the user | The service is quietly in the request path of checkout |
| Lightweight tier-3 note | One owner, a rollback, and an alert if it stops | The job writes data you cannot rebuild. That is at least tier 2 |
| Re-review | You cross a tier boundary, change the datastore, or take a new compliance scope | Every config tweak. Review the delta |

## Defaults

- One owning team and a named on-call rotation. A service with no pager is not tier 1. See [alerting and on-call](../observability/alerting-oncall.md) and the [runbook](../../templates/runbook.md) outline.
- SLOs exist before the launch, with alerts on the burn, not on every log line. See [SLOs](../observability/slos.md) and the [SLO template](../../templates/slo.md). A dashboard shows the SLIs, the dependencies, and the saturation signals the on-call will open at 02:00.
- Dependencies and failure modes are listed: what happens when each one times out, returns errors, or is simply slow. The client has a timeout. See [CI and CD](cicd.md) for how the artifact is promoted, and [progressive delivery](progressive-delivery.md) for how traffic arrives.
- Rollback is a previous digest, a [feature flag](feature-flags.md), or both. If the change includes a migration that destroys data, the review says so and the rollback is not "redeploy yesterday."
- Security: a [threat model](../../templates/threat-model.md) for tier 1, and a review of authz on the new routes for every tier. See [threat modeling](../security/threat-modeling.md).
- Data: classification, backups, and a restore that has been done. "The vendor snapshots" is not a restore test. See [disaster recovery](../reliability/disaster-recovery.md).
- Capacity: a load-test result tied to the SLO, or an explicit statement that you have not run one and the launch is capped. See [testing strategy](testing-strategy.md).
- Cost: a rough monthly run-rate at the traffic you expect, and what doubles it. See [FinOps](../cost/finops.md).
- Compliance: admin actions and access to customer data land in the [audit log](../compliance/audit-logs.md) if the service is in scope for an attestation or a regulation you already claim.
- The review is recorded. Waivers have an owner and an expiry. A permanent waiver is a decision to change the tier or the standard.

## Gates by tier

Tier 3: owner, how to disable it, where the logs are, and what a failed run does to data.

Tier 2, plus the tier-3 items: SLO or an explicit "no SLO, and here is the user impact," dashboard, on-call, dependency list, rollback, and a backup story if it stores data you would miss.

Tier 1, plus the tier-2 items: load or capacity evidence, threat model, restore test with a date, staged rollout, audit logging where the service touches privileged or customer data, and a cost estimate.

## Checklist

- [ ] The tier is written on the service, not implied by who shouted loudest.
- [ ] A person who was not the author can follow the runbook to roll back.
- [ ] Alerts page a human who can act, and the noisy ones were deleted before launch.
- [ ] A restore test date is filled in, or the service stores nothing that matters.
- [ ] Feature flags for risky behavior default off, and the kill switch was tried.
- [ ] Waivers expire.

## Anti-patterns

- A 40-line questionnaire that is all "yes" and was filled in the day of launch.
- Tier 1 in the diagram and tier 3 in the on-call rota.
- Load testing a laptop and calling it capacity evidence.
- Rollback that has never been rehearsed because the migration already dropped the column.
- Review as a meeting with no record and no waiver list.

## Related

- [Production readiness review template](../../templates/production-readiness-review.md)
- [Progressive delivery](progressive-delivery.md)
- [Incidents](../observability/incidents.md)

## Further reading

- [SLOs](../observability/slos.md)
- [Disaster recovery](../reliability/disaster-recovery.md)
- [Threat modeling](../security/threat-modeling.md)
