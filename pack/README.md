# Enterprise system design skills

A tool-agnostic skill pack for designing and reviewing production software systems. It adapts the working method of the [System Design Primer](https://github.com/donnemartin/system-design-primer) — scope the problem, sketch components, estimate, then stress the design — and adds the enterprise checks that method does not cover: identity, security requirements, compliance, operability, retention, cost, migration, and team boundaries.

The original Primer study prose is preserved in the root [README.md](../README.md) under "Original study guide". Translations and `solutions/` are unchanged. This `pack/` directory is the tool-agnostic skill workflow. The production guides around it are [enterprise/](../enterprise/README.md), [patterns/](../patterns/README.md), and [templates/](../templates/README.md). Agent entry points are [AGENTS.md](../AGENTS.md) and [llms.txt](../llms.txt). Skills are plain Markdown with YAML frontmatter so a packager can ship them without tying them to one product. Fjorj is the intended packager; nothing here calls a vendor API or depends on a vendor file layout.

## Skills

| Skill | Use |
|---|---|
| [system-architect](skills/system-architect/SKILL.md) | Turn a feature or product request into requirements, estimates, a component sketch, a data model, an API outline, and explicit tradeoffs. |
| [design-reviewer](skills/design-reviewer/SKILL.md) | Review that design. Findings are ranked by severity. The checks live in [checklist.md](skills/design-reviewer/checklist.md). |
| [adr-writer](skills/adr-writer/SKILL.md) | Record one architecture decision using [template.md](skills/adr-writer/template.md). |

Run them in that order when you are taking a request from a blank page to a decision: architect, then reviewer, then an ADR for any tradeoff the review says must be an explicit decision. Each skill tells the agent which sibling files to read, and which [enterprise](../enterprise/README.md) pages and [pattern cards](../patterns/README.md) to open for the decision in front of it. Copyable outlines are in [templates/](../templates/README.md). The ADR outline in [template.md](skills/adr-writer/template.md) is the only copy. [templates/adr.md](../templates/adr.md) points at it.

Worked quality bar: [a multi-tenant audit log](examples/multi-tenant-audit-log/README.md), with both the architect output and the reviewer output.

Numbers, patterns, and the four-step method are distilled under [skills/system-architect/reference/](skills/system-architect/reference/approach.md). Sources the Primer does not cover are indexed in [corpora/INDEX.md](corpora/INDEX.md). That index links out. It does not copy those works.

## Use the skills in any agent

The skill is the `SKILL.md` file plus the files it links to. Point the agent at that file and tell it to follow the links. Do not paste the Primer README in as a substitute.

**Generic.** Add the skill directory to the agent's skill path, or attach `SKILL.md` and say: "Follow this skill, including the files it links." The agent needs the linked reference, checklist, or template in context, not only the frontmatter.

**Cursor.** Copy or symlink each skill directory to `.cursor/skills/<skill-name>/` in the project (the folder that contains `SKILL.md`). Alternatively, add a project rule whose only instruction is to follow `pack/skills/<skill-name>/SKILL.md` when the task matches that skill's description.

**Claude Code.** Copy or symlink each skill directory to `.claude/skills/<skill-name>/`. The folder name and the `name` field in the frontmatter match (`system-architect`, `design-reviewer`, `adr-writer`).

Descriptions in the frontmatter start with "Use this when" so an agent that selects skills by description can trigger them without a slash command.

## Attribution

The design method, latency table, powers-of-two table, availability figures, and scalability patterns distilled in `skills/system-architect/reference/` are adapted from:

**The System Design Primer** by Donne Martin.
Copyright 2017 Donne Martin.
Licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
Upstream project: https://github.com/donnemartin/system-design-primer

`LICENSE.txt` in this repository states the same grant, and adds: "Because this is my personal repository, the license you receive to my code and resources is from me and not my employer (Facebook)." The license names the employer as Facebook. That sentence is part of the license text. In this repository the full license file is [`../LICENSE.txt`](../LICENSE.txt).

This pack does not copy the Primer's prose, solutions, or images. It restates the method in new words and reprints the small numerical tables (powers of two, latency, availability downtime) with attribution, because those tables are the estimation reference the method depends on. CC BY 4.0 allows that adaptation if attribution is kept. If you copy a skill directory out of this repo, keep this attribution section with it.

Other works listed in [corpora/INDEX.md](corpora/INDEX.md) stay under their own licenses. Several are not redistributable. This pack links to them and does not include their text.
