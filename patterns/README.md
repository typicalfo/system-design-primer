---
title: "Pattern cards"
summary: "One card per pattern with the problem, when to use it, when not to, tradeoffs, and failure modes."
tags: [patterns, index]
when_to_use: "Use when you already know the pattern name and need the operational decision, or when you are choosing among a small set of options."
related:
  - ../enterprise/README.md
  - ../templates/README.md
  - ../pack/skills/system-architect/reference/scalability.md
  - ../README.md
last_reviewed: 2026-09-25
---

# Pattern cards

Each card has the same sections: Problem, When to use, When not to use, Tradeoffs, Failure modes, Implementation notes, Related patterns. Cards that restate a Primer topic link to that section of [README.md](../README.md). The Primer text is untouched.

Guides with the surrounding enterprise context live under [enterprise/](../enterprise/README.md).

## Primer patterns

| Card | Primer section |
|---|---|
| [Cache-aside](cache-aside.md) | [Cache-aside](../README.md#cache-aside) |
| [Write-through](write-through.md) | [Write-through](../README.md#write-through) |
| [Write-behind](write-behind.md) | [Write-behind](../README.md#write-behind-write-back) |
| [Refresh-ahead](refresh-ahead.md) | [Refresh-ahead](../README.md#refresh-ahead) |
| [Cache invalidation](cache-invalidation.md) | [When to update the cache](../README.md#when-to-update-the-cache) |
| [Sharding](sharding.md) | [Sharding](../README.md#sharding) |
| [Leader-follower replication](replication-leader-follower.md) | [Master-slave replication](../README.md#master-slave-replication) |
| [Multi-leader replication](replication-multi-leader.md) | [Master-master replication](../README.md#master-master-replication) |
| [Federation](federation.md) | [Federation](../README.md#federation) |
| [Denormalization](denormalization.md) | [Denormalization](../README.md#denormalization) |
| [Message queues](message-queues.md) | [Message queues](../README.md#message-queues) |
| [CDN](cdn.md) | [Content delivery network](../README.md#content-delivery-network) |
| [Load balancing](load-balancing.md) | [Load balancer](../README.md#load-balancer) |
| [Reverse proxy](reverse-proxy.md) | [Reverse proxy](../README.md#reverse-proxy-web-server) |
| [Consistency patterns](consistency-patterns.md) | [Consistency patterns](../README.md#consistency-patterns) |
| [Availability and failover](availability-failover.md) | [Availability patterns](../README.md#availability-patterns) |

## Enterprise patterns

| Card | Read with |
|---|---|
| [Circuit breaker](circuit-breaker.md) | [Circuit breakers and bulkheads](../enterprise/reliability/circuit-breaker-bulkhead.md) |
| [Retry with backoff](retry-with-backoff.md) | [Retries and timeouts](../enterprise/reliability/retries-timeouts.md) |
| [Bulkhead](bulkhead.md) | [Circuit breakers and bulkheads](../enterprise/reliability/circuit-breaker-bulkhead.md) |
| [Load shedding](load-shedding.md) | [Load shedding](../enterprise/reliability/load-shedding.md) |
| [Rate limiting](rate-limiting.md) | [Rate limiting](../enterprise/apis/rate-limiting.md) |
| [Idempotency keys](idempotency-keys.md) | [Idempotency](../enterprise/data/idempotency.md) |
| [Transactional outbox](transactional-outbox.md) | [Transactional outbox](../enterprise/data/transactional-outbox.md) |
| [Change data capture](cdc.md) | [CDC](../enterprise/data/cdc.md) |
| [Saga](saga.md) | [Sagas](../enterprise/data/sagas.md) |
| [CQRS](cqrs.md) | [Event-driven architecture](../enterprise/data/event-driven.md) |
| [Event sourcing](event-sourcing.md) | [Audit logs](../enterprise/compliance/audit-logs.md) |
| [Strangler fig](strangler-fig.md) | [Strangler fig guide](../enterprise/modernization/strangler-fig.md) |
| [Anti-corruption layer](anti-corruption-layer.md) | [Anti-corruption layer guide](../enterprise/modernization/anti-corruption-layer.md) |
| [API gateway](api-gateway.md) | [API gateways](../enterprise/apis/gateways.md) |
| [Backend for frontend](backend-for-frontend.md) | [API styles](../enterprise/apis/styles.md) |
| [Sidecar and service mesh](sidecar-service-mesh.md) | [Service-to-service auth](../enterprise/identity/service-to-service.md) |
| [Feature flags](feature-flags.md) | [Feature flags guide](../enterprise/delivery/feature-flags.md) |
| [Blue/green](blue-green.md) | [Progressive delivery](../enterprise/delivery/progressive-delivery.md) |
| [Canary](canary.md) | [Progressive delivery](../enterprise/delivery/progressive-delivery.md) |
