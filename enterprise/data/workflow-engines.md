---
title: "Workflow engines"
summary: "Choose durable execution, an orchestrated saga, choreography, a job queue, or cron from how long the process lives and who must remember the step."
tags: [data, workflow, orchestration, sagas]
when_to_use: "Use when a business process outlives one request and you are deciding whether a durable engine, a saga, a queue, or a clock should hold the state."
related:
  - sagas.md
  - idempotency.md
  - event-driven.md
  - transactional-outbox.md
  - ../reliability/retries-timeouts.md
  - ../apis/errors-pagination-async.md
  - ../../patterns/saga.md
  - ../../patterns/message-queues.md
  - ../../patterns/idempotency-keys.md
last_reviewed: 2026-09-25
---

# Workflow engines

Some work is one message and a handler. Some work is "wait three days, then charge, and if a person clicks cancel, stop." The second kind needs a store that remembers the step after every process restart. A workflow engine is that store plus a replay or a state machine. A saga is the business shape of the steps and their compensations. The engine is one way to run the saga. The saga page is [sagas](sagas.md).

## Decide

| Approach | Use when | Avoid when |
|---|---|---|
| Durable execution | The process waits on timers, people, or many steps, and the code should be the definition that survives worker crashes | The job is one handler. You would operate an engine to wrap a queue |
| Orchestrated saga | Several services must commit local work, and one component must answer "where is this order?" | The orchestrator starts owning other teams' private rules. Keep it to sequence, timers, and compensations |
| Choreography on a log or queue | Few steps, and each service already reacts to facts | Nobody can name the current step without reading every repository |
| Job queue | One unit of work, retries, a dead letter | The next step is "sleep until Tuesday" or a compensation graph |
| Cron | A time tick starts work that is safe to skip or to overlap under a lock | The cron scans a table of half-finished jobs. That table is an engine |

## Defaults

Durable execution, in the Temporal shape, works like this.

- The workflow function is ordinary code. What the platform stores is the event history of that run: commands the code issued and the results that came back.
- After a crash or a deploy, a worker replays the code against that history. Results already in the history are reused. The code must take the same path, or the replay does not match the history.
- Anything that can change between replays stays out of the workflow function: network calls, random numbers, the wall clock, and reading your own database. Those run as activities. Activities have their own retry policy and timeouts. A heartbeat can checkpoint a long activity. The next attempt starts from the start of the activity unless the heartbeat payload tells it otherwise.
- A signal is an asynchronous message into a running workflow. A query reads state. An update is a tracked write that can return a result. Timers are recorded in the history, so "sleep for 30 days" does not pin a thread and still fires if workers were down at the deadline.
- The HTTP API that starts this work is usually [asynchronous](../apis/errors-pagination-async.md): accept the request, return a status resource, and let the engine run.

Other engines in the same family, stated only as their own docs describe them:

