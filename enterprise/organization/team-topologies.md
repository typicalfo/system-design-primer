---
title: "Team topologies"
summary: "Organize teams by the kind of work they do and the way they are allowed to interact, so delivery is not an accident of the org chart."
tags: [organization, teams, topology]
when_to_use: "Use when you are splitting people around a system and need more than 'everyone owns everything' or 'one team per microservice.'"
related:
  - ownership.md
  - platform-teams.md
  - conways-law.md
  - decisions.md
last_reviewed: 2026-09-25
---

# Team topologies

[Team Topologies](https://teamtopologies.com/) (Skelton and Pais) names four team types and three interaction modes. This page is a short operational reading, not a summary of the book and not a copy of it.

## Team types

| Type | Exists to | Fails when |
|---|---|---|
| Stream-aligned | Deliver one flow of user value, end to end, including on-call for that flow | It is a layer (the "frontend team") with no path to production |
| Platform | Offer self-service capabilities so stream-aligned teams do not each reinvent CI, clusters, and observability | It becomes a ticket desk. See [platform teams](platform-teams.md) |
| Enabling | Teach a capability (testing, security, data) for a while, then leave | It stays forever and becomes a gate on every pull request |
| Complicated-subsystem | Own a piece that really needs deep specialists (a pricing engine, a codec) | You invent one for every shared library |

Most product work should sit in stream-aligned teams. The others exist to reduce their cognitive load, not to accumulate decision rights.

## Interaction modes

| Mode | Use when | Time box |
|---|---|---|
| Collaboration | Two teams must discover the boundary together | Weeks, then end it. Permanent collaboration is a merged team that has not admitted it |
| X-as-a-service | The boundary is a stable API or platform | Ongoing, with a service level |
| Facilitating | An enabling team is coaching | The length of the skill transfer |

## Defaults

- A team is small enough to share one on-call rotation and one context. If the system they own needs a diagram key, the split is wrong or the platform is missing.
- Hand-offs between "dev," "QA," and "ops" for the same change are a topology problem. The stream-aligned team should be able to ship.
- When two teams collaborate on every release, draw the boundary in the wrong place or staff a single team.
- Revisit the topology when the product changes. A map from three years ago will not match the code, and [Conway's law](conways-law.md) says the code will lose.

## Anti-patterns

- A microservice per two-pizza team slogan with no platform, producing twenty deploy pipelines and no owners.
- An architecture board that must approve every service call. That is a bottleneck with a calendar.
- Enabling teams with production approval power and no on-call.
- Splitting by technology layer so a one-line user fix needs three teams.

## Further reading

- [Team Topologies](https://teamtopologies.com/)
