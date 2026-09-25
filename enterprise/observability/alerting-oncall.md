---
title: "Alerting and on-call"
summary: "Page a named owner on user-visible symptoms that threaten the error budget, and keep a human rotation that can act."
tags: [observability, alerting, oncall]
when_to_use: "Use when you are deciding what wakes a human up versus what waits for the next business day."
related:
  - slos.md
  - telemetry.md
  - incidents.md
  - ../reliability/load-shedding.md
  - ../../templates/runbook.md
last_reviewed: 2026-09-25
---

# Alerting and on-call

An alert is a request for a human to act. If there is no action, it is a dashboard. Pages that do not require action train the rotation to sleep through the one that does.

## Decide

| Severity | Page? | Example |
|---|---|---|
| User-visible path is down or the fast error-budget burn is firing | Yes, primary on-call | Checkout error rate will exhaust the monthly budget in hours |
| Saturation will breach the SLO soon, and a human can still prevent it | Yes, if the lead time is short | Queue age past the point where catch-up is possible before the freshness SLO dies |
| Slow burn, capacity trend, certificate expiry in 14 days | Ticket, business hours | Disk will fill next month at the current rate |
| A single host is unhealthy and the fleet replaced it | No page | Autoscaler already killed it. Chart it |
| A cause metric moved (CPU on one box) but users are fine | Dashboard | High CPU with flat latency |

## Defaults

- Every page has a service owner, a severity, and a link to a [runbook](../../templates/runbook.md).
- Symptom first: "invoice write success ratio below burn threshold." Cause second, inside the runbook.
- Primary and secondary. The secondary is paged if the primary does not acknowledge within the agreed minutes.
- Handoff is a short written note: what is burning, what was changed, what to watch.
- Alert routing follows the team that ships the service. A platform team pages only for the platform's SLO, not for every tenant of that platform, unless the contract says they do.
- Silence and inhibit rules have an expiry. A silence without an expiry is how a dead region stays quiet.
- Synthetic checks hit the user path from outside the cluster. They do not replace the SLI; they catch "we forgot to measure it" and DNS failures.
- On-call load is reviewed. More than a couple of interrupt nights a week means the alerts or the system need work, not tougher heroes.

## Checklist

- [ ] A new service does not go to production without a pager route and a runbook for "it is down" and "it is slow."
- [ ] Ack and escalate times are defined.
- [ ] The alert fires in a staging drill or a unit of the rule, so a typo does not hide a real page.
- [ ] People can decline a week of on-call without heroics, and the schedule still has coverage.
- [ ] After an incident, noisy alerts are removed or fixed. They are not accepted as flavor.

## Anti-patterns

- Paging the whole company channel.
- Ten alerts for one failure (host, pod, error log, SLO, and synthetic) with no grouping.
- A runbook that says "restart the server" and nothing about how to tell if that made it worse.
- On-call for a service the team cannot roll back.
