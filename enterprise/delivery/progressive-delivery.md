---
title: "Progressive delivery"
summary: "Expose a release to a small slice first, watch the SLO, and expand or roll back on that evidence."
tags: [delivery, canary, blue-green, rollout]
when_to_use: "Use when a production deploy can hurt users and you can shift traffic in steps."
related:
  - feature-flags.md
  - cicd.md
  - database-migrations.md
  - ../observability/slos.md
  - ../../patterns/canary.md
  - ../../patterns/blue-green.md
last_reviewed: 2026-09-25
---

# Progressive delivery

Progressive delivery means not everyone gets the new version at once. The two common mechanisms are a [canary](../../patterns/canary.md) (a small percentage of traffic on the new version) and [blue/green](../../patterns/blue-green.md) (two full environments, one live). Feature flags slice by identity instead of by process. Use the one that matches the risk.

## Decide

| Mechanism | Use when | Avoid when |
|---|---|---|
| Canary | Stateless services behind a load balancer, and you have a metric that will move if the version is bad | One tenant's traffic is sticky in a way your slice cannot see, or the bug is data corruption too rare for a five-minute canary |
| Blue/green | You can afford two full stacks and you want an immediate cutback | The database migration is incompatible with the old binary. Switching the app back will not undo the schema |
| Flag by tenant | A specific customer should go first, or you need an instant off switch without a redeploy | The risky code runs in a migration or a worker the flag does not wrap |
| Big bang | The change is tiny, reversible, and well tested, or the system is single-instance and you accept the window | The last three incidents were bad deploys |

## Defaults

- Automatic rollback criteria are written before the rollout: error rate, latency, or a business SLO, compared to the baseline, with a minimum sample.
- Canary long enough to see real traffic, short enough that you do not leave two versions overnight without an owner.
- Sessions that must stay on one version (a multi-step wizard) pin to the version they started on, or the steps are compatible across versions.
- Workers and cron jobs get a rollout story too. Canary only the web tier and you will miss the bad migration job.
- The previous digest stays deployed and routable until the bake finishes.
- A database change in the same release follows expand/contract so both versions run. See [database migrations](database-migrations.md).
- Chat or the deploy record says who is rolling out what, so the on-call does not debug a canary as a mystery partial outage.

## Anti-patterns

- A canary of 50% called progressive. That is half the users.
- Watching CPU and not the user SLO.
- Rolling forward automatically when the canary is red because the pipeline's next stage is unconditional.
- Two versions writing incompatible rows with no feature detection.
