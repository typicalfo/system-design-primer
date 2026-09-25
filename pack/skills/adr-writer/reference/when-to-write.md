---
title: "When to write an ADR"
summary: "Choose an ADR to record one decision already made, an RFC while several teams still have to critique an open choice, and a design doc for the whole system."
tags: [adr, decisions]
when_to_use: "Use when you are about to record a choice and need to decide whether it is an ADR, an RFC, or a section of the design doc."
related:
  - ../template.md
  - ../SKILL.md
  - ../../../../enterprise/organization/decisions.md
  - ../../../../templates/adr.md
last_reviewed: 2026-09-25
---

# When to write an ADR

An RFC is a proposal still in discussion. An ADR is the decision after that discussion, written so it stays true when the chat history is gone. A design doc is the whole system: requirements, estimates, and a diagram. The full page is [ADRs and RFCs](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/organization/decisions.md). The outline you copy is [template.md](../template.md). [templates/adr.md](https://github.com/typicalfo/system-design-primer/blob/master/templates/adr.md) only points at that outline.

## Decide

| Artifact | Use when | Avoid when |
|---|---|---|
| RFC | Several teams must critique the choice before anyone commits, or the tradeoff is still open | The choice is local and easy to reverse |
| ADR | You picked one option, rejected others, and a later reader will ask why | You are still listing equal options. That document is an RFC |
| Design doc | The whole system needs requirements, estimates, and a sketch | You only need to record one choice. Do not paste the design into the ADR |
| Chat or a ticket | Coordination that expires | The only copy of a decision other teams have to live with |

## Defaults

- One decision per ADR. The title is the choice ("Use a transactional outbox for order events"), not the area ("Messaging").
- Status is Proposed, Accepted, Deprecated, or Superseded by a newer ADR. Do not silently rewrite an accepted decision. Supersede it.
- Each rejected alternative names the operational cost that knocked it out: data loss, latency, money, operational load, or a team boundary.
- The owner is the team that lives with the outcome.
- An RFC has a deadline and a named decider.
- Keep ADRs next to the code or in one `docs/adr` path the team actually opens. Number them. Continue from the highest number in that place, or start at `ADR-0001`.
- Drop the YAML frontmatter when you copy [template.md](../template.md) out of this repo. That block is catalog metadata.

## Checklist

- Is this one choice, or a bundle of unrelated choices that belong in separate records?
- Are the rejected options ones you could have shipped?
- Does the decision name the component and the behavior a caller can rely on?
- Does the status match whether the decision is already in force?
- Does the record point at the design or the review finding, instead of repeating them?

## Anti-patterns

- An ADR written after an incident to bless whatever shipped, with alternatives invented for the file.
- A review board that must approve every ADR, including ones inside a single team.
- An RFC that expires with no decision and is implemented halfway anyway.
- The only copy of the decision living in a pull-request description.
