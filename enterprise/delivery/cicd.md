---
title: "CI and CD"
summary: "Build an artifact once, test it, sign it, and promote that same digest through environments."
tags: [delivery, cicd, release]
when_to_use: "Use when code must reach production through a path you can explain, reverse, and audit."
related:
  - iac-environments.md
  - progressive-delivery.md
  - ../security/supply-chain.md
  - ../observability/incidents.md
  - ../../patterns/blue-green.md
  - ../../patterns/canary.md
---

# CI and CD

Continuous integration means the main branch stays buildable and tested as changes land. Continuous delivery means that artifact can be released safely. Continuous deployment means it does release on its own. Pick delivery versus deployment explicitly. Both still require the same artifact and a rollback.

Twelve-factor practices that still hold (one codebase, explicit dependencies, config in the environment, separate build and run, logs as streams) are documented at <https://12factor.net/> under the MIT license noted in [pack/corpora/INDEX.md](../../pack/corpora/INDEX.md). This page does not copy that text.

## Defaults

- Every change is a reviewed commit on the trunk or a short-lived branch. Long-lived branches are where integration goes to die.
- CI builds, runs unit and contract tests, scans dependencies, produces an SBOM, and signs the digest. See [supply chain](../security/supply-chain.md).
- The deploy promotes the digest. It does not compile again from a different commit and call it the same version.
- Config that changes per environment is not baked into the image. Secrets come from the secret manager at runtime.
- Required checks gate merge. Flaky tests are fixed or removed. A required check that is red half the time will be bypassed.
- Production deploys are attributable: commit, digest, approver or policy, time. That is change-management evidence. See [SOC 2](../compliance/soc2.md).
- Rollback is a redeploy of the previous digest, a [feature flag](feature-flags.md), or both. If the release included a destructive migration, rollback of the binary is not enough. See [database migrations](database-migrations.md).
- Progressive exposure ([canary](../../patterns/canary.md) or [blue/green](../../patterns/blue-green.md)) is how you limit blast radius when the test suite cannot see production traffic.
- Database and infrastructure changes go through the same review path as application code.

## Checklist

- [ ] You can redeploy last week's digest without rebuilding it.
- [ ] A failed test blocks merge without a human remembering to look.
- [ ] Production and CI use different identities and different secrets.
- [ ] Deploy logs are retained with the audit stream or linked from it.
- [ ] The pipeline itself is defined as code and reviewed.

## Anti-patterns

- SSH and a git pull on the server.
- "Hotfix" branches that skip CI and never merge back.
- Tests that need a shared mutable staging database and fail when run twice.
- A green pipeline that does not include the migration, discovered only at the production step.
