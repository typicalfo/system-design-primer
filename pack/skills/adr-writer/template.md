---
title: "ADR template"
summary: "The canonical Architecture Decision Record outline: status, context, the decision, rejected alternatives, and consequences."
tags: [adr, template]
when_to_use: "Use when copying the outline for one architecture decision into the place your team keeps ADRs."
related:
  - SKILL.md
  - reference/when-to-write.md
  - ../../../enterprise/organization/decisions.md
  - ../../../templates/adr.md
last_reviewed: 2026-09-25
---

# ADR-NNNN: Title in the imperative

- Status: Proposed
- Date: YYYY-MM-DD
- Owners: team that lives with the decision

## Context

What requirement, constraint, or incident forces a choice. State the scale and the consistency or security constraint that matter. Link the design or the review finding.

## Decision

What we will do. Name the component, the data it owns, and the behavior callers can rely on.

## Alternatives rejected

### Alternative name

Why it was rejected. One concrete cost: data loss window, latency, money, operational load, or a team boundary it breaks.

### Alternative name

Why it was rejected.

## Consequences

- Easier: what this choice simplifies.
- Harder: what callers, operators, or other teams must now do.
- Accepted risk: the failure mode we are choosing to live with, and how we would notice it.
- Follow-ups: the migration, the alarm, or the next ADR this decision requires. Omit if there are none.

## Status history

| Date | Status | Note |
|---|---|---|
| YYYY-MM-DD | Proposed | |
