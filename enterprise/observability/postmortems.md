---
title: "Blameless postmortems"
summary: "Write what happened, why the system allowed it, and which actions will change the system, without blaming a person."
tags: [observability, postmortem, incident]
when_to_use: "Use after a SEV-1 or SEV-2 incident, a near miss that would have been one, or any customer-impacting data incident."
related:
  - incidents.md
  - alerting-oncall.md
  - slos.md
  - ../../templates/postmortem.md
last_reviewed: 2026-09-25
---

# Blameless postmortems

Blameless means the write-up assumes the person did a reasonable thing with the information and tools they had. The fix is a change to the system, the runbook, the alert, or the staffing. It is not a request for someone to be more careful.

The copyable structure is [templates/postmortem.md](../../templates/postmortem.md).

## Defaults

- Write it within a few days, while logs still exist and memories agree with the timeline.
- Timeline is in UTC with sources (alert id, deploy id, dashboard). Separate what was later learned from what the responder knew then.
- Impact is user-facing: who, how many, how long, whether data was wrong or only delayed. Tie it to the SLO and the error budget if you have one.
- Contributing factors are technical and organizational. "The engineer typed the wrong command" is incomplete without "the production console defaults to the global tenant and has no confirmation."
- Action items have an owner, a priority, and a link to the ticket. "Be more careful" is not an action item. A guardrail is.
- Detection and mitigation delays are explicit. Time to detect and time to mitigate are the numbers worth shrinking.
- Share the postmortem with the teams who felt the dependency, not only the team that owned the bug.
- A review meeting walks the actions. The document is not the end.

## What to include

| Section | Question it answers |
|---|---|
| Summary | What broke, in three sentences, for a reader who was not there |
| Impact | Who felt it and what the SLO did |
| Timeline | What happened in order |
| Trigger | The change or fault that started it |
| Detection | How we noticed, and how we could have noticed sooner |
| Response | What we did, including dead ends |
| Contributing factors | Why the trigger became user impact |
| What worked | Controls that limited the blast radius, so you do not remove them |
| Actions | System changes with owners |

## Anti-patterns

- Naming a culprit in the title.
- A private document that never reaches the team that will hit the same dependency.
- Twenty actions, none scheduled. Prefer a few that remove the class of failure.
- Action items that are "add more monitoring" with no signal, threshold, or page route.
- Skipping the postmortem because the rollback was fast. Near misses are how the next SEV-1 is cheap to prevent.
