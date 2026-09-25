---
name: adr-writer
description: "Use this when recording an architecture decision: context, the decision, alternatives rejected and why, consequences, and status, as an Architecture Decision Record."
---

# ADR writer

Write one Architecture Decision Record for one decision. Use [template.md](template.md) and fill every section. If the design review produced the decision, link the finding. If the architect skill produced it, link the tradeoff. Do not reopen unrelated choices in the same file.

## Rules

- The title names the decision ("Use object storage as the source of truth for audit batches"), not the problem area ("Storage").
- Context is the forces that make this a decision: requirements, scale, constraints, and what has already been ruled out. No solution yet.
- The decision is a few sentences an engineer can implement. Name the component and the behavior.
- Alternatives are real options you could have shipped. Each one says why it lost, in operational terms (latency, data loss, cost, complexity, team ownership), not "worse" or "not a fit."
- Consequences include what becomes easier, what becomes harder, and what you must now operate, secure, or budget. Name the failure you accepted.
- Status is one of: Proposed, Accepted, Deprecated, Superseded by ADR-NNNN. A new record starts as Proposed unless the user says the decision is already in force.
- Number the file `ADR-NNNN` in the title, continuing from the highest existing ADR in the place the user keeps them. If there is no set yet, start at ADR-0001.
- Keep it short enough to read in one sitting. Move diagrams and estimates back to the design; the ADR records the choice and points at them.

When the decision needs estimates or a pattern name, use the architect references rather than inventing numbers:

- [estimates](../system-architect/reference/estimates.md)
- [scalability](../system-architect/reference/scalability.md)
- [data](../system-architect/reference/data.md)

When to write an ADR instead of an RFC, and where to file it: [ADRs and RFCs](../../../enterprise/organization/decisions.md). The copyable pointer for humans is [templates/adr.md](../../../templates/adr.md). It does not contain a second template. Pattern names in the decision should match a card under [patterns/](../../../patterns/README.md).
