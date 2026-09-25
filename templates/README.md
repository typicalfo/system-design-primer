---
title: "Templates"
summary: "Copyable templates for a design doc, an ADR, an RFC, a threat model, an SLO, a runbook, a postmortem, a capacity worksheet, a vendor evaluation, a production-readiness review, and a DPIA."
tags: [templates, index]
when_to_use: "Use when a human or an agent is about to write one of these documents and should start from a fixed outline."
related:
  - design-doc.md
  - adr.md
  - threat-model.md
  - slo.md
  - runbook.md
  - postmortem.md
  - capacity-estimate.md
  - rfc.md
  - vendor-evaluation.md
  - production-readiness-review.md
  - dpia.md
  - ../pack/skills/adr-writer/template.md
  - ../pack/skills/system-architect/SKILL.md
last_reviewed: 2026-09-25
---

# Templates

Copy the file, fill every section, and delete the italic guidance. Do not leave a section blank. Write "Not applicable" and the reason if a section truly does not apply.

| Template | Use |
|---|---|
| [Design doc](design-doc.md) | Requirements, estimates, sketch, data, API, and tradeoffs. Matches the [system-architect](../pack/skills/system-architect/SKILL.md) output. |
| [ADR](adr.md) | Pointer to the canonical ADR template. Do not keep a second copy. |
| [Threat model](threat-model.md) | STRIDE walk of one design. |
| [SLO](slo.md) | SLI, target, window, and error-budget policy. |
| [Runbook](runbook.md) | What on-call does when a page fires. |
| [Postmortem](postmortem.md) | Blameless write-up after an incident. |
| [Capacity estimate](capacity-estimate.md) | Arithmetic for rate, storage, bottleneck, and cost. |
| [RFC](rfc.md) | A proposal still open for comment, with a named decider. |
| [Vendor evaluation](vendor-evaluation.md) | Weighted scores, a three-year cost, and an exit plan. |
| [Production readiness review](production-readiness-review.md) | Launch evidence and a gate per service tier. |
| [DPIA](dpia.md) | GDPR Article 35 structure for a high-risk processing activity. Not legal advice. |

Worked example of a design plus a review: [pack/examples/multi-tenant-audit-log](../pack/examples/multi-tenant-audit-log/README.md).