- [Temporal](https://docs.temporal.io/evaluate/understanding-temporal) is a durable-execution platform. The [Temporal server repository](https://github.com/temporalio/temporal) describes it as a fork of Uber's Cadence, by Cadence's creators. Workflows replay from [event history](https://docs.temporal.io/workflow-execution/event). [Activities](https://docs.temporal.io/activities) are the non-deterministic steps and should be idempotent. [Signals, queries, and updates](https://docs.temporal.io/encyclopedia/workflow-message-passing/) are the message types. [Timers](https://docs.temporal.io/workflow-execution/timers-delays) are persisted.
- [Cadence](https://cadenceworkflow.io/) is a CNCF durable-execution project. Workflows resume from execution history. Activities retry, and sleep survives worker restarts. The project site lists Go, Java, and Python clients, and persistence with Cassandra, PostgreSQL, MySQL, and OpenSearch.
- [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) is a managed state-machine service. Current docs distinguish Standard workflows (exactly-once execution, up to one year) from Express workflows (at-least-once execution, up to five minutes).
- [Azure Durable Functions](https://learn.microsoft.com/en-us/azure/durable-task/durable-functions/durable-functions-overview) extends Azure Functions with orchestrator, activity, and entity functions. The runtime checkpoints and retries. [Orchestrators must be deterministic because they replay](https://learn.microsoft.com/en-us/azure/durable-task/common/durable-task-code-constraints).
- [Restate](https://docs.restate.dev/) records an invocation journal and replays it. Non-deterministic work is wrapped so the recorded result is what replay sees. Timers and retries are part of that path. See [request lifecycle](https://docs.restate.dev/guides/request-lifecycle).

## Versioning

Replay compares the commands this version of the code emits with the commands already in the history. Adding, removing, or reordering an activity, a timer, a child workflow, or a signal-send on a run that already passed that point breaks the run.

Ship the new sequence so new runs take it and old runs keep the old path. Temporal's versioning docs call the in-code branch patching, and the deployment form worker versioning: an open run stays on the worker revision it started on. A new workflow name is a cutover only for runs that have not started. [Continue-as-new](https://docs.temporal.io/workflow-execution/continue-as-new) closes the current run and starts a fresh history with the state you pass in. Temporal's event page documents hard limits that force that practice: a history that exceeds 51,200 events, 2,000 updates, or 10,000 signals terminates the run. Those caps are the vendor's current numbers. Read the page before you treat them as permanent.

## Idempotent activities

An activity retry runs the function again. "Charge the card" must key the charge so the second attempt finds the first. The workflow's own history dedupes the activity result after a recorded success. It does not dedupe a side effect that happened and then failed to report. Use the same rules as [idempotency](idempotency.md): a natural unique key, or an idempotency key stored with the effect.

## What it costs to run

You pay for history, replay, and a service.

Planning assumptions, not a benchmark: 2,000,000 runs per day, 40 persisted events each, 1,536 bytes stored per event, keep 14 days, three copies on the history store.

```text
Events per day = 2,000,000 * 40 = 80,000,000
Bytes per day  = 80,000,000 * 1,536 = 122,880,000,000
14 days        = 14 * 122,880,000,000 = 1,720,320,000,000 bytes
Three copies   = 3 * 1,720,320,000,000 = 5,160,960,000,000 bytes
               = 5,160,960,000,000 / 1024^4 = 4.694 TiB
```

The TiB figure is that byte count divided by 1024^4, rounded to three decimals.

That is the history payload only. Indexes, visibility search, and worker replay CPU are extra. Replay reads the history and re-executes workflow code until it catches up. Long histories make every recovery slower. Continue-as-new is how you cap that.

Self-hosted Cadence or Temporal means you operate that store, the service in front of it, upgrades, and the workers. [Temporal Cloud](https://docs.temporal.io/cloud) is Temporal's managed service. You still write deterministic workflow code and you still run workers. Step Functions and Durable Functions are managed: you pay their execution model and you still own the determinism and the idempotency of each step. A managed control plane does not make a non-idempotent charge safe.

## Checklist

- [ ] The process has a duration and a "where is it" question that a queue depth does not answer.
- [ ] Workflow code does not read the clock, the network, or a random source except through the engine's APIs.
- [ ] Every activity that writes somewhere else is idempotent.
- [ ] A code change has a story for runs that are already open.
- [ ] History growth has a continue-as-new or equivalent bound.
- [ ] Timeouts exist for activities and for the whole run. A stuck step is visible.

## Anti-patterns

- Hiding a single RPC inside a workflow so the diagram looks serious.
- Logging or calling HTTP directly in workflow code, then debugging replay mismatches in production.
- An activity that charges again on every retry.
- Editing the steps of a year-long run in place.
- Cron plus a status column, with no timeout and no owner, called "lightweight orchestration."
- Building the engine yourself the second time a job needs a sleep. The first time, a delayed message is enough.

## Related

- [Sagas](sagas.md), [idempotency](idempotency.md), [events](event-driven.md), [outbox](transactional-outbox.md)
- [Retries](../reliability/retries-timeouts.md), [async HTTP](../apis/errors-pagination-async.md)
- [Saga](../../patterns/saga.md), [queues](../../patterns/message-queues.md), [idempotency keys](../../patterns/idempotency-keys.md)

## Sources

- [Understanding Temporal](https://docs.temporal.io/evaluate/understanding-temporal)
- [Temporal event history](https://docs.temporal.io/workflow-execution/event), [activities](https://docs.temporal.io/activities), [messages](https://docs.temporal.io/encyclopedia/workflow-message-passing/), [timers](https://docs.temporal.io/workflow-execution/timers-delays), [versioning](https://docs.temporal.io/develop/typescript/versioning), [continue-as-new](https://docs.temporal.io/workflow-execution/continue-as-new)
- [Temporal server repository](https://github.com/temporalio/temporal), [Temporal Cloud](https://docs.temporal.io/cloud)
- [Cadence](https://cadenceworkflow.io/)
- [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
- [Azure Durable Functions overview](https://learn.microsoft.com/en-us/azure/durable-task/durable-functions/durable-functions-overview), [orchestrator constraints](https://learn.microsoft.com/en-us/azure/durable-task/common/durable-task-code-constraints)
- [Restate](https://docs.restate.dev/), [request lifecycle](https://docs.restate.dev/guides/request-lifecycle)
