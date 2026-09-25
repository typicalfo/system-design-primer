---
title: "Load balancing"
summary: "Spread requests across healthy targets so one instance is not the user-facing capacity or the single failure."
tags: [edge, primer, availability]
when_to_use: "Use when more than one instance serves the same stateless role, or when you need health checks to remove a bad instance."
related:
  - reverse-proxy.md
  - availability-failover.md
  - bulkhead.md
last_reviewed: 2026-09-25
---

# Load balancing

## Problem

A single instance caps throughput and dies as a unit. A balancer spreads work and skips unhealthy targets.

The System Design Primer covers the underlying idea in [Load balancer](../README.md#load-balancer). This card is the operational form. The Primer prose is unchanged.

## When to use

- Application instances are stateless, or session state lives in a store you named.
- You can run at least two targets.
- Health checks reflect real ability to serve, not only that the process is listening.

## When not to use

- The bottleneck is the database. More app instances will open more connections and make it worse until the database is scaled.
- You need sticky sessions to hide state on the instance. Fix the state instead, unless the stickiness is temporary.
- One balancer with no pair. You moved the single point of failure.

## Tradeoffs

| You gain | You pay |
|---|---|
| Horizontal scale and removal of dead instances | A component that can itself fail or saturate |
| A place for TLS and routing | Health-check mistakes that drain the fleet or send traffic to a sick target |
| Layer 7 routing by path or header | More work per request than layer 4, usually small, still worth measuring if you are at the limit |

## Failure modes

- Health check too strict: instances flap out.
- Health check too weak: traffic goes to instances that cannot reach the database.
- Connection pile-up on a slow target if the balancer does not time out.
- Deploying all targets at once behind a balancer that then has nowhere healthy to send traffic.

## Implementation notes

- Run the balancers themselves as a pair.
- Prefer a shared session store and round-robin over sticky sessions.
- Layer 4 when you only need IP and port. Layer 7 when you route on HTTP.
- Drain connections before removing an instance.
- The Primer lists random, least loaded, session, round robin, and weighted round robin. Least loaded needs a load signal that is not already stale.
- The usual edge today is a cloud load balancer or an Envoy or nginx-class proxy, not a single hardware box.

## Related patterns

- [Reverse proxy](reverse-proxy.md)
- [Availability and failover](availability-failover.md)
- [Canary](canary.md)
