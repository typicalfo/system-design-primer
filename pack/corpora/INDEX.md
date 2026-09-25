---
title: "Complementary sources"
summary: "License-checked index of works the Primer does not cover, and whether each one may be copied into a skill."
tags: [sources, licenses]
when_to_use: "Use before citing SRE, ASVS, twelve-factor, Well-Architected, or microservices.io, so the license is settled before any text is copied."
related:
  - ../README.md
  - ../skills/system-architect/SKILL.md
  - ../skills/design-reviewer/SKILL.md
  - ../skills/design-reviewer/checklist.md
last_reviewed: 2026-09-25
---

# Complementary sources

Works the System Design Primer does not cover, for use with the skills in this pack. This index links to them. It does not include their text.

Licenses below were checked against the page named in the license line. "May be bundled" means the license allows redistribution under the conditions stated. This pack still only links. Anything not clearly redistributable is link-only.

| Source | URL | Covers | Used by | License | Bundle? |
|---|---|---|---|---|---|
| AWS Well-Architected Framework | https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html | Review questions for cloud workloads across six pillars: operational excellence, security, reliability, performance efficiency, cost optimization, and sustainability. Publication date on the welcome page: November 6, 2024. | [design-reviewer](../skills/design-reviewer/SKILL.md) for reliability, security, cost, and operations. [system-architect](../skills/system-architect/SKILL.md) when a tradeoff is a cloud-platform choice. | CC BY-SA 4.0. The AWS Site Terms (last updated June 4, 2025) state that documentation hosted on docs.aws.amazon.com is licensed under CC-BY-SA-4.0, and code samples there under MIT-0: https://aws.amazon.com/terms/ . The Framework URL is on that host. | May be bundled only if that copy stays under CC BY-SA 4.0 with attribution. Otherwise link only. This pack links only. |
| Google SRE books | https://sre.google/books/ | Production operations: SLOs and error budgets, monitoring, incident response, overload, cascading failure, postmortems, data integrity. Three books. | [design-reviewer](../skills/design-reviewer/SKILL.md) for SLOs, on-call, and failure behavior. [system-architect](../skills/system-architect/SKILL.md) for availability targets and overload. | Split by book, from the pages below. | Link only for the first two. The third may be bundled under its own terms. This pack links only and copies none of them. |
| Site Reliability Engineering | https://sre.google/sre-book/table-of-contents/ | How Google defines SRE, SLOs, monitoring, automation, release engineering, on-call, incidents. | Same as the row above. | CC BY-NC-ND 4.0. Footer on https://sre.google/sre-book/preface/ : "Copyright © 2017 Google, Inc. Published by O'Reilly Media, Inc. Licensed under CC BY-NC-ND 4.0." | Link only. NonCommercial and NoDerivatives block bundling into a commercial skills product and block adapted excerpts. |
| The Site Reliability Workbook | https://sre.google/workbook/table-of-contents/ | Hands-on companion: implementing SLOs, alerting, configuration, on-call practice. | [design-reviewer](../skills/design-reviewer/SKILL.md) | CC BY-NC-ND 4.0. Footer on https://sre.google/workbook/preface/ : "Copyright © 2018 Google, Inc. Published by O'Reilly Media, Inc. Licensed under CC BY-NC-ND 4.0." | Link only, for the same reason as the SRE book. |
| Building Secure and Reliable Systems | https://google.github.io/building-secure-and-reliable-systems/raw/toc.html | Security and reliability as one design problem. Linked from the SRE books page as the online edition. | [design-reviewer](../skills/design-reviewer/SKILL.md) for the security-reliability intersection. | CC BY 4.0. The publishing repo's LICENSE is Creative Commons Attribution 4.0 International: https://github.com/google/building-secure-and-reliable-systems/blob/main/LICENSE | May be bundled with attribution under CC BY 4.0. This pack links only. |
| OWASP ASVS | https://owasp.org/projects/asvs | Security requirements for web apps and web services. Current stable version used by this pack is 5.0.0 (May 2025). Chapter map: [checklist](../skills/design-reviewer/checklist.md). | [design-reviewer](../skills/design-reviewer/SKILL.md) | CC BY-SA 4.0 for the project content, stated in the repo README: https://github.com/OWASP/ASVS/blob/master/README.md and the 5.0.0 tree https://github.com/OWASP/ASVS/tree/v5.0.0 . Standard text: https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/OWASP_Application_Security_Verification_Standard_5.0.0_en.pdf | May be bundled only if that copy stays under CC BY-SA 4.0 with attribution. This pack names chapters in the checklist and does not copy requirement text. |
| The Twelve-Factor App | https://12factor.net/ | Twelve practices for services: one codebase, explicit dependencies, config in the environment, backing services as attached resources, separate build and run, stateless processes, port binding, process-model concurrency, disposability, dev/prod parity, logs as streams, admin tasks as one-off processes. | [system-architect](../skills/system-architect/SKILL.md) for stateless services, config, and logs. [design-reviewer](../skills/design-reviewer/SKILL.md) when a design pins config or session state to an instance. | MIT, Copyright (c) 2012 Adam Wiggins, in https://github.com/heroku/12factor/blob/main/LICENSE . The 12factor.net pages themselves do not repeat the license; the license verified here is that repository, which is the document's source repo. | May be bundled if the copyright notice and the MIT permission notice travel with the copy. This pack links only. |
| microservices.io patterns | https://microservices.io/patterns/index.html | A pattern language for microservice boundaries and collaboration, plus deployment, testing, and cross-cutting concerns. The homepage describes it that way. Author: Chris Richardson. | [system-architect](../skills/system-architect/SKILL.md) when splitting a system into services. [design-reviewer](../skills/design-reviewer/SKILL.md) for ownership boundaries. | All rights reserved. Homepage footer fetched from https://microservices.io/ : "Copyright © 2026 Chris Richardson • All rights reserved." No open license is stated there. | Link only. Do not copy pattern text into a skill or a design. |

## Primer license

The System Design Primer itself is CC BY 4.0, Copyright 2017 Donne Martin. Full attribution is in the [pack README](../README.md#attribution). It is the source of the method, not a gap-filler, so it is not a row above.
