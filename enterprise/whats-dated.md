---
title: "What's dated in the Primer"
summary: "Where the System Design Primer's advice shows its era, and the current equivalent to use in a design."
tags: [primer, dated, modernization]
when_to_use: "Use when a Primer section is the starting point and you need to know what not to copy literally into a new system."
related:
  - README.md
  - ../patterns/consistency-patterns.md
  - ../patterns/replication-leader-follower.md
  - ../patterns/message-queues.md
  - ../pack/skills/system-architect/reference/data.md
  - ../patterns/cell-based-architecture.md
  - ../patterns/shuffle-sharding.md
  - ../patterns/durable-workflow.md
last_reviewed: 2026-09-25
---

# What's dated in the Primer

The Primer is still a sound way to scope a problem, sketch boxes, estimate, and name tradeoffs. Several concrete technologies and slogans are from the mid-2010s. Use the modern equivalent below, and say in the design that you did. The original Primer text stays as it is.

## CAP and PACELC

The Primer says a system supports two of consistency, availability, and partition tolerance, then immediately notes that networks partition so the real choice is consistency or availability. The standing "pick two" slogan is what aged. Partitions are an event. While the network is healthy you also trade latency against consistency. That is PACELC. Write both choices. See [consistency patterns](../patterns/consistency-patterns.md) and the [data reference](../pack/skills/system-architect/reference/data.md).

## Replication terminology

Master-slave and master-master are the Primer's names. In new designs say leader-follower (or primary-replica) and multi-leader. The mechanics it describes are unchanged: one writer versus several, lag, lost writes on failover, and conflicts. Cards: [leader-follower](../patterns/replication-leader-follower.md), [multi-leader](../patterns/replication-multi-leader.md).

## Query cache and SQL folklore

"Tune the query cache" points at the MySQL query cache. MySQL 8.0 removed it. Use the buffer pool and an application or CDN cache. `VARCHAR(255)` as a performance trick and CHAR-versus-VARCHAR rules from that era are engine folklore. Size types to the domain and check the query plan. See the [data reference](../pack/skills/system-architect/reference/data.md).

## Dynamo and DynamoDB

The Primer points at Amazon's 2007 Dynamo paper in places that readers now map onto the product DynamoDB. They are different systems. Read the consistency model of the product you will run.

## Latency numbers

The published table (SSD at about 1 GB/s, 1 Gbps Ethernet, HDD seeks) is the wrong absolute for NVMe and 10/25/100 Gbps networks. Keep it as a ratio tool: memory is far faster than disk, disk is far faster than a cross-region round trip, and a cross-continent trip dominates a local cache hit. Do not replace the table with invented "current" numbers. Measure the hop you are betting on. Source note: [estimates reference](../pack/skills/system-architect/reference/estimates.md).

## Availability patterns

A second replica is not a cell. Failover between two copies of one stack still shares fate when the shared dependency fails. A cell is a full stack with its own copy of those dependencies, and shuffle sharding is how tenants share a pool without all sharing the same failure. See [cell-based architecture](../patterns/cell-based-architecture.md) and [shuffle sharding](../patterns/shuffle-sharding.md). The Primer's failover sketch is still the right picture for one database.

## Proxies and load balancers

The job is the same: health checks, TLS termination, spread load, more than one balancer. The usual implementation is a cloud load balancer or an Envoy or nginx-class proxy. Squid is not the default cache in front of an origin anymore. A CDN often terminates TLS and can cache selected dynamic responses. Only cache responses you are willing to serve late. Cards: [load balancing](../patterns/load-balancing.md), [reverse proxy](../patterns/reverse-proxy.md), [CDN](../patterns/cdn.md).

## Queues

Redis as a broker can lose jobs. RabbitMQ means you run the nodes. SQS is at-least-once. Those warnings hold. For a durable replayable stream, use a log (Kafka or the cloud equivalent). A queue does not by itself resume a multi-step process after a worker dies. That needs a durable workflow: persisted steps, timers, and compensation. See [durable workflow](../patterns/durable-workflow.md). Celery is one Python task library, not the pattern. The pattern is a worker on a durable queue. See [message queues](../patterns/message-queues.md) and the [outbox](../patterns/transactional-outbox.md).

## Service discovery

Consul, etcd, and ZooKeeper are still real systems. On Kubernetes, Service DNS plus readiness probes cover the common case. A separate discovery cluster is extra machinery until you have a reason. Health checks remain mandatory either way. See the [scalability reference](../pack/skills/system-architect/reference/scalability.md).

## RPC, REST, and clients

Protobuf, Thrift, and Avro are the Primer's RPC examples. Internal RPC today is usually gRPC on Protobuf. The Primer's complaint that nested resources take many round trips is why GraphQL and a backend-for-frontend exist. Pick one style per boundary. See [API styles](apis/styles.md).

## Microservices

The Primer already lists operational complexity as the disadvantage. What it does not say is when not to split: a small team, unclear boundaries, no platform, or a transaction that still wants one database. Start with a [modular monolith](modernization/modular-monolith.md). Extract with a [strangler](modernization/strangler-fig.md) when a team or a scale number forces it. [Conway's law](organization/conways-law.md) will win over a diagram.

## Security

The Primer's security section is explicitly a stub: encrypt, sanitize, parameterize, least privilege. That floor still matters and it is not a design. Identity, authorization, ASVS, supply chain, tenancy, and audit are the [security](security/threat-modeling.md) and [identity](identity/oidc-oauth2.md) guides. The design reviewer checklist is the gate.

## What did not age

Horizontal scale of stateless app tiers, load balancing, caching objects by id, replication lag, sharding hot keys, back-pressure on queues, and estimating with explicit arithmetic are still the right instincts. Use them, then attach an owner, an SLO, and a rollback.
