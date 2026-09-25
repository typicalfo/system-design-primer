---
title: "Design doc template"
summary: "Outline for a system design with requirements, estimates, a component sketch, data, API, and tradeoffs."
tags: [templates, design]
when_to_use: "Use when turning a request into a design another engineer can review."
related:
  - capacity-estimate.md
  - threat-model.md
  - slo.md
  - adr.md
  - ../pack/skills/system-architect/SKILL.md
  - ../pack/skills/system-architect/reference/approach.md
  - ../pack/skills/design-reviewer/checklist.md
last_reviewed: 2026-09-25
---

# Design doc: <name>

*One paragraph. Who calls this, what they do, and what is out of scope.*

## Functional requirements

*Observable behavior, including what a retry and a duplicate write return.*

- 

## Non-functional requirements

*Each target has a number, a unit, and a condition.*

| Target | Value | Condition |
|---|---|---|
| Latency | | |
| Durability / RPO | | |
| Availability / RTO | | |
| Consistency | | |
| Tenancy isolation | | |
| Retention | | |
| Residency | | |

## Estimates

*Show the arithmetic. Mark each input as given or assumed. Use [capacity-estimate.md](capacity-estimate.md).*

## Component sketch

```mermaid
flowchart LR
  caller[Caller]
  api[API]
  db[Store]
  caller --> api --> db
```

*For each box: what it owns, and what it explicitly does not own.*

## Data model

| Entity | Key | Store | Source of truth? | Consistency |
|---|---|---|---|---|
| | | | | |

## API

| Operation | Caller | Idempotency | Error a client may retry |
|---|---|---|---|
| | | | |

## Tradeoffs

| Choice | Alternative rejected | Cost you accept |
|---|---|---|
| | | |

## Operability

*Owner, SLO link, what pages, how to roll back, what a bad deploy does.*

## Open questions

*Facts that would change the shape of the design. Label assumptions you proceeded with.*
