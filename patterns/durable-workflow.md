---
title: "Durable workflow"
summary: "Record each step of a long-running process in an event history and continue by replaying that history, instead of holding the work in memory."
tags: [data, workflow, orchestration]
when_to_use: "Use when a business process outlives one process, needs timers and retries, and must not lose its place when the worker dies."
related:
  - saga.md
  - idempotency-keys.md
  - transactional-outbox.md
  - ../enterprise/data/workflow-engines.md
  - ../enterprise/data/sagas.md
last_reviewed: 2026-09-25
---

# Durable workflow

## Problem

A checkout, an onboarding, or a provisioner takes minutes or days. Timers fire, people approve, and downstream APIs fail. If the only copy of "we are on step 3" is a thread in one process, a deploy or a crash resumes from nowhere or, worse, from the start and repeats a side effect.

## When to use

- The process has several steps, waits, and a status a person will ask about.
- Steps have side effects that must be retried without doubling the effect.
- You can keep the workflow code deterministic on replay: same history, same next decision.
- Operating a workflow engine, or paying for a managed one, is cheaper than inventing this recovery in each service.

## When not to use

- One database transaction covers the work. Use the transaction.
- The flow is a single short request with an idempotency key. A workflow history is overhead. See [idempotency keys](idempotency-keys.md).
- You only need to publish a fact and let consumers react, with no central status. That is choreography. See [saga](saga.md).
- The team will edit in-flight workflow code the way they edit a normal service. Replay will diverge, and the engine will refuse the workflow or, if you disable the check, do the wrong next step.

## Tradeoffs

| You gain | You pay |
|---|---|
| A crash resumes from the recorded history | An engine to run, upgrade, and watch |
| Timers and retries live in the history, not in a forgotten cron | Activities must be idempotent. The engine will run them more than once |
| One place that can answer "where is this order" | Workflow code must stay deterministic. Clocks, random numbers, and new branches break replay |
| Compensation and human waits are ordinary steps | History rows accumulate. You need a retention plan |
| | The engine is now on the path of every long-running process |

## Failure modes

- A new deploy changes a decision for a history that already happened. Replay does not match. The workflow sticks.
- An activity charges a card and then times out before recording success. The retry charges again.
- A signal or a timer is handled in the worker's memory and never appended. After a crash the wait is gone.
- History is unbounded. A workflow that loops for months fills the store and slows every replay.
- Operators "fix" a stuck workflow by editing the history. The next replay is a lie.
- The engine's own store is one region with no restore test. You durable-executed yourself into a single outage.

## Implementation notes

- The history is the source of truth for control flow. The worker may die. Replay reads the history and continues.
- Side effects go in activities, not in the workflow decision. Activities have timeouts and retries. The workflow code itself does not call the network on replay.
- Pass an idempotency key into every activity that can move money, send a message, or create a resource.
- Version the workflow type. Run in-flight executions on the code they started with, or only append steps in a way replay still accepts.
- Compare this with a saga orchestrator you built on a queue, and with choreography, in [workflow engines](../enterprise/data/workflow-engines.md) and [sagas](../enterprise/data/sagas.md). A queue without a history is not this pattern. A cron that scans a status column is not this pattern either, unless the scan is the recovery you have tested.

## Related patterns

- [Saga](saga.md)
- [Idempotency keys](idempotency-keys.md)
- [Transactional outbox](transactional-outbox.md)
