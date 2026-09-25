---
title: "Content delivery network"
summary: "Serve cacheable bytes from a location near the user so the origin does not see that request."
tags: [edge, primer, caching]
when_to_use: "Use when many users fetch the same bytes and those bytes can be stale for a TTL you name."
related:
  - cache-invalidation.md
  - reverse-proxy.md
  - load-balancing.md
last_reviewed: 2026-09-25
---

# Content delivery network

## Problem

Users far from your origin pay a long round trip for static or otherwise cacheable content, and your origin spends capacity repeating the same response.

The System Design Primer covers the underlying idea in [Content delivery network](../README.md#content-delivery-network). This card is the operational form. The Primer prose is unchanged.

## When to use

- The content is static or safely cacheable (images, scripts, public downloads).
- You can purge or TTL when it changes.
- The cost of the CDN is less than the origin capacity it replaces, or the latency win is the requirement.

## When not to use

- The response is private to a user or a tenant. A shared cache key will leak it.
- The response must be current to the second and you have no purge path.
- You put the CDN in front of personalized HTML without a Vary rule and a private cache policy.

## Tradeoffs

| You gain | You pay |
|---|---|
| Lower latency and less origin traffic | Stale content until TTL or purge |
| A buffer against origin bursts | Cost that can exceed the origin you removed |
| TLS and caching at the edge | Another system that can serve the wrong object's cached copy |

## Failure modes

- A long TTL after an urgent change. Purge is the mitigation, and purge is eventually consistent.
- Cache key omits a header that changes the body.
- Authenticated responses cached and served to the next user.
- Origin outage hidden until the TTL expires, then a hard failure. That can be a feature if you meant to serve stale.

## Implementation notes

- The Primer's push versus pull distinction still holds: push when objects are few and you control updates; pull when the library is large and only recent objects are hot.
- Today a CDN often terminates TLS and can cache selected dynamic responses. Only do that for responses you are willing to see served late.
- Set `Cache-Control` deliberately. Default platform caching is how private data escapes.
- Version asset URLs so deploys do not depend on purge.

## Related patterns

- [Cache invalidation](cache-invalidation.md)
- [Reverse proxy](reverse-proxy.md)
- [Load balancing](load-balancing.md)
