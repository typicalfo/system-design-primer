---
title: "SLIs, SLOs, and error budgets"
summary: "Define a user-visible indicator, set a target over a window, and spend the error budget on purpose."
tags: [observability, sli, slo, error-budget]
when_to_use: "Use when you need to say how reliable a feature must be and how you will notice it is not."
related:
  - telemetry.md
  - alerting-oncall.md
  - incidents.md
  - ../reliability/disaster-recovery.md
  - ../../templates/slo.md
  - ../../pack/corpora/INDEX.md
  - ../organization/delivery-metrics.md
  - ../delivery/testing-strategy.md
last_reviewed: 2026-09-25
---

# SLIs, SLOs, and error budgets

An SLI is a measurement of user-visible goodness. An SLO is a target for that SLI over a window. The error budget is what you can burn and still meet the SLO: `1 - target` of the events in the window.

The Google SRE book and workbook are the long-form references and are CC BY-NC-ND 4.0 (link only). Start at <https://sre.google/books/>. The definition worksheet is [templates/slo.md](../../templates/slo.md).

## Defaults

- Write the SLI as a ratio of good events to valid events. Example: successful invoice reads faster than 300 ms, divided by all invoice reads, excluding health checks and cancelled client disconnects you have defined.
- Pick the promise a user would notice: availability of the write, freshness of a projection, durability of an accepted message. CPU is not an SLI.
- Set the window (28 or 30 days is common) and the target from the product need, not from the number of nines you wish you had. Each extra nine is a real operational cost. Primer downtime figures are in [estimates](../../pack/skills/system-architect/reference/estimates.md).
- Multi-service journeys need a journey SLI or an explicit statement that each hop's SLO multiplies. Five 99.9% hops in sequence are about 99.5%.
- Error budget policy is written before the incident: when the budget is gone, halt risky releases or add capacity. The policy is a product decision.
- Burn alerts page on fast budget consumption and ticket on slow consumption. A single 5-minute error spike that does not threaten the monthly SLO should not page at 3 a.m. unless the user impact is severe and ongoing. See [alerting](alerting-oncall.md).
- Publish the SLO next to the service owner. An SLO with no owner is a wish.

## Decide

| SLI shape | Fits | Poor fit |
|---|---|---|
| Availability (non-5xx, or explicit success code) | Request/response APIs | Async work, where the HTTP 202 is not the user's outcome |
| Latency (share under a threshold) | Interactive reads and writes | Batch jobs. Use completion time or lateness |
| Freshness | Search indexes, replicas, CDC pipelines | The source of truth itself. Measure durability there |
| Correctness / durability | "Accepted write is in the next export" | Anything you can only check by reading every row on the request path |
| Throughput | A pipeline with a promised rate | A user-facing page. Latency and errors dominate |

## Checklist

- [ ] The SLI excludes synthetic traffic or counts it separately.
- [ ] The threshold matches a number in the design's non-functional requirements.
- [ ] You can compute the SLI from telemetry you already emit, or the design adds that telemetry.
- [ ] There is a named owner and a window.
- [ ] The error budget is visible on a dashboard the team looks at during release review.

## Anti-patterns

- A 100% SLO. Any dependency makes it a lie, and the budget is zero so every error is an emergency.
- Targeting internal RPC success while the user-facing gateway times out.
- Changing the SLI after a bad week so the chart looks green.
- Alerting on the SLO target as a gauge without a burn rate, so noise trains people to ignore pages.
