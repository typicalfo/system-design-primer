---
title: "Postmortem template"
summary: "A blameless incident write-up with a timeline, impact, contributing factors, and owned actions."
tags: [templates, postmortem, incident]
when_to_use: "Use within a few days of a severe incident or a near miss that would have been one."
related:
  - runbook.md
  - slo.md
  - ../enterprise/observability/postmortems.md
  - ../enterprise/observability/incidents.md
---

# Postmortem: <incident title>

*The title names the user-visible failure, not a person.*

| Field | Value |
|---|---|
| Date | |
| Severity | |
| Incident lead | |
| Status | Draft or final |
| Owners of actions | |

## Summary

*Three sentences. What broke, who felt it, what restored service.*

## Impact

| Question | Answer |
|---|---|
| Who was affected | |
| Duration | Detected at, mitigated at, ended at. UTC |
| Data | Delayed, wrong, or lost. Which store |
| SLO / error budget | |

## Timeline

*UTC. Separate what responders knew then from what we learned later.*

| Time | Event | Source |
|---|---|---|
| | | |

## Trigger

*The change or fault that started this incident.*

## Detection

*How we noticed, and the gap before the first page.*

## Response

*What we did, including the steps that did not help.*

## Contributing factors

*Why the trigger became user impact. Include missing guardrails, not a person's character.*

## What worked

*Controls that limited the blast radius.*

## Actions

| Action | Owner | Priority | Ticket |
|---|---|---|---|
| | | | |

*An action changes a system, a test, an alert, or a staffing rule. "Be more careful" is not an action.*
