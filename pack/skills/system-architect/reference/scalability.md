# Scaling patterns

Adapted from the System Design Primer. Attribution: [pack README](../../../README.md#attribution).

Use a pattern when [estimates](estimates.md) show a bottleneck. Record the disadvantage in the design's tradeoffs. Definitions below follow the Primer; sentences marked dated name the current equivalent. Cards with the same names live in [patterns/](../../../../patterns/README.md): [cache-aside](../../../../patterns/cache-aside.md), [write-through](../../../../patterns/write-through.md), [write-behind](../../../../patterns/write-behind.md), [sharding](../../../../patterns/sharding.md), [CDN](../../../../patterns/cdn.md), [load balancing](../../../../patterns/load-balancing.md), [reverse proxy](../../../../patterns/reverse-proxy.md), [message queues](../../../../patterns/message-queues.md). The enterprise resilience cards ([retry](../../../../patterns/retry-with-backoff.md), [circuit breaker](../../../../patterns/circuit-breaker.md), [bulkhead](../../../../patterns/bulkhead.md), [load shedding](../../../../patterns/load-shedding.md)) extend the Primer's back-pressure note.

## Performance and scalability

A system has a performance problem when it is slow for one user. It has a scalability problem when it is fast for one user and slow under load. Scalability means performance grows in proportion to the resources you add. Latency is the time for one action. Throughput is how many actions complete per unit time. Target the throughput the requirement states, at a latency the requirement allows.

## Horizontal scale and load balancing

Prefer several ordinary machines over one larger machine. The Primer's condition: application servers hold no user-specific state. Sessions and uploads live in a store you name, not on the instance. More app servers means more connections into caches and databases; those stores have to accept the new connection count.

A load balancer spreads requests, skips unhealthy targets, and stops one instance from taking the whole pile. One balancer is itself a single point of failure. Run a pair, active-passive (standby takes over the address; only one side serves) or active-active (both serve). Failover can drop writes that had not replicated yet. The balancer is also a bottleneck if it is undersized.

- **Layer 4** balances on IP and port, and forwards packets. Cheaper, less information.
- **Layer 7** terminates the connection and can route on the HTTP path, header, or cookie (video to one pool, billing to another). More flexible, more work per request. On current hardware that cost is often small; measure it before you avoid layer 7 for performance.

Algorithms the Primer lists: random, least loaded, session cookie, round robin, weighted round robin. Session stickiness is a substitute for fixing state on the instance. Prefer a shared session store, then you can round-robin.

A reverse proxy (nginx and HAProxy do both jobs) is useful even in front of one origin: hide the origin, terminate TLS, compress, cache, serve static files. A single proxy is a single point of failure, same as a single balancer.

**Dated.** The Primer's concrete proxies include Squid and an old HAProxy architecture note. The usual edge today is a cloud load balancer or an Envoy/nginx-class proxy, with static assets on a CDN. The job (terminate TLS, health-check, spread load) is unchanged.

## CDN

A CDN serves bytes from a location near the user and takes that traffic off your origin. Push: you upload when content changes. Better when objects are few and rarely updated. Pull: the CDN fetches on first request and keeps the object for a TTL. Better when traffic is heavy and only recent objects are worth storing. Stale content is the failure mode of a long TTL. Cost can exceed the origin capacity it replaces; compare the two bills.

The Primer treats dynamic HTML as origin work, with a note that some CDNs already served dynamic content. Today a CDN commonly terminates TLS and caches selected dynamic responses at the edge. Use that only for responses you are willing to see served late, and name the TTL.

## Cache

A cache absorbs repeated reads and smooths a hot key so it does not pin one database partition. Place it where the repeated read actually happens: client, CDN, reverse proxy, or an in-memory store in front of the database (the Primer's examples are Memcached and Redis). Caching a whole query string is brittle, because any changed cell invalidates an unknown set of queries. Cache an object you can invalidate by id.

Redis adds persistence and structures such as sorted sets. Memcached is the Primer's usual cache-aside store. Prefer the cache your platform already runs.

Update strategies:

| Strategy | Behavior | Cost |
|---|---|---|
| Cache-aside | App reads the cache, and on a miss loads the store and fills the cache. | A miss is three trips. Writes to the store leave the cache stale until TTL or an explicit delete. A new empty node is a cold start. |
| Write-through | App writes the cache; the cache writes the store synchronously. | Slow writes, fresh reads. Data nobody reads still occupies memory; use a TTL. A new node stays cold until the next write. |
| Write-behind | App writes the cache; the store is updated asynchronously. | Fast writes. A crash before the flush loses those writes. |
| Refresh-ahead | Cache reloads a hot entry before its TTL. | Low latency when the prediction is right. Extra load when it is wrong. |

Invalidation is the hard part. Name who deletes or overwrites the entry, and the maximum staleness a caller can observe. If the cached view can be rebuilt entirely from a source of truth, say that, and treat the cache as a projection with a lag target rather than as an independent store.

**Dated.** "Tune the database query cache" in the Primer refers to the MySQL query cache, which MySQL 8.0 removed. Use the database buffer pool plus an application or CDN cache.

## Async work

Move work off the request when the user does not need the result to finish the action. The Primer's shape: the app enqueues a job and returns a status; a worker runs it and marks it complete. The user path stays short. The queue is now part of correctness.

- A queue that is only memory (the Primer's warning about Redis as a broker) can lose jobs.
- A managed queue is often at-least-once. Consumers must be idempotent. The Primer names SQS and also calls it high-latency; at-least-once is still the contract to design for, and latency has to be measured on the current service.
- RabbitMQ is the Primer's example of running your own broker. You own the nodes.
- A task queue (the Primer's example is Celery) adds scheduling. Celery is Python-specific. The mechanism is a worker on a queue, not that library.

**Dated.** For a durable, replayable stream, the usual equivalent is a log such as Kafka or the cloud log on the same platform. For multi-step work with timers and compensation, a workflow engine (Temporal and its peers) replaces a pile of ad-hoc task queues. Use those names when the requirement is replay or multi-step state, not as decoration.

Backpressure: cap the queue. Past the cap, refuse with a busy status and tell the client to retry with exponential backoff. An unbounded queue spills to disk and gets slower exactly when you are overloaded.

Do not insert a queue for a cheap, latency-sensitive call. The queue adds delay and a failure mode.

## Service boundaries

Split a web tier from an application tier when they need to scale on different axes. The Primer's microservices note: small processes, each owned by a small team, talking over a narrow API. The cost is deployment and operational complexity. Prefer one deployable unit until a team or a scale number forces the split. See [data.md](data.md) for how data follows that split (federation).

**Dated.** The Primer's service-discovery examples are Consul, etcd, and ZooKeeper. They are still valid systems. On Kubernetes, Service DNS plus readiness probes cover the common case, and a separate discovery cluster is extra machinery. Health checks remain non-negotiable either way.

## APIs between components

The Primer's split: REST exposes resources with a small set of verbs, stays stateless, and fits public HTTP. RPC exposes procedures, couples the client to the server's operations, and was the Primer's choice for internal calls that need to be tight. A new RPC method is a new contract; a REST API that is really a list of verbs-as-URLs has the same coupling with extra ceremony.

**Dated.** Internal RPC today is usually gRPC on Protocol Buffers (the Primer already names Protobuf, alongside Thrift and Avro). The Primer's complaint that nested resources take many round trips is the problem GraphQL and backend-for-frontend aggregation were adopted to reduce. Pick one style per boundary and write it in the API section.
