---
title: "Conway's law"
summary: "Expect the system to mirror team communication, and change the team boundary when you want a different system boundary."
tags: [organization, conway, architecture]
when_to_use: "Use when a proposed service split does not match how teams talk, or when a reorganization is about to redraw the architecture by accident."
related:
  - team-topologies.md
  - ownership.md
  - platform-teams.md
  - ../modernization/modular-monolith.md
  - ../modernization/strangler-fig.md
---

# Conway's law

Conway's law observes that a system design copies the communication structure of the organization that builds it. The inverse is the useful lever: if you want a certain architecture, staff and empower the teams that match it. Drawing service boxes that cross team boundaries will produce a distributed monolith with a meeting between every call.

## Defaults

- A service boundary that no team boundary matches will be leaky. Either form a team around the service or fold the service back into the team that actually talks about it.
- Cross-team calls need a contract and a compatibility rule. If the teams sit together and change both sides in one pull request, they do not have two services. They have one system with extra latency.
- A reorganization that moves people without moving on-call and repositories will leave the old architecture running under new names.
- Platform boundaries are communication boundaries too. If every deploy needs a conversation with the platform, the platform is part of every team's design, whether the diagram says so or not.
- When you want to split a monolith, start with a [modular monolith](../modernization/modular-monolith.md) whose modules match the teams you actually have. Extract a service only when a team can own it independently.
- Document the intended communication (who reviews whose API) in the ownership catalog. If the real communication differs, believe the real one and update the design.

## Decide

| You want | Staff this way | Not this way |
|---|---|---|
| Independent release of billing | A team that owns billing end to end | Billing logic spread across four teams who must release together |
| A stable edge platform | A platform team with a self-service API | Every product team editing the gateway |
| Fewer production incidents from hand-offs | One team owns the change through deploy and on-call | Separate dev and ops teams with a ticket between them |

## Anti-patterns

- An architecture diagram used as a wish that the org chart will catch up later. The code will follow the org chart first.
- Splitting a team in two and expecting their shared database to become two clean services without a project.
- A "guild" or a chat channel described as the owner of a production service.
- Ignoring the law in a small startup because it feels corporate. Two people still have a communication structure. It is just short.
