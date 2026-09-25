---
title: "Logs, metrics, and traces"
summary: "Use metrics for symptoms and alerts, traces for one request's path, and logs for the detail you cannot aggregate."
tags: [observability, logs, metrics, traces]
when_to_use: "Use when you are deciding what a service should emit so an on-call engineer can tell whether a user request succeeded."
related:
  - opentelemetry.md
  - slos.md
  - alerting-oncall.md
  - ../compliance/audit-logs.md
  - ../../templates/runbook.md
---

# Logs, metrics, and traces

Three signals answer different questions. Metrics say how the system is doing. Traces say where one request spent time and which hop failed. Logs say what happened at a line you chose to record. Audit logs are a fourth stream with stricter integrity. See [audit logs](../compliance/audit-logs.md).

The Google SRE books discuss monitoring and are CC BY-NC-ND 4.0, so this page links them and does not copy them: <https://sre.google/books/>. License notes are in [pack/corpora/INDEX.md](../../pack/corpora/INDEX.md).

## Decide

| Signal | Use when | Avoid when |
|---|---|---|
| Metric (counter, gauge, histogram) | You will alert, dashboard, or budget a rate, error ratio, or latency | The label set includes user id, tenant id unbounded, or a raw URL. Cardinality will take the pipeline down |
| Trace span | A request crosses processes and you need the path after a failure | You trace every field of a payload. Use attributes sparingly and scrub them |
| Structured log | A human or a later query needs a specific id (request id, batch id) and a stable event name | You print unstructured paragraphs, or you log secrets and personal data |
| Audit log | The action is privileged or security-relevant | The event is a health check or a debug trace |

## Defaults

- RED for services: rate, errors, duration, per operation. USE for resources: utilization, saturation, errors (CPU, pool, queue, disk).
- One correlation id (trace id or request id) from the edge to the database call and the async job. Logs include it.
- Structured logs: JSON with `time`, `severity`, `service`, `trace_id`, `msg`, and a few stable fields. Levels mean something. `ERROR` is paged or ticketed, not a stack trace you ignore.
- Histograms have explicit buckets that cover the SLO threshold, so you can measure "faster than 300 ms" without guessing.
- Sampling of traces is head-based or tail-based at the collector, not an accident of one SDK default. Errors are kept.
- Scrub tokens, cookies, passwords, and personal payloads before export. Scrubbing in the vendor UI is too late if the vendor already stored them.
- Clocks are UTC. Units are named (`latency_ms`, not `latency`).

## Checklist

- [ ] For a failed user write, you can find the trace or the log line from the request id you returned to the caller.
- [ ] Dashboards show saturation (queue depth, pool wait, replication lag), not only CPU.
- [ ] A tenant id is available on the request log where you need to debug one customer, and is not a label on every metric.
- [ ] Health checks are not counted as user traffic in the SLO.
- [ ] Log volume has a cap or a sampling rule so a loop cannot exhaust the bill or the disk.

## Anti-patterns

- A log line that says "failed" with no id, no operation, and no error class.
- Averaging latency. Use a histogram and read a percentile.
- A separate request id in the gateway, the app, and the worker, with no join.
- Shipping debug logs and audit logs through one pipeline that drops under backpressure.
