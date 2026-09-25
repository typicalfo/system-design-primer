---
title: "API gateway"
summary: "A single edge that authenticates, limits, and routes requests, without owning product decisions."
tags: [api, edge]
when_to_use: "Use when many clients share a front door and you want TLS, authentication, and routing in one place."
related:
  - backend-for-frontend.md
  - rate-limiting.md
  - reverse-proxy.md
  - ../enterprise/apis/gateways.md
---

# API gateway

## Problem

Every service should not each invent TLS, token checks, and client-facing routing. A gateway centralizes the edge. It becomes a liability when it also centralizes product logic.

## When to use

- Multiple services sit behind one public host.
- You want a consistent token check and a request id.
- Route config can be reviewed and rolled back.

## When not to use

- One service with a platform load balancer that already does the job.
- The gateway team must edit code for every product change. Push routes to self-service.
- Authorization depends on the resource body. That belongs in the service.

## Tradeoffs

| You gain | You pay |
|---|---|
| One place for edge policy | A component on every request's critical path |
| Hidden internal topology | Risk of a bottleneck team or a bottleneck CPU |
| Easier client configuration | Header and routing bugs affect everyone |

## Failure modes

- Auth only at the gateway, services trust a spoofable header.
- The gateway buffers large bodies and runs out of memory.
- A bad route sends one product's traffic to another.
- Timeouts longer than the service's own timeouts, so errors pile up.

## Implementation notes

- Verify tokens at the edge. Authorize in the service.
- Bound body size and time.
- Identity from the gateway to the service is authenticated (mTLS or a signed header from a trusted hop).
- Guide: [API gateways](../enterprise/apis/gateways.md).

## Related patterns

- [Backend for frontend](backend-for-frontend.md)
- [Rate limiting](rate-limiting.md)
- [Reverse proxy](reverse-proxy.md)
