---
title: "Software delivery metrics"
summary: "Measure DORA's five software delivery metrics from deploys and incidents, and pair them with SLOs so speed is not the only score."
tags: [organization, dora, delivery, metrics]
when_to_use: "Use when a team wants a small set of delivery measures and needs the current DORA names, the collection rules, and the ways the numbers get gamed."
related:
  - ownership.md
  - ../delivery/cicd.md
  - ../delivery/testing-strategy.md
  - ../observability/slos.md
  - ../observability/incidents.md
last_reviewed: 2026-09-25
---

# Software delivery metrics

DORA's current software delivery model has five metrics in two groups. The names below follow the [DORA metrics guide](https://dora.dev/guides/dora-metrics/) and the [history of those metrics](https://dora.dev/insights/dora-metrics-history). This page paraphrases them. It does not copy the reports.

Attribution: DORA research program, <https://dora.dev/>, used under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Throughput:

- **Change lead time.** Time from a change committed to version control until that change is running in production.
- **Deployment frequency.** How often you deploy, or the time between deployments.
- **Failed deployment recovery time.** Time to recover from a deployment that fails and needs immediate intervention, such as a rollback or a hotfix. This replaced the older "time to restore service" (sometimes called MTTR). The older measure mixed failures caused by a change with failures caused by something else, such as a data-center outage. The current measure is about the failed deployment.

Instability:

- **Change fail rate.** The share of deployments that need immediate intervention after they go out (rollback, hotfix, or an equivalent fix-forward).
- **Deployment rework rate.** The share of deployments that were not planned and that exist because of an incident in production. DORA added this fifth metric in 2024 so that a bug fixed the next day is visible even when it never triggered an instant rollback. The history page groups change fail rate and deployment rework rate as instability, and the three throughput metrics above as throughput.

Older write-ups say "lead time for changes," "change failure rate," and "time to restore service." Use the current names in new dashboards, and label the old name once if a chart still has it.

## Decide

| Choose | Use when | Avoid when |
|---|---|---|
| All five, per application | You deploy the application as a unit and you can tie a restore to a deploy | You only have a survey answer and no deploy record. A survey is how DORA studies the industry. It is a weak primary source for your own team |
| Change lead time and deployment frequency first | You are instrumenting from zero and the pipeline already records deploys | Leadership will rank teams on those two and ignore failures |
| Failed deployment recovery time, not generic MTTR | You want the speed of repairing a bad release | You also need incident duration for outages that were not a release. Keep that as an incident metric. See [incidents](../observability/incidents.md) |
| Rework rate next to change fail rate | Hotfixes land outside the "immediate" window and disappear from the fail rate | You cannot tell a planned deploy from an unplanned one. Fix the reason field before you trust the ratio |

## How to measure

Define the application first. A repo that is a library is not a deployment. A product made of four services needs a rule for what counts as one deploy of that product. Write the rule down.

- **Deployment frequency.** Count successful production deployments in a window. Source: the deploy log (digest, time, application), not the merge button. See [CI and CD](../delivery/cicd.md).
- **Change lead time.** For each deploy, the time from the commit DORA describes (code committed) to production. If several commits ship together, decide whether you report the oldest commit in the deploy or the median commit, and keep that choice. Do not start the clock at "ticket created" and still call it change lead time.
- **Change fail rate.** Numerator: deployments that were followed by an immediate remediation you have defined (rollback to a previous digest, or a hotfix deploy tagged to the same change). Denominator: deployments. Pick the time window (for example, remediation started within one hour) and publish it. A silent window change moves the rate.
- **Failed deployment recovery time.** From the start of customer impact, or from the decision to remediate, to the deploy that restores the previous good behavior. Say which start you use. "Ticket closed" is not the end.
- **Deployment rework rate.** Numerator: deployments marked unplanned and caused by a user-facing production bug. Denominator: deployments. The mark has to be set by the person shipping the fix, in the pipeline, not inferred a quarter later.

Pair the five with the SLO for that application. A team that deploys hourly and burns the error budget is not a high performer in any sense a customer can feel. See [SLOs](../observability/slos.md). Review wait, flaky tests, and deploy pain belong next to the five as well. See [testing strategy](../delivery/testing-strategy.md). One team owns the application these numbers describe. See [service ownership](ownership.md).

## Checklist

- [ ] Each metric has a source system and a definition of "application."
- [ ] Rollbacks are deploys in the same log, so they cannot vanish from the fail rate.
- [ ] The remediation window for "immediate" is written next to the change fail rate.
- [ ] Rework is a field on the deploy, not a guess from the commit message.
- [ ] The dashboard shows the SLO next to throughput.
- [ ] You do not publish a team ranking from these five alone.

## Anti-patterns

- Goodhart's law in practice: the metric becomes the target, so people split one change into many deploys, or hide a rollback as a "forward fix" with no tag.
- Comparing a mobile app's release train with a web service's daily deploy, then calling one team low.
- Counting failed CI builds as change failures. Those builds never reached a user.
- Using mean recovery time when a single multi-day incident dominates. Report the median and the bad tail.
- A program that rewards deployment frequency and never asks whether the deploys were rework.

## Related

- [CI and CD](../delivery/cicd.md)
- [SLOs](../observability/slos.md)
- [Incidents](../observability/incidents.md)

## Further reading

- [DORA's software delivery performance metrics](https://dora.dev/guides/dora-metrics/)
- [A history of DORA's software delivery metrics](https://dora.dev/insights/dora-metrics-history)
- [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
