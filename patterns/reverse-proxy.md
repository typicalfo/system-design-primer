---
title: "Reverse proxy"
summary: "A proxy in front of the origin terminates client connections and can cache, compress, and hide the origin."
tags: [edge, primer]
when_to_use: "Use when you want TLS termination, request limits, static file serving, or a single front for one or more origins."
related:
  - load-balancing.md
  - cdn.md
  - api-gateway.md
last_reviewed: 2026-09-25
---

# Reverse proxy

## Problem

Clients should not connect straight to application processes. You need a place to terminate TLS, enforce limits, and optionally cache.

The System Design Primer covers the underlying idea in [Reverse proxy (web server)](../README.md#reverse-proxy-web-server). This card is the operational form. The Primer prose is unchanged.

## When to use

- You have at least one origin to protect or to configure in one place.
- You need behaviors a load balancer at layer 4 will not do (path routing, header edits, caching).
- The proxy is highly available. A single proxy is a single point of failure, same as a single balancer.

## When not to use

- You are adding it only to get a vendor logo. If the platform load balancer already terminates TLS and routes, a second hop must earn its latency.
- The proxy will hold unbounded request bodies or long connections without a timeout.

## Tradeoffs

| You gain | You pay |
|---|---|
| TLS, compression, caching, and a hidden origin | Another hop and another config to get wrong |
| A stable front door during origin deploys | Cache and header bugs that become user-facing |
|  | Capacity planning for the proxy itself |

## Failure modes

- One proxy dies and the site is down.
- Buffered uploads exhaust proxy memory.
- The proxy strips a header the origin needed for tenant or trace context.
- Stale cached error pages.

## Implementation notes

- nginx and HAProxy still cover this job. Envoy is the common programmable proxy. Squid is no longer the default choice the Primer's era sometimes implied.
- Set client, proxy, and upstream timeouts explicitly.
- Forward a request id.
- Do not let the proxy be the only copy of routing config without review.

## Related patterns

- [Load balancing](load-balancing.md)
- [API gateway](api-gateway.md)
- [CDN](cdn.md)
