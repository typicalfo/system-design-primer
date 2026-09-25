---
title: "Testing strategy"
summary: "Keep a portfolio of fast tests, a thin end-to-end slice, and load tests whose pass line is the SLO, including the queueing an open workload exposes."
tags: [delivery, testing, performance, quality]
when_to_use: "Use when you are deciding which tests to keep, how production is allowed to be a test stage, and what a performance run must show before a launch."
related:
  - cicd.md
  - progressive-delivery.md
  - production-readiness.md
  - ../apis/contract-testing.md
  - ../observability/slos.md
  - ../reliability/chaos.md
last_reviewed: 2026-09-25
---

# Testing strategy

Tests answer different questions. A unit test checks one function. An integration test checks a service against a real dependency you own (a database, a queue). A contract test checks the slice two deployables agreed on. An end-to-end test clicks through a deployed stack. A load test asks whether the SLO holds at a stated arrival rate. None of them replaces the others. The expensive ones should be few, because a suite nobody can run will be skipped.

## Decide

| Layer | Use when | Avoid when |
|---|---|---|
| Unit | The bug is in logic you can call without a network, and you want a failure in seconds | The bug is "the SQL is wrong" or "the other service changed a field." A unit test with five mocks will stay green |
| Integration | You own both sides of a database, a queue, or a local adapter, and the test can start from a known dataset | The dependency is a third party you should not call from every commit. Fake that edge, and contract-test your client |
| Contract | Two teams deploy on different days. See [contract testing](../apis/contract-testing.md) | There is one binary. An integration test is simpler |
| End-to-end, kept thin | A few user journeys must prove the wiring: login, the main write, the main read | You are encoding every business rule in a browser. Those rules belong lower, where the failure points at a line |
| Production canaries and synthetics | You need to see the real path after a small slice of traffic, or to notice a dependency dying when no user is clicking | The change is unsafe at any percentage. Test it before, or do not ship it. See [progressive delivery](progressive-delivery.md) |
| Load, stress, soak, spike | A tier-1 launch or a capacity change needs a pass line. See [production readiness](production-readiness.md) | You have no SLO and no representative data. The chart will not tell you anything you can act on |

## Defaults

- The pipeline runs unit, integration, and contract tests on the artifact you will deploy. See [CI and CD](cicd.md). End-to-end runs on that same digest, in a small set, and a red result blocks the promotion.
- Test data is generated or scrubbed, reset per run, and free of production personal data. A shared mutable database that only passes when yesterday's rows are still there is not a test. Seed the minimum, name the tenant, and delete it.
- Production testing means a canary with an automatic halt, and synthetic probes that run the critical journey on a schedule. It does not mean testers sharing the production admin password. Chaos tests are a separate, hypothesized drill. See [chaos testing](../reliability/chaos.md).
- Performance vocabulary, kept distinct:
  - **Load.** The arrival rate you expect, held long enough to see steady state.
  - **Stress.** Past that rate, until something saturates, so you know what breaks first.
  - **Soak.** The expected rate for long enough that leaks, queue growth, and cache expiry show up.
  - **Spike.** A short jump in arrivals, then a return, to see whether you shed load and recover.
- Model the work. A closed-loop generator sends the next request only after the previous one returns, often with a fixed number of virtual users. When the system slows, the generator slows with it. Latency then looks better than users experienced, because the requests that would have been waiting were never sent. That gap is coordinated omission. An open model schedules arrivals on a clock (so many per second) whether or not the last response came back, and records the time from scheduled send to response, including queueing. Use an open model when the SLO is about user-visible latency at a rate. Use a closed model only when that is actually how clients behave (a fixed pool that waits), and say so.
- The environment is sized like production, or the report lists the differences (smaller database, no cross-zone hop, caches warm). A pass on a laptop does not satisfy a tier-1 gate.
- Pass and fail are the SLOs: error rate, latency at a stated percentile, and saturation, at a stated arrival rate, for a stated duration. "It felt fine" is not a result. See [SLOs](../observability/slos.md).
- Flaky tests are a defect. Quarantine with an owner and a date, and do not let a retry loop turn red into green as the permanent policy. A required check that is red half the time will be bypassed. Fix the test or delete it.

## Pyramid and trophy

One common picture is a pyramid: many unit tests, fewer integration tests, very few end-to-end tests. Martin Fowler's [practical test pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) is a clear statement of that shape. Another picture, often called a trophy, puts the wide band on integration tests, on the argument that many defects sit at the boundary between components, and still keeps the end-to-end tip small. Both pictures agree that a large end-to-end suite is the slow, brittle place. Pick the mix from where your defects actually were last quarter, not from a diagram. If integration tests catch the regressions and unit tests do not, move effort. If the suite takes an hour because every rule is a browser test, move the rules down.

## Checklist

- [ ] A new engineer can run the fast suite without a shared password.
- [ ] Contract tests cover the consumers you can break independently.
- [ ] End-to-end covers a handful of journeys, and each one has an owner.
- [ ] The latest load report states open or closed, the rate, the duration, the environment gaps, and the SLO line it had to beat.
- [ ] Soak has been run for at least as long as your cache and token lifetimes if those lifetimes cause a stampede. Write the duration next to the result.
- [ ] The flaky list is short, named, and dated.

## Anti-patterns

- A green suite that mocks the database and the queue and the clock, and still calls itself integration.
- End-to-end tests that assert copy on the marketing homepage.
- Load tests that drop the slow requests from the histogram and then meet the SLO.
- Retrying every failed test three times in CI and reporting the pass rate as quality.
- Production "testing" that is a manual script against customer tenants.

## Related

- [Contract testing](../apis/contract-testing.md)
- [Progressive delivery](progressive-delivery.md)
- [Production readiness](production-readiness.md)

## Further reading

- [The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) (Martin Fowler)
- [SLOs](../observability/slos.md)
