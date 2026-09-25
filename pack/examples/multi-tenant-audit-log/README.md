# Worked example: multi-tenant audit log

A hand-run of the skills on one enterprise feature, so readers can see the quality bar. Nothing here is a service in this repository. The Primer solutions are untouched.

**Request.** Product services in a multi-tenant B2B platform must record who did what to which resource. Customer security teams query and export that history. Retention is part of the contract. Tenants must not see each other.

1. [design.md](design.md) is the output of [system-architect](../../skills/system-architect/SKILL.md), following its reference files.
2. [review.md](review.md) is the output of [design-reviewer](../../skills/design-reviewer/SKILL.md) applied to that design, using [checklist.md](../../skills/design-reviewer/checklist.md).

The review disagrees with the design in several places. That is the point. A review that only restates the design is not using the checklist. No ADR is included; write one with [adr-writer](../../skills/adr-writer/SKILL.md) only when a finding is accepted as a decision rather than fixed.
