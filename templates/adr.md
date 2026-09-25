---
title: "ADR template pointer"
summary: "The canonical Architecture Decision Record template lives with the adr-writer skill. Copy that file, not a second variant."
tags: [templates, adr]
when_to_use: "Use when you are about to record one architecture decision and need the outline."
related:
  - ../pack/skills/adr-writer/template.md
  - ../pack/skills/adr-writer/SKILL.md
  - ../enterprise/organization/decisions.md
last_reviewed: 2026-09-25
---

# ADR template

The only ADR template in this repo is [pack/skills/adr-writer/template.md](../pack/skills/adr-writer/template.md). Copy that file into the place you keep decisions (`ADR-0001-title.md`), then fill it by following [adr-writer](../pack/skills/adr-writer/SKILL.md).

Do not paste a divergent outline here. If the template changes, it changes in that one file.

## How to file one

1. Continue the number from the highest ADR in the destination folder. Start at `ADR-0001` if there is no set.
2. Copy [template.md](../pack/skills/adr-writer/template.md).
3. One decision per file. Title the decision, not the topic area.
4. Link the design doc or the review finding that forced the choice.
5. Status starts as Proposed unless the decision is already in force.

Background on when an ADR beats an RFC: [ADRs and RFCs](../enterprise/organization/decisions.md).
