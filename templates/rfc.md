---
title: "RFC template"
summary: "Outline for a proposal several teams still have to critique: problem, goals, the proposal, alternatives, risks, rollout, and who decides."
tags: [templates, rfc, decisions]
when_to_use: "Use when a choice is still open and more than one team needs to comment before anyone commits."
related:
  - adr.md
  - design-doc.md
  - ../enterprise/organization/decisions.md
  - ../pack/skills/adr-writer/SKILL.md
  - ../pack/skills/adr-writer/reference/when-to-write.md
last_reviewed: 2026-09-25
---

# RFC: <title>

*The title names the proposal, not the area. "Put tenant events in a per-cell log" beats "Storage."*

| Field | Value |
|---|---|
| Author | |
| Status | Draft, in review, accepted, or withdrawn |
| Comment deadline | Date, and the channel |
| Decider | One person or a named group. Not "the team" |
| Design or ADR | Link. An accepted RFC becomes an [ADR](adr.md) or a decision section. It does not stay the only record |

An RFC is the discussion. An ADR is the decision after it. When to use which: [ADRs and RFCs](../enterprise/organization/decisions.md).

## Problem

*Who hurts, how often, and what is true today. No solution in this section.*

## Goals

*Observable outcomes. Each one can be checked after rollout.*

-

## Non-goals

*Choices this RFC refuses to settle, so reviewers do not expand it.*

-

## Proposal

*The design you want comments on. Name components, data ownership, and the caller-visible behavior. Link a sketch instead of pasting a second design doc. Use [design-doc.md](design-doc.md) if the whole system is undescribed.*

## Alternatives

*Real options, including "do nothing." Each one says why it is weaker for this problem: latency, data loss, cost, operational load, or a team boundary. "Not a fit" is not a reason.*

| Alternative | Why it loses, or why it is still in the running |
|---|---|
| Do nothing | |
| | |

## Risks

| Risk | How we would notice | Mitigation or accepted |
|---|---|---|
| | | |

## Rollout

*How this reaches production, how it is reversed, and what a bad first step does to data. Name the flag, the migration, or the cell wave if those are the mechanism.*

1. 
2. Rollback:

## Open questions

*Facts that would change the proposal. Mark the assumption you are proceeding with if the question is still open at the deadline.*

| Question | Owner | Needed by |
|---|---|---|
| | | |

## Decision and approvers

| Role | Name | Decision |
|---|---|---|
| Decider | | Accept, reject, or accept with the changes listed here |
| Approver (security, data, or the team that will operate it) | | |
| Consulted, not approvers | | Comment only |

*Date the decision. If it is accepted, file the ADR and link it here. Do not leave the outcome only in the comment thread.*
