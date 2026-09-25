---
name: adr-writer
description: "Use this when recording an architecture decision: context, the decision, alternatives rejected and why, consequences, and status, as an Architecture Decision Record."
---

# ADR writer

Write one Architecture Decision Record for one decision. Use [template.md](template.md) and fill every section. When this should be an ADR rather than an RFC or a design-doc section, read [reference/when-to-write.md](reference/when-to-write.md). If the design review produced the decision, link the finding. If the architect skill produced it, link the tradeoff. Do not reopen unrelated choices in the same file.

## Rules

- The title names the decision ("Use object storage as the source of truth for audit batches"), not the problem area ("Storage").
- Context is the forces that make this a decision: requirements, scale, constraints, and what has already been ruled out. No solution yet.
- The decision is a few sentences an engineer can implement. Name the component and the behavior.
- Alternatives are real options you could have shipped. Each one says why it lost, in operational terms (latency, data loss, cost, complexity, team ownership), not "worse" or "not a fit."
- Consequences include what becomes easier, what becomes harder, and what you must now operate, secure, or budget. Name the failure you accepted.
- Status is one of: Proposed, Accepted, Deprecated, Superseded by ADR-NNNN. A new record starts as Proposed unless the user says the decision is already in force.
- Number the file `ADR-NNNN` in the title, continuing from the highest existing ADR in the place the user keeps them. If there is no set yet, start at ADR-0001.
- Keep it short enough to read in one sitting. Move diagrams and estimates back to the design; the ADR records the choice and points at them.
- Drop the YAML frontmatter when you copy template.md into the team's ADR folder. That block is catalog metadata for this repo.

When the decision needs estimates or a pattern name, use the architect references rather than inventing numbers:

- [estimates](https://github.com/typicalfo/system-design-primer/blob/master/pack/skills/system-architect/reference/estimates.md)
- [scalability](https://github.com/typicalfo/system-design-primer/blob/master/pack/skills/system-architect/reference/scalability.md)
- [data](https://github.com/typicalfo/system-design-primer/blob/master/pack/skills/system-architect/reference/data.md)

When to write an ADR instead of an RFC, and where to file it: [ADRs and RFCs](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/organization/decisions.md). The copyable pointer for humans is [templates/adr.md](https://github.com/typicalfo/system-design-primer/blob/master/templates/adr.md). It does not contain a second template. Pattern names in the decision should match a card under [patterns/](https://github.com/typicalfo/system-design-primer/blob/master/patterns/README.md).
