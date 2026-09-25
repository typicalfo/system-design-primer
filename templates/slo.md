---
title: "SLO template"
summary: "A one-page definition of an SLI, its target and window, and what happens when the error budget burns."
tags: [templates, slo, observability]
when_to_use: "Use when a service needs a reliability target that alerting and release policy can share."
related:
  - runbook.md
  - ../enterprise/observability/slos.md
  - ../enterprise/observability/alerting-oncall.md
  - ../pack/skills/system-architect/reference/estimates.md
---

# SLO: <service / journey>

*Owner team. Date. Link the design doc.*

## Promise

*The user-visible sentence. Example: "An accepted invoice write is durable in-region and the caller gets a response in 300 ms."*

## SLI

| Field | Value |
|---|---|
| Good event | |
| Valid event | |
| Exclusions | Health checks, and what else |
| Measurement | Metric or trace query |

SLI = good / valid over the window.

## Target

| Field | Value |
|---|---|
| Target | Example: 99.9% |
| Window | Example: 30 days rolling |
| Error budget | 1 - target, in minutes or in event count |

*Downtime arithmetic for 99.9% and 99.99% is in the [estimates reference](../pack/skills/system-architect/reference/estimates.md). Do not invent a tighter target without a cost.*

## Burn policy

| Burn | What we do |
|---|---|
| Fast (budget would exhaust in hours) | Page. Link the [runbook](runbook.md) |
| Slow (budget would exhaust in days) | Ticket the owner |
| Budget spent | Freeze risky releases or add capacity. Name which |

## Not this SLO

*Load, CPU, and queue depth are saturation signals. List the ones you will graph, and do not call them the SLO.*
