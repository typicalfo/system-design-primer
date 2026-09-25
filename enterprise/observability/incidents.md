---
title: "Incident response"
summary: "Declare early, assign roles, mitigate first, and keep a timeline that the postmortem can trust."
tags: [observability, incident, operations]
when_to_use: "Use when user impact is underway or likely, and ad-hoc chat is no longer enough to coordinate."
related:
  - alerting-oncall.md
  - postmortems.md
  - slos.md
  - ../reliability/disaster-recovery.md
  - ../../templates/runbook.md
  - ../../templates/postmortem.md
last_reviewed: 2026-09-25
---

# Incident response

An incident is a named coordination problem. The goal during the incident is to restore the user-visible promise. Understanding the root cause can wait until users are safe.

## Roles

| Role | Does | Does not |
|---|---|---|
| Incident lead | Sets severity, keeps the timeline, decides mitigate versus investigate, calls the next role | Have to be the person who types the fix |
| Operators | Change the system: rollback, shed load, fail over | Argue about the design in the same channel without a decision |
| Communications | Update status page and stakeholders on a cadence | Invent technical detail they were not given |
| Subject owner | The team that owns the hurting service | Every curious engineer. Extra people go to a side channel |

One person can hold two roles on a small team. Write that down so it is a choice.

## Defaults

- Severity is defined before you need it. Example: SEV-1 is a full outage or data-loss risk for many customers; SEV-2 is major degradation; SEV-3 is limited impact that can wait for business hours. Use your own names, but use them consistently.
- Declare in a dedicated channel. The first message states impact, start time, what you are doing now, and who the lead is.
- Mitigate in the safest reversible way: feature flag off, rollback, shed the expensive route, fail over to the passive region you have tested. See [progressive delivery](../delivery/progressive-delivery.md).
- Change one thing at a time during the incident if you can, and write down what you changed.
- Data-loss or cross-tenant suspicion raises severity even if the error rate is low. Stop the writes that make it worse.
- Customer communication says what is affected and the next update time. It does not speculate about a cause you have not checked.
- Handoffs include the timeline doc, not a verbal summary only.
- Close the incident when impact has stopped, then schedule the [postmortem](postmortems.md). Action items are not the incident channel's job to remember.

## Checklist

- [ ] There is a way to declare that does not depend on the failing system (out-of-band chat or phone).
- [ ] Rollback and feature-flag ownership are known at 2 a.m.
- [ ] A status page or a customer mailing list has an owner.
- [ ] Access to production during the incident is still named and logged.
- [ ] A drill has been run once, even as a game day on a staging failure.

## Anti-patterns

- Waiting for certainty before declaring, while users are already failing.
- Twenty people editing production with no lead.
- Fixing forward with an unreviewed patch as the first move, when a rollback exists.
- Ending with "resolved" and no record of what was rolled back.
