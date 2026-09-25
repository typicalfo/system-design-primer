---
title: "Sidecar and service mesh"
summary: "Run a helper process beside each instance to do mTLS, retries, and telemetry, or adopt a mesh when many services need those uniformly."
tags: [platform, security, reliability]
when_to_use: "Use when many services need the same transport security and traffic policy and you will actually operate the mesh."
related:
  - api-gateway.md
  - circuit-breaker.md
  - retry-with-backoff.md
  - ../enterprise/identity/service-to-service.md
---

# Sidecar and service mesh

## Problem

Each service reimplementing TLS, retries, and metrics drifts. A sidecar (or a node agent) moves that machinery out of the business process. A mesh is the control plane that configures those proxies.

## When to use

- You have enough services that per-service TLS and traffic policy is already a problem.
- You need workload identity between services.
- The team running the cluster can own the mesh's failure modes.

## When not to use

- You have a handful of services and a gateway. A mesh is a new production system.
- The mesh is installed in permissive mode and will stay there.
- Business authorization is expected to live in proxy config. It will be invisible and wrong.

## Tradeoffs

| You gain | You pay |
|---|---|
| Uniform mTLS and traffic metrics | Latency, RAM, and a control plane |
| Policy without rewriting every service | Upgrades that can black-hole traffic |
| Identity for workloads | Debugging two processes per pod |

## Failure modes

- Permissive mode means unauthenticated traffic still works, so the security control is fictional.
- Retries in the sidecar plus retries in the app multiply.
- The sidecar's resource limit kills traffic under load.
- Configuration applies to the wrong namespace.

## Implementation notes

- Start with identity and mTLS, not every feature.
- Disable app-level retries if the sidecar retries, or the reverse. One layer.
- Treat mesh config as code.
- Guide: [service-to-service auth](../enterprise/identity/service-to-service.md).

## Related patterns

- [API gateway](api-gateway.md)
- [Circuit breaker](circuit-breaker.md)
- [Retry with backoff](retry-with-backoff.md)
