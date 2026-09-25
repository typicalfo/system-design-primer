---
title: "Feature flags"
summary: "Separate release from deploy with short-lived flags, and make the off state safe when the flag service is down."
tags: [delivery, feature-flags, release]
when_to_use: "Use when you need to ship code dark, open it to a subset, or kill a path without a redeploy."
related:
  - progressive-delivery.md
  - cicd.md
  - ../observability/incidents.md
  - ../../patterns/feature-flags.md
  - ../../patterns/canary.md
---

# Feature flags

A feature flag is a runtime branch with an owner and an expiry. It lets you deploy code without exposing it, or turn off a bad path faster than a build. It is also a permanent fork in behavior if nobody deletes it.

Pattern card: [feature flags](../../patterns/feature-flags.md).

## Decide

| Kind | Lifetime | Default if the flag service is down |
|---|---|---|
| Release flag | Days to a few weeks, then delete | Off, for a new risky path. On, only if the new path is already the only safe one |
| Experiment | The length of the experiment, then delete | The control path |
| Ops kill switch | As long as the dependency it guards exists | The safe degraded mode (skip the dependency, or stop the write) |
| Permission or entitlement | Not a flag. That is authorization data | Do not invent a default that grants access |

## Defaults

- Evaluate security and entitlement on the server. A client-side flag is a UX hint. Anyone can flip it in the browser.
- Target by tenant, user cohort, or percentage. Stick a subject to a variant for the life of an experiment if you need comparable groups.
- The off path is tested. A flag you cannot turn off is a branch nobody runs until the incident.
- Flags live in a service or a config with an audit trail: who changed it, when, for whom. A flag flip is a production change.
- Cache evaluations briefly and tolerate flag-service downtime using the default above. Do not make every request fail because the flag service failed, unless the flag is an authorization decision you must not cache loosely.
- Name flags after the behavior, not after the ticket forever. Remove the branch in the cleanup PR. A cleanup ticket with no date will not happen.
- Do not nest five flags to reconstruct a state machine. That is a product you cannot test.

## Checklist

- [ ] Every release flag has an owner and a removal date.
- [ ] The incident runbook names the kill switch for each risky dependency.
- [ ] Flag changes are logged.
- [ ] A test runs both sides of a high-risk flag.
- [ ] Entitlements are not implemented as untracked flags.

## Anti-patterns

- A flag service outage that takes down checkout because evaluation throws.
- Percentage rollouts that re-randomize every request, so one user sees both variants.
- Flags checked only in the UI, with the API always on.
- Hundreds of stale flags, one of which still guards a security fix someone might turn off.
