---
title: "Multi-tenant audit log review"
summary: "Design-reviewer findings on the multi-tenant audit log, led by the missing erasure path and the single-writer hash chain."
tags: [example, audit-log, review]
when_to_use: "Use when you want to see severity-ranked findings against a design that already looks complete."
related:
  - design.md
  - README.md
  - ../../skills/design-reviewer/SKILL.md
  - ../../skills/design-reviewer/checklist.md
last_reviewed: 2026-09-25
---

# Design review: multi-tenant audit log

Reviewed [design.md](design.md) against the [design-reviewer checklist](../../skills/design-reviewer/checklist.md). Checks the design already settles are not listed. In particular: the search index is a rebuildable projection with a sweeper, so a lost queue message does not lose an acknowledged event; idempotency falls through to a conditional create on the object key; exports read the bucket; tenant id is taken from the credential; TLS and encryption at rest are specified.

## Findings

### 1. Unclassified payloads are stored immutable, with no erasure path

- Severity: Critical
- Area: Data retention and deletion
- Evidence: `schema_id` is optional, and unknown ids are stored and labeled `unregistered`. The payload is a JSON object. Batch objects are immutable. Retention is 1 year or 7 years, and legal hold only stops deletion. Nothing in the design classifies fields or removes personal data from an acknowledged batch.
- Why it matters: A product bug or a wide payload (email, token, free text) becomes a seven-year record the operator cannot edit. Immutability then blocks the deletion a tenant or a person can demand. That is a privacy incident with no recovery short of throwing away the hash chain.
- Change: Reject unregistered schemas in production. Each registered field is classified. To erase, write a new manifest that keeps `event_id`, `prev_hash`, and the linkage, and drops the personal payload, and record who ordered the erasure. The registry has to be up for ingest to fail closed; give it a second instance.
- ASVS: v5.0.0 V14 Data Protection, V2 Validation and Business Logic

### 2. The per-tenant hash chain is a single writer on the request path

- Severity: High
- Area: Behavior at 10× load
- Evidence: Each batch object stores `prev_hash` of the previous batch for that tenant, and ingest "writes one immutable object per batch" before it acknowledges. Partitions are 32 ways by `tenant_id`. The latency budget allows a 200 ms p99 only if a same-region PUT is one hop. The cap is 500 events or 1 MB. Nothing sets a minimum, so a one-event batch is a legal call.
- Why it matters: Batches for one tenant cannot be written in parallel, and the 32 partitions do not split a tenant. A same-region PUT on the order of a few tens of milliseconds allows on the order of 20 sequential batches per second before the chain alone misses 200 ms. A producer that posts one event per action, for a tenant that is a tenth of today's 2,900/s peak, submits about 290 writes/s to that chain. Those calls queue for seconds. At a sustained 10× (29,000 events/s peak, about 1 TB/day) the same shape is about 2,900 single-event writes/s for that tenant. Full 500-event batches would fit (20 batches/s is 10,000 events/s); the design never requires them. Bandwidth is not the limit. The Primer's lopsided-shard failure is this chain.
- Change: Acknowledge against an append-only log partitioned by tenant, and build the hash-chained object in a consumer that can batch for up to the lag already allowed on the query path. Keep the object as the source of truth. Do not hold the user-facing p99 on a chain of PUTs.
- ASVS: omit

### 3. Events that matter can die in the producer process

- Severity: High
- Area: Failure modes and blast radius
- Evidence: Producers "retry in process" across the 15-minute home-region pause. The durability NFR starts when the service acknowledges. A crash before `202` loses the events. There is no outbox.
- Why it matters: The request is a record of actions the product already performed. A deploy of the product service during a region pause drops those actions, and the audit log's 99.9% target never moves, because the lost events were never submitted. The availability math does not see the real failure.
- Change: In the same transaction as the business write, insert an outbox row. A worker posts the batch until `202`. If a product team will not do that, the compliance owner accepts the loss in writing and the NFR says the record is best-effort before acknowledgement.
- ASVS: omit

### 4. The daily integrity root lives in the bucket it is meant to detect tampering of

- Severity: High
- Area: Security, mapped to OWASP ASVS 5.0.0
- Evidence: A nightly job writes `roots/yyyy-mm-dd` into the same bucket as the batches. Encryption at rest uses the provider key on that bucket.
- Why it matters: Anyone who can rewrite objects can rewrite the root to match. The hash chain then proves nothing to an auditor. A bug in the ingest role, or a stolen ingest credential, is enough.
- Change: Have a second principal, in a separate account the ingest role cannot write to, record the daily root (or publish it to a transparency log). Ingest keeps write access only to the batch prefix.
- ASVS: v5.0.0 V11 Cryptography

### 5. "Only the query service should read the index" is not a control

