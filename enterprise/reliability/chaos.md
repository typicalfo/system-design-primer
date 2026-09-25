---
title: "Chaos testing"
summary: "Run a small, reversible fault with a hypothesis and an abort switch, and write down what broke."
tags: [reliability, chaos, game-day]
when_to_use: "Use when a failover, timeout, or shedder exists on paper and you need evidence it works before an incident does."
related:
  - disaster-recovery.md
  - multi-region.md
  - circuit-breaker-bulkhead.md
  - ../observability/incidents.md
  - ../../templates/runbook.md
last_reviewed: 2026-09-25
---

# Chaos testing

Chaos testing injects a fault you already believe the system handles. The result is either a confirmed control or a bug with a smaller blast radius than production discovered alone. It is not random destruction.

## Defaults

- Write the hypothesis first: "If one zone of the primary disappears, writes continue within the RTO and no acknowledged write is lost."
- Pick the smallest blast radius that tests the hypothesis: one instance, then one dependency, then one zone. Region kill comes after the smaller drills have passed.
- Abort conditions are numeric and watched by someone who is not also typing the fault: error rate, queue age, or a manual stop.
- Run with an incident lead, a timeline, and a way to undo (restore the instance, close the network rule, end the pod kill).
- Production drills need a window, a customer-communication plan if user impact is possible, and authorization. Staging drills are valid only if staging matches the failure domain you care about (same topology, smaller data).
- Start with faults that match real incidents: dependency timeout, full disk, bad deploy, certificate expiry, DNS failure, a slow database. Exotic kernel faults can wait.
- Fix what you find before you add a larger fault. A game day that produces a slide and no ticket was a demo.

## A useful sequence

| Drill | What it proves |
|---|---|
| Kill one instance | Health checks and the load balancer remove it |
| Dependency returns errors and slowness | Timeouts, breaker, and bulkhead trip; the user path degrades as designed |
| Fill the queue to its cap | Producers get a busy response and do not stampede |
| Restore from backup onto a scratch environment | RTO is real, credentials work, the runbook's first page is right |
| Lose a zone | Multi-AZ placement is actually multi-AZ, including the "hidden" single-AZ disk |
| Fail over a region | Only after the rows above, and only if multi-region is a requirement |

## Checklist

- [ ] The fault is reversible.
- [ ] Someone is watching the SLO and can stop the drill.
- [ ] The hypothesis is written where the result will be written.
- [ ] Findings become owned actions. See [postmortems](../observability/postmortems.md) if the drill became an incident.
- [ ] You do not inject faults into a data store you cannot rebuild, without a backup taken immediately beforehand.

## Anti-patterns

- A chaos tool running continuously in production on day one, with no hypothesis.
- Drills only in a single-instance staging environment that cannot show failover.
- Declaring success because the process restarted, without checking whether writes were lost.
- Skipping the drill because the provider "handles it." The provider does not handle your failover runbook.
