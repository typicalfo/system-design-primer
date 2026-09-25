---
title: "Infrastructure as code and environments"
summary: "Describe infrastructure in reviewed code, and keep environments separated without copying production personal data downhill."
tags: [delivery, iac, environments]
when_to_use: "Use when a cloud resource, network rule, or environment difference can exist and you need it to be reviewable and repeatable."
related:
  - cicd.md
  - database-migrations.md
  - ../identity/secrets.md
  - ../security/supply-chain.md
  - ../compliance/privacy.md
last_reviewed: 2026-09-25
---

# Infrastructure as code and environments

If production's shape lives in a console, it lives in someone's memory. Infrastructure as code (IaC) puts the desired state in reviewable text and applies it through a pipeline. Drift is the difference between that text and what is actually running.

## Defaults

- One tool the team will actually run (Terraform, Pulumi, CloudFormation, or the platform's equivalent). The requirement is plan, review, apply, not the brand.
- Plan output is reviewed before apply to production. The identity that can apply is not every developer.
- State is locked and stored remotely. Two applies at once corrupt state.
- Changes are small. A pull request that rebuilds the network and upgrades the database is two incidents waiting.
- Environments differ by scale and by data, not by architecture. If staging cannot represent the failure mode, it will not catch it.
- Minimum set: production, a pre-production that matches topology closely enough to rehearse deploys, and ephemeral environments for pull requests if they stay cheap. A long chain of dev, QA, UAT, staging, and preprod usually means nobody knows which one is real.
- Production data does not flow into lower environments unless it is synthetic or transformed under a written rule. See [privacy](../compliance/privacy.md).
- Secrets are not in the IaC source. The code names the secret; the manager holds the value.
- Drift detection runs on a schedule. Either reconcile to the code or accept a console change by coding it. Do not leave both.
- Destroy is a protected command. A typo in a name should not delete the production database. Separate state for production.

## Decide

| Environment | Data | Purpose |
|---|---|---|
| Local / ephemeral | Synthetic | Developer feedback |
| Shared staging | Synthetic, production-shaped volume if you can afford a slice | Rehearse deploy, migration, and failure |
| Production | Real | Customers |

## Anti-patterns

- Click-ops in production "just this once," with no follow-up commit.
- One IaC state for every environment, so a staging apply can touch production.
- Staging that is a single tiny VM while production is multi-zone, used to justify a region failover you have never seen.
- Importing a live account into IaC and then applying a plan you did not read.
- Shared admin credentials across environments because the pipeline was annoying to split.