- Severity: High
- Area: Authentication and authorization
- Evidence: Tenant isolation on the query API is real: the tenant comes from the credential. The index itself is described as "the only path that should read" it. No network rule, no IAM condition, and no separate audience for ingest versus query credentials are specified. Both APIs sit in one region and one sketch.
- Why it matters: A second client, or a product role granted index access during an incident, runs a query with no tenant predicate. That is a cross-tenant read of 90 days of audit data, which the design calls a correctness requirement.
- Change: Block index access to the indexer and the query role. Mint ingest tokens and query tokens with different audiences. Add a test that a query built for tenant A returns zero rows of tenant B, including when the caller passes tenant B's id in the query string.
- ASVS: v5.0.0 V8 Authorization, V9 Self-contained Tokens

### 6. A destroyed home region deletes the one-year tier

- Severity: High
- Area: Failure modes and blast radius
- Evidence: The NFR says a region loss must not destroy acknowledged events inside the retention window, and the tradeoff says an asynchronous copy covers "the seven-year prefix only," so a destroyed home region "loses the one-year tier." The design marks this as weaker than the NFR.
- Why it matters: Unavailability and destruction are different faults. Manual promotion in 15 minutes covers a paused region if the bytes are still there. It does not cover a region that is gone. Default-retention tenants, the 32.85 TB one-year tier, have a single region.
- Change: Pick one and delete the other. Either replicate every acknowledged batch to the second region before you claim the NFR, or change the NFR so default retention is single-region and only the seven-year flag is a disaster-recovery product.
- ASVS: omit

### 7. On-call can look up a batch, and nothing pages them

- Severity: High
- Area: Observability and on-call
- Evidence: The NFR is that on-call "can tell, for a batch id, whether it was acknowledged." No SLI, no burn alert, no named page. Admin changes to retention and legal hold are an API (`PUT /v1/admin/tenants/{id}`) with no statement that those calls are themselves audited.
- Why it matters: The failure this service exists to catch is silent loss. A dashboard somebody might open does not catch it. An operator who shortens retention or clears a legal hold, with no record, undoes the control the export is supposed to provide.
- Change: Page the platform owner when the fraction of `202` responses, or the age of the newest manifest per home region, burns a stated SLO (the design's 99.9% monthly ingest target is the starting point). Write admin calls to the same log, under a platform tenant, from a role that cannot delete them.
- ASVS: v5.0.0 V16 Security Logging and Error Handling

### 8. Query callers cannot see the lag the design allows

- Severity: Medium
- Area: Cache invalidation
- Evidence: Queries "may lag ingest by up to 60 s" and are served from the index. `GET /v1/events` returns events and a cursor, not how far the index has caught up. The sweeper repairs a missing marker; it does not tell the caller the watermark.
- Why it matters: An auditor who acts, then immediately searches, can conclude the action was not recorded. They will re-emit or file an incident. The projection strategy is sound; hiding its lag makes the 60 s NFR untestable from the outside.
- Change: Return the index watermark (the latest `received_at` indexed for that tenant) on every query. Document that a row newer than the watermark is absent on purpose.
- ASVS: omit

### 9. A bad registered schema cannot be quarantined without blocking the tenant

- Severity: Medium
- Area: Migration and rollback
- Evidence: Rollback in the tradeoffs is the producer's in-memory retry and a client that stops calling. Unknown schemas are accepted during a 90-day window. Nothing describes pulling one schema version out of the commit path while other tenants and other schemas keep flowing. Objects already written cannot be deleted by a rollback, which is correct for a log and incomplete for a bad version.
- Why it matters: The first version a team registers will be wrong. With finding 1 fixed, that version is still immutable once acknowledged. Rollback of the product deploy does not stop a worker that is still posting, and there is no place to park poison batches.
- Change: Let the registry mark a version as quarantine. Ingest accepts those batches onto a side prefix, excludes them from the tenant's default export, and does not advance the hash chain with their payload until an owner releases or rejects them.
- ASVS: omit

### 10. Index cost has no alarm

- Severity: Low
- Area: Cost
- Evidence: The hot index is about 27 TB at the stated rate (9 TB raw × 1.5 overhead × 2 copies). A sustained 10× rate for one 90-day window is about 270 TB, on the same formula. Retention of the index is "90 days" in prose. The seven-year flag is a separate tenant setting on the cold tier.
- Why it matters: The expensive mistake is an operator pointing the index retention at the legal retention. The bill moves from tens of terabytes to the seven-year set, and nothing in the design notices.
- Change: Alarm when index bytes exceed the 90-day estimate by a stated margin, and refuse an index retention setting above 90 days in the admin API.
- ASVS: omit

## Accepted risks

- Interactive queries are eventual, with a 60 s target, because the source of truth stays in object storage and exports read it. Finding 8 is the missing way for a caller to see that lag, not a reason to put queries on the bucket.
- Ingest instances are stateless behind a load balancer, so one instance is not a single point of failure. The per-tenant chain in finding 2 is a write bottleneck, not a second copy of the bytes.
- A home-region outage may pause ingest until a human promotes, with a 15-minute target. That pause is acceptable only together with finding 3 (the pause must not drop actions) and finding 6 (the bytes must still exist when the region comes back or is abandoned).
