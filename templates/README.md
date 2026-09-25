---
title: "Templates"
summary: "Copyable templates for a design doc, an ADR, a threat model, an SLO, a runbook, a postmortem, and a capacity worksheet."
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
  - ../pack/skills/adr-writer/template.md
  - ../pack/skills/system-architect/SKILL.md
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

Worked example of a design plus a review: [pack/examples/multi-tenant-audit-log](../pack/examples/multi-tenant-audit-log/README.md).
