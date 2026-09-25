---
title: "Backend for frontend"
summary: "A server-side API shaped for one client, aggregating downstream services so the client does not."
tags: [api, clients]
when_to_use: "Use when a specific client (web, mobile, or a partner) needs a different aggregation or auth cookie story than the domain APIs provide."
related:
  - api-gateway.md
  - cqrs.md
  - ../enterprise/apis/styles.md
last_reviewed: 2026-09-25
---

# Backend for frontend

## Problem

General-purpose APIs force every client to fan out and to ignore most of the payload. A backend for frontend (BFF) does that fan-out for one client.

## When to use

- The client has a distinct shape or trust model (a browser that should not hold a refresh token, a mobile app on a high-latency network).
- The aggregation changes with that client's screen, and the client team should own it.
- Downstream services stay the systems of record.

## When not to use

- One client and one service. The BFF is an extra hop.
- You are tempted to put domain rules only in the BFF, so other clients bypass them.
- Several BFFs copy the same business rule instead of calling the domain service.

## Tradeoffs

| You gain | You pay |
|---|---|
| Fewer round trips for that client | Another deployable per client family |
| A place for the token-holding cookie | The BFF can become a hidden monolith |
| Client-specific payloads | Duplication if domain rules leak into it |

## Failure modes

- The BFF caches another tenant's aggregation under a shared key.
- Downstream timeouts are longer than the client's patience.
- A domain change requires every BFF to deploy because they each reimplemented the rule.
- The BFF is the only authorization check.

## Implementation notes

- Own the BFF with the client team.
- Keep domain writes in the domain service.
- Authorize downstream with the user and tenant, not with a god credential, unless the BFF is explicitly the policy enforcement point and the downstream is not reachable another way.
- For browsers, the BFF is the right place to hold refresh tokens. See [OIDC](../enterprise/identity/oidc-oauth2.md).

## Related patterns

- [API gateway](api-gateway.md)
- [CQRS](cqrs.md)
