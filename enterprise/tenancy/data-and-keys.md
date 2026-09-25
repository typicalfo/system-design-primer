---
title: "Per-tenant data and keys"
summary: "Put the tenant on every record and decide which tenants get their own encryption key."
tags: [tenancy, data, encryption, keys]
when_to_use: "Use when you are choosing a primary key, a cache key, or a KMS key strategy for a multi-tenant store."
related:
  - isolation-models.md
  - lifecycle.md
  - ../security/encryption-keys.md
  - ../compliance/retention.md
  - ../ai/rag.md
  - ../data/search.md
  - ../data/caching-at-scale.md
  - ../../patterns/sharding.md
last_reviewed: 2026-09-25
---

# Per-tenant data and keys

Shared stores leak through forgotten predicates and through keys that omit the tenant. Data placement and encryption keys are the same decision: whose blast radius is this byte in.

## Defaults

- Every tenant-owned row has a `tenant_id` that is part of the primary key or of a unique constraint, not a nullable attribute filled in later.
- Secondary indexes that the app queries lead with `tenant_id` when the query is tenant-scoped. A global index on email is a cross-tenant lookup. Treat it as privileged.
- Object storage keys are prefixed by tenant and are authorized server-side. Pre-signed URLs are scoped to one object and expire quickly.
- Cache keys include the tenant id. TTL does not fix a wrong key.
- Search documents carry the tenant id, and the query the user cannot edit includes a filter. Prefer a search realm or index per large tenant when the engine cannot enforce the filter underneath you.
- Queue messages carry the tenant id in a field the worker trusts only if your own publisher wrote it. Do not let an external producer set it.
- Encryption: one data key per sensitive object or per tenant, wrapped by a KEK. Offer a customer-managed key when the contract says the customer must be able to cut off your access. See [encryption](../security/encryption-keys.md).
- Analytics copies are tenant-scoped or de-identified. A warehouse role that can `SELECT *` from the raw pool is a second production database.

## Decide

| Key scope | Use when | Avoid when |
|---|---|---|
| Platform-managed key for the pool | Tenants are small and disk encryption plus authorization meets the contract | The customer requires the ability to destroy their key without your cooperation |
| Per-tenant DEK, platform KEK | You want crypto-shred of one tenant and a smaller blast radius | You have no deletion workflow and the keys will leak into backups anyway |
| Customer-managed KEK | The customer must disable the key in their cloud account | You cannot operate the failure mode "this tenant cannot read or write because they disabled the key" |
| Per-tenant database | Isolation model is silo | You only needed a separate key. A database is the expensive way to get one |

## Checklist

- [ ] A new table checklist item says "tenant id is in the key."
- [ ] Exports and backups can be limited to one tenant, or you have accepted that a restore is global and documented the consequence.
- [ ] Destroying a tenant key makes that tenant's ciphertext unreadable, including in the search index and the data lake, if that is the claim.
- [ ] Support staff who impersonate a user do it inside one tenant, with an audit record.

## Anti-patterns

- Globally unique email as the only primary key in a pooled user table, with tenant as a soft column.
- A pre-signed URL pattern that lists a bucket prefix the client can edit.
- One AES key for all tenants in an environment variable.
- Copying production rows into a shared sandbox "for debugging" without the same controls.
