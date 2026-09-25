# Design method

Adapted from the System Design Primer. Attribution: [pack README](../../../README.md#attribution).

The Primer teaches an interview conversation in four steps. Use the same order for a written enterprise design. The output of each step is a section, not a speech.

## 1. Use cases, constraints, assumptions

The Primer starts by pinning who uses the system, how, how many of them, what goes in and out, how much data, how many requests per second, and the read/write ratio.

Write:

- **Functional requirements.** Each one is a behavior a caller can observe: "a tenant admin can export their events for a closed time range." Include the failure behavior the caller sees (what a retry returns, what a duplicate write returns).
- **Non-functional requirements.** Latency, throughput, durability, availability, consistency, isolation between tenants, retention, and who is allowed to call. State a target, a unit, and the condition ("p99 under 300 ms for a point read in the home region").
- **Assumptions.** Users, rate, payload size, retention, regions, and peak multiplier. Label each as given or assumed.

Out of scope belongs here too, so later sections do not grow a second product.

## 2. High-level design

Sketch the boxes and the links. Justify each box with a requirement from step 1. A box with no requirement is cut.

The component sketch is a mermaid flowchart. Group it by trust boundary (public caller, your services, data stores) so single points of failure are visible.

## 3. Core components

For the boxes on the critical path, specify:

- The data model: entities, keys, what is immutable, and which store holds the source of truth.
- The API: resource or action, caller, idempotency, and the error a caller retries.
- How that component is looked up, written, and scaled. Use the patterns in [scalability.md](scalability.md) and [data.md](data.md). Pick one and record the rejected alternative in Tradeoffs.

The Primer's running example is a URL shortener: hash the URL, store it, resolve it, decide SQL or NoSQL, then define the API. Do the same depth for the two or three components that dominate cost or correctness. Leave the others as boxes.

## 4. Scale the design

Given the estimates, name the bottleneck: CPU, connections, disk, lock contention, hot key, or cross-region latency. Address it with a pattern from the references (load balancing, horizontal scale, cache, partition, async queue, CDN) only when the estimate shows the bottleneck is real.

Then write **Tradeoffs**. Every scaling choice costs something the Primer is explicit about: extra hardware, complexity, stale reads, or lost writes on failover. State that cost.

## Sections to emit

Use these headings, in order:

1. Functional requirements
2. Non-functional requirements
3. Estimates
4. Component sketch
5. Data model
6. API
7. Tradeoffs

Estimates use [estimates.md](estimates.md). Do not add a section the request does not need, and do not drop Estimates or Tradeoffs.

The same headings are the [design doc template](../../../../templates/design-doc.md). Enterprise constraints (identity, tenancy, retention, residency) are requirements when the request has them. The index is [enterprise/README.md](../../../../enterprise/README.md). Pattern names in component notes should match a card in [patterns/](../../../../patterns/README.md). If a Primer note is marked dated in [scalability.md](scalability.md) or [data.md](data.md), the short list is [what's dated](../../../../enterprise/whats-dated.md).
