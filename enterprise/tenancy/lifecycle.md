---
title: "Tenant onboarding and offboarding"
summary: "Provision a tenant as a record plus policy, and offboard it including access, exports, deletion, and backups."
tags: [tenancy, onboarding, offboarding, deletion]
when_to_use: "Use when a customer is created, suspended, moved, or closed and you must say what happens to identity, data, and spend."
related:
  - isolation-models.md
  - data-and-keys.md
  - routing.md
  - ../identity/saml-sso.md
  - ../compliance/retention.md
  - ../compliance/privacy.md
  - ../cost/allocation.md
  - ../identity/scim-provisioning.md
last_reviewed: 2026-09-25
---

# Tenant onboarding and offboarding

A tenant is a lifecycle, not a row insert. Onboarding sets identity, placement, limits, and keys. Offboarding removes access and data on a schedule you can explain to the customer and to counsel.

## Onboarding defaults

- Create the tenant record first: id, home region, isolation mode, retention, plan, and status (`provisioning`, `active`).
- Provision dependencies in an order you can retry: directory entry, database or schema, key, default roles, limits. The pipeline is idempotent. A second run does not create a second tenant.
- SSO comes after the tenant exists. Invite the first admin. Do not activate paid features until an admin has signed in and accepted the terms you actually require.
- Seed nothing from another tenant. Demo data is synthetic and marked.
- Record who created the tenant and which plan limits apply. That record feeds [cost allocation](../cost/allocation.md).

## Offboarding defaults

1. Disable new interactive login and API tokens. Status becomes `suspended` or `closing`.
2. Revoke refresh tokens and service credentials. In-flight jobs stop or finish a defined drain.
3. Offer or run the contractual export while the data is still readable.
4. Delete or crypto-shred tenant data in primary stores, indexes, caches, object storage, queues, and warehouses.
5. Apply the same decision to backups: age them out, exclude them, or destroy the tenant key so old backups cannot be read. Say which. See [retention and deletion](../compliance/retention.md).
6. Keep the audit of the deletion itself for as long as the control framework requires, without keeping the customer's payload.
7. Release the name and the host only after the data is gone, so a new tenant cannot inherit links or webhooks.

Legal hold pauses deletion for that tenant and no one else.

## Decide

| Event | Default behavior |
|---|---|
| Trial expiry | Suspend access, retain data for the stated grace period, then delete |
| Non-payment | Suspend writes first or suspend all access. Pick one in the contract and implement that one |
| Admin "delete organization" | Require a second factor or a typed confirmation, then run the offboard workflow, do not hard-delete in the request thread |
| Security incident at the tenant | Your incident process plus their admin. Do not silently copy their data into a shared forensics bucket without a policy |

## Checklist

- [ ] Provisioning is idempotent and visible (a tenant does not sit at `provisioning` forever without an alert).
- [ ] Suspension is reversible. Closing is not, after the deletion window.
- [ ] A closed tenant's webhook endpoint and SSO config cannot still receive or emit events.
- [ ] You can prove, for one test tenant, that primary data and the search index no longer return it.
- [ ] Billing stops. Orphaned cloud resources are tagged with the tenant id so they die with the workflow.

## Anti-patterns

- `DELETE FROM tenants WHERE id = ?` as the offboarding plan.
- Reusing a tenant id for a new customer.
- Leaving the object-storage prefix because the database delete succeeded.
- A grace period that exists in the marketing page and not in a job.
