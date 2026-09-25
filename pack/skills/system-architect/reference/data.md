---
title: "Data, consistency, and availability"
summary: "How to pick a store, a consistency model, and a replication scheme, with the Primer's older terms mapped to current names."
tags: [data, consistency, replication]
when_to_use: "Use when the design has to name a database, a consistency choice, or what a failover does to writes."
related:
  - estimates.md
  - scalability.md
  - ../SKILL.md
  - ../../../../patterns/README.md
  - ../../../../enterprise/reliability/multi-region.md
last_reviewed: 2026-09-25
---

# Data, consistency, and availability

Adapted from the System Design Primer by Donne Martin, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Attribution: [pack README](https://github.com/typicalfo/system-design-primer/blob/master/pack/README.md#attribution).

Pick the store from the access pattern, then pick the consistency you can actually operate. Vocabulary follows the Primer. "Master/slave" in the Primer means primary/replica (one writer) and "master/master" means multi-primary. Use the current terms in the design. Cards: [leader-follower](https://github.com/typicalfo/system-design-primer/blob/master/patterns/replication-leader-follower.md), [multi-leader](https://github.com/typicalfo/system-design-primer/blob/master/patterns/replication-multi-leader.md), [federation](https://github.com/typicalfo/system-design-primer/blob/master/patterns/federation.md), [sharding](https://github.com/typicalfo/system-design-primer/blob/master/patterns/sharding.md), [denormalization](https://github.com/typicalfo/system-design-primer/blob/master/patterns/denormalization.md), [consistency patterns](https://github.com/typicalfo/system-design-primer/blob/master/patterns/consistency-patterns.md), [availability and failover](https://github.com/typicalfo/system-design-primer/blob/master/patterns/availability-failover.md). Region placement and RPO/RTO are in [multi-region](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/reliability/multi-region.md) and [disaster recovery](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/reliability/disaster-recovery.md).

## SQL and NoSQL

Relational (SQL) gives ACID transactions: all-or-nothing, valid state to valid state, concurrent transactions equivalent to a serial order, and committed writes that stay committed. Use it for structured rows, real constraints, joins, and transactions.

NoSQL in the Primer is an umbrella: key-value, document, wide-column, graph. Data is usually denormalized and joined in the application. The Primer describes these systems with BASE: basically available, soft state, eventually consistent. That slogan is a tendency, not a law. Several stores now offer transactions over a subset of keys. Read the transaction scope you are relying on and write it down.

| Shape | Fits | Primer's caution |
|---|---|---|
| Key-value | Point reads and writes by id, session and cache data. O(1) when the key is known. | Anything richer moves into the application. |
| Document | One aggregate read and written together, fields that differ across records. | Weak fit when you constantly query across aggregates. |
| Wide-column | Very large append-heavy sets, range scans on a key prefix. | Data model is the row key. A wrong key is a full rewrite. |
| Graph | Relationship-heavy traversals (social graph). | Narrower tooling. Do not adopt it for ordinary CRUD. |

The Primer's SQL-tuning notes that still hold: index columns you filter, join, and sort; denormalize when a measured read ratio makes the join too expensive; keep hot rows in their own partition if that is what lets them stay in memory; benchmark.

**Dated.** The Primer's CHAR-vs-VARCHAR rules, the `VARCHAR(255)` byte argument, and the MySQL query cache are storage-engine folklore from a specific era. MySQL 8.0 removed the query cache. Pick types that match the domain and check the plan on the engine you run. The Primer also points DynamoDB at the 2007 Dynamo paper; that paper is Amazon's Dynamo, a different system. Treat current DynamoDB as a managed key-value and document store and read its current consistency model.

Logs, clickstreams, and leaderboards are the Primer's examples of a NoSQL-shaped write load. An audit or event ingest path is in that family. A billing ledger with cross-row constraints is in the SQL family.

## Replication

**Primary-replica.** One primary takes writes and replicates them to replicas that serve reads. If the primary dies, you promote a replica or serve reads only until you do. Failover logic is yours.

**Multi-primary.** More than one node takes writes. The system keeps serving writes when one writer dies. Conflicts get more likely as writers and latency grow. The Primer's warning: these systems are loosely consistent, or they pay synchronous latency to avoid that.

Costs that apply to both:

- A primary crash can lose writes that never reached a replica.
- Replicas replay writes. A heavy write load steals their read capacity, and lag grows as you add replicas.
- Some engines parallelize writes on the primary and apply them serially on the replica, so the replica falls behind under load.
- More hardware, more failure modes.

## Federation and sharding

**Federation** (functional partitioning) splits databases by domain: users in one, orders in another. Each store takes less traffic, holds a larger fraction of its working set in memory, and writes are not serialized through one primary. Joins across the split become application calls. Useless when one table is the whole load.

**Sharding** splits one dataset so each node holds a subset, often by a key hash or a range. Same benefits as federation, plus a smaller index. One shard down does not take the others down, and it does lose the rows on that shard unless you also replicate.

Costs the Primer emphasizes:

- The application has to know the shard. Cross-shard queries and transactions are a different, harder design.
- A key that clumps (the Primer's example is a popular user, or a naive geographic key) overloads one shard. Rebalancing is the expensive follow-up. Consistent hashing cuts how much data moves when you add a shard.
- A shard function you cannot change later is a product decision. Write it in Tradeoffs.

## Consistency patterns

With copies, choose what a read may return after a write:

- **Weak.** A later read might never see the write. The Primer's examples are realtime voice and games, where a gap is dropped rather than replayed.
- **Eventual.** A later read will see the write after a lag, often milliseconds, sometimes much longer under failure. Replication is asynchronous. DNS and mail are the Primer's examples. This is the usual choice when availability beats a synchronous write.
- **Strong.** After a successful write, reads see it. Replication of that write is synchronous. The cost is latency and, during a partition, refused writes or reads.

Say which one applies to which path. A system can be strong for "did the write commit" and eventual for a search projection over those writes.

## Availability patterns

**Active-passive.** Heartbeats. On missed beats the passive takes the address. Downtime depends on hot versus cold standby. Writes not yet replicated can disappear.

**Active-active.** Both sides take traffic. Callers (DNS or client config) must know both. Conflicts are an application problem the moment both sides write the same key.

Availability math is in [estimates.md](estimates.md). Failover hardware does not raise availability if the promotion path is untested or if both copies share a power domain, a deploy pipeline, or a schema change.

## CAP, and what has dated

The Primer states CAP as "pick two" of consistency, availability, and partition tolerance, then immediately says networks partition, so the real choice is consistency or availability during a partition.

- **CP:** during a partition, fail the request rather than serve a stale or split write. Right when a wrong read is worse than an error.
- **AP:** during a partition, answer with the copy you have. Right when being down is worse than being slightly behind, and you have a story for conflicts.

**Dated.** "Pick two of three" as a standing property of a system is the slogan Brewer later walked back. Partitions are an event, not a mode you live in. The modern framing is PACELC (Daniel Abadi): during a Partition you trade Availability against Consistency; Else, while healthy, you trade Latency against Consistency. Use PACELC when you write the tradeoff. A system can be CP during a partition and still waste latency on synchronous replication when the network is fine. Those are two choices. Write both.
