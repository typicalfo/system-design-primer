---
title: "Sidecar and service mesh"
summary: "Run a helper beside each instance, or a node-level proxy plus optional waypoints, when many services need the same mTLS and traffic policy."
tags: [platform, security, reliability]
when_to_use: "Use when many services need the same transport security and traffic policy and you will actually operate the mesh."
related:
  - api-gateway.md
  - circuit-breaker.md
  - retry-with-backoff.md
  - ../enterprise/identity/service-to-service.md
last_reviewed: 2026-09-25
---

# Sidecar and service mesh

## Problem

Each service reimplementing TLS, retries, and metrics drifts. A sidecar (or a node agent) moves that machinery out of the business process. A mesh is the control plane that configures those proxies.

Istio's ambient mode is the sidecarless shape of that idea. It reached general availability in Istio 1.24 (November 2024). A shared ztunnel on each node handles L4 (mTLS, identity, L4 authorization, telemetry). An optional waypoint proxy handles L7 for a namespace or a service, not for every pod. Sidecars remain supported.

## When to use

- You have enough services that per-service TLS and traffic policy is already a problem.
- You need workload identity between services.
- The team running the cluster can own the mesh's failure modes.
- Prefer ambient when the need is mTLS and L4 policy across many pods and you do not want a proxy container on each pod. CPU and memory then follow nodes (ztunnel) and waypoint replicas, not pod count. Joining the mesh is a namespace label. A mesh upgrade of ztunnel does not restart every application pod.
- Add a waypoint only where you need L7: HTTP routing, authorization on method or path or headers, or proxy-level retries. Waypoints scale on their own.
- Keep a sidecar when the pod needs the proxy in its own network namespace, or when you depend on a feature the ambient build you run has not marked ready. Sidecar and ambient pods can share one mesh while you move a namespace at a time.

## When not to use

- You have a handful of services and a gateway. A mesh is a new production system.
- The mesh is installed in permissive mode and will stay there.
- Business authorization is expected to live in proxy config. It will be invisible and wrong.
- You point L7 rules at ztunnel. The node proxy is L4. An L7 policy enforced there fails closed (it becomes a deny). Put L7 rules on a waypoint.
- You assume a sidecar caller's L7 policy and an ambient waypoint's L7 policy both apply. During a move, traffic from a sidecar pod to an ambient destination can skip the waypoint, so the waypoint policy is not on that path until the caller moves too.

## Tradeoffs

| You gain | You pay |
|---|---|
| Uniform mTLS and traffic metrics | Latency, RAM, and a control plane |
| Policy without rewriting every service | Upgrades that can black-hole traffic |
| Identity for workloads | Debugging two processes per pod |
| No per-pod proxy on the L4 path | A shared ztunnel: a bad node proxy affects every pod on that node. A waypoint upgrade still does not restart the app |

## Failure modes

- Permissive mode means unauthenticated traffic still works, so the security control is fictional.
- Retries in the sidecar plus retries in the app multiply. The same split applies if both the app and a waypoint retry.
- The sidecar's resource limit kills traffic under load. A waypoint that is too small does the same for every pod that routes through it.
- Configuration applies to the wrong namespace.
- ztunnel is down on a node, so mesh traffic for pods on that node stops even though the pods are up.
- A waypoint is missing or has no address, and L7 policy is silently skipped while L4 still flows. Require waypoint traversal with an L4 allow for the waypoint's identity when L7 is the control you meant.

## Implementation notes

- Start with identity and mTLS, not every feature. On Istio ambient that is ztunnel first, then a waypoint where L7 is required.
- Ambient was marked GA in Istio 1.24 on 7 November 2024: ztunnel, waypoints, and the ambient APIs were called stable. Individual L7 features still move on their own. On the current L7 table, HTTP routing via HTTPRoute and L7 authorization are Beta, and TLSRoute and TCPRoute are Alpha. VirtualService support in ambient is Alpha. Read the feature table for the version you run before you depend on one of those. Sidecars stay fully supported, including where ambient's L7 gap matters.
- Disable app-level retries if the sidecar or the waypoint retries, or the reverse. One layer.
- Treat mesh config as code.
- Istio: [ambient mode GA in 1.24](https://istio.io/latest/blog/2024/ambient-reaches-ga/), [data-plane modes](https://istio.io/latest/docs/overview/dataplane-modes/), [ambient overview](https://istio.io/latest/docs/ambient/overview/), [L7 features](https://istio.io/latest/docs/ambient/usage/l7-features/).
- Guide: [service-to-service auth](../enterprise/identity/service-to-service.md).

## Related patterns

- [API gateway](api-gateway.md)
- [Circuit breaker](circuit-breaker.md)
- [Retry with backoff](retry-with-backoff.md)
