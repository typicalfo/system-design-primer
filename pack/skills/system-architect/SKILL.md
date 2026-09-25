---
name: system-architect
description: "Use this when turning a feature or product request into an enterprise system design: functional and non-functional requirements, back-of-the-envelope traffic, storage, and bandwidth estimates, a mermaid component sketch, a data model, an API outline, and explicit tradeoffs."
---

# System architect

Produce a design another engineer can review. Follow [reference/approach.md](reference/approach.md). Pull numbers from [reference/estimates.md](reference/estimates.md) and component choices from [reference/scalability.md](reference/scalability.md) and [reference/data.md](reference/data.md).

## Steps

1. Restate the request in one paragraph. List the users, the writes, the reads, and what is out of scope.
2. Write assumptions that the design depends on. If a missing fact would change the shape of the design (consistency, tenancy, retention, or the order of magnitude of traffic), ask once, then proceed with a labeled assumption if you still do not have it.
3. Write functional requirements as observable behavior, and non-functional requirements as targets you could test (latency, durability, availability, tenancy isolation, retention). For a production system, include security, privacy, and operability targets at requirement level. Do not invent a control catalog; [the design reviewer](../design-reviewer/SKILL.md) checks controls.
4. Estimate traffic, storage, and bandwidth with the formulas in the estimates reference. Show the arithmetic. Every number comes from a stated assumption or from that reference.
5. Sketch components as a mermaid diagram. For each box, say what it owns and what it explicitly does not own.
6. Specify the data model, the consistency of each store, and the API. Name replication, partitioning, and cache update strategy using the reference vocabulary.
7. End with tradeoffs. For each one, name the alternative you rejected and the concrete cost of the option you kept (data loss window, extra latency, operational burden, or money).
8. Where a Primer recommendation is marked dated in the reference, use the modern equivalent named there and say so in the tradeoff or the component note.

## Output

Emit the sections listed in [reference/approach.md](reference/approach.md), in that order. Keep the design specific to this request. Cut any component that no requirement needs.

When the user wants a review, hand the design to the design-reviewer skill. When a tradeoff must be durable, hand that single decision to the [adr-writer](../adr-writer/SKILL.md) skill.

Complementary sources, with licenses, are in [corpora/INDEX.md](../../corpora/INDEX.md). Link them. Do not copy them in.

## Where to read next

- Map of production topics: [enterprise guide](../../../enterprise/README.md). Where a Primer recommendation has aged: [what's dated](../../../enterprise/whats-dated.md).
- Pattern cards, one decision each: [patterns](../../../patterns/README.md).
- Outline to fill: [design doc](../../../templates/design-doc.md) and [capacity worksheet](../../../templates/capacity-estimate.md).
- Worked end-to-end designs: [reference architectures](../../../enterprise/reference-architectures/README.md).
