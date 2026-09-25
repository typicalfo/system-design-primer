---
title: "Runbook template"
summary: "The steps on-call follows for one page, including how to tell that the mitigation worked."
tags: [templates, oncall, runbook]
when_to_use: "Use when an alert is being added and a human will be asked to act."
related:
  - slo.md
  - postmortem.md
  - ../enterprise/observability/alerting-oncall.md
  - ../enterprise/observability/incidents.md
---

# Runbook: <alert name>

| Field | Value |
|---|---|
| Service | |
| Owner | |
| Severity | |
| SLO affected | |
| Dashboard | |
| Logs / traces | How to query by request id |

## What this page means

*One or two sentences. The user-visible symptom, not the cause metric.*

## Confirm

1. Check the dashboard linked above. Is the SLI actually burning, or is this a single host the orchestrator already replaced?
2. Check the last deploy and the last flag change.
3. If this is a dependency, name which one and whether the circuit is open.

## Mitigate

*Ordered, reversible actions. Stop when the SLI recovers. Do not list five unrelated experiments.*

1. 
2. Roll back to digest `<how to find it>` or turn off flag `<name>`.
3. If data loss or cross-tenant exposure is possible, stop the writes and declare an incident. Use [incident response](../enterprise/observability/incidents.md).

## Escalate

| Condition | Who |
|---|---|
| Primary does not ack | Secondary |
| Dependency owned by another team | That team's page |
| Region or data incident | Incident lead |

## Done when

*The SLI is back inside the burn threshold for how long, and what you post in the channel.*
