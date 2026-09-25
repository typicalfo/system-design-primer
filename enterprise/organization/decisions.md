---
title: "ADRs and RFCs"
summary: "Use an RFC to shape a proposal with the people it affects, and an ADR to record the decision you actually made."
tags: [organization, adr, rfc, decisions]
when_to_use: "Use when a choice will be expensive to reverse, or when a later reader will otherwise relitigate it in a pull request."
related:
  - ownership.md
  - team-topologies.md
  - ../../templates/adr.md
  - ../../pack/skills/adr-writer/SKILL.md
  - ../../pack/skills/adr-writer/template.md
last_reviewed: 2026-09-25
---

# ADRs and RFCs

An RFC (request for comments) is a proposal in flight. An ADR (architecture decision record) is the decision after the discussion, written so it stays true even if the chat history disappears. They are short on purpose.

The canonical ADR template for this repo is [pack/skills/adr-writer/template.md](../../pack/skills/adr-writer/template.md). [templates/adr.md](../../templates/adr.md) points at it. The skill that fills it is [adr-writer](../../pack/skills/adr-writer/SKILL.md).

## Decide

| Artifact | Use when | Avoid when |
|---|---|---|
| RFC | Several teams must critique a design before you commit, or the tradeoff is still open | The choice is local and reversible. Write the ADR or just the code |
| ADR | You chose one option and rejected others, and someone will ask why next year | You are still brainstorming. An ADR that lists five equal options is an RFC |
| Design doc | The whole system needs requirements, estimates, and a diagram | You only need to record one choice. Do not paste the design doc into the ADR |
| Chat or ticket | Ephemeral coordination | The only copy of a decision that binds other teams |

## Defaults

- One decision per ADR. Title it as the choice ("Use a transactional outbox for order events"), not the area ("Messaging").
- Status is Proposed, Accepted, Deprecated, or Superseded by a newer ADR. Do not silently edit an accepted ADR's decision. Supersede it.
- Alternatives are real, each with the cost that knocked it out.
- The owner is the team that lives with the outcome.
- RFCs have a deadline and a decider. A comment thread with no decider is a delay.
- Store ADRs next to the code or in a single `docs/adr` path the team actually opens. Link them from the design.
- Number them. `ADR-0007` beats "final-final."

## Anti-patterns

- An ADR written after the incident to bless whatever shipped, with invented alternatives.
- A mandatory architecture review for every ADR, including ones inside a team boundary.
- RFCs that expire into nothing and are implemented halfway anyway.
- Recording the decision only in the pull-request description of a 2,000-line change.
