---
title: "API gateways"
summary: "Put edge concerns at the gateway and keep product policy in the service that owns the data."
tags: [api, gateway, edge]
when_to_use: "Use when many clients enter through one front door and you are deciding what that door is allowed to do."
related:
  - styles.md
  - rate-limiting.md
  - ../identity/oidc-oauth2.md
  - ../identity/authorization-models.md
  - ../../patterns/api-gateway.md
  - ../../patterns/backend-for-frontend.md
---

# API gateways

A gateway terminates TLS, authenticates the caller, enforces coarse limits, and routes to a service. It is not the place for pricing rules, tenant data joins, or a second copy of authorization that drifts from the service.

Pattern card: [API gateway](../../patterns/api-gateway.md). When each client shape needs its own aggregation, add a [backend for frontend](../../patterns/backend-for-frontend.md) behind the gateway rather than growing the gateway into that client.

## Defaults

- The gateway verifies the token signature, issuer, audience, and expiry. The service still authorizes the action on the resource. See [authorization](../identity/authorization-models.md).
- Request size, header size, and time limits are set. Body buffering is bounded so a slow client cannot pin memory.
- Rate limits live here when they are coarse (per token, per IP for anonymous traffic). Expensive-route limits can live here or in the service. One of them must exist. See [rate limiting](rate-limiting.md).
- Routes are configuration reviewed like code. A typo that sends tenant traffic to the wrong service is an incident.
- The gateway generates or forwards a request id and trace context. See [OpenTelemetry](../observability/opentelemetry.md).
- mTLS or workload identity on the hop from gateway to service, so the service does not accept the same call from anywhere in the cluster just because the gateway would have checked. See [service-to-service auth](../identity/service-to-service.md).
- Configuration changes can roll back. The gateway is on the path of every request. Treat it like a production dependency with its own SLO.

## Decide

| Put it on the gateway | Put it in the service |
|---|---|
| TLS, token verification, coarse rate limit, request size, WAF-style blocking of obvious abuse | Whether this user may export this tenant's invoices |
| Path routing to the owning service | Business validation and transactions |
| A BFF's aggregation, if the gateway team does not own that product | The BFF, owned by the client team, if the aggregation changes with the UI |

## Anti-patterns

- A shared gateway team that must edit a route for every product change. You built a bottleneck. Self-service routes with policy checks scale better.
- Authorization only at the gateway, trusting a header the service cannot verify.
- Transformation spaghetti that rewrites bodies differently per customer.
- Bypassing the gateway from the public internet "just for this one webhook" with no equivalent controls.
