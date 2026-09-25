---
title: "SCIM provisioning"
summary: "Push user and group lifecycle from the IdP with SCIM 2.0, and treat deprovision as disable-now plus a separate delete decision."
tags: [identity, scim, provisioning, directory]
when_to_use: "Use when an enterprise tenant expects the IdP to create, update, and remove users and groups in your product."
related:
  - oidc-oauth2.md
  - saml-sso.md
  - authorization-models.md
  - secrets.md
  - ../tenancy/lifecycle.md
  - ../compliance/audit-logs.md
  - ../compliance/retention.md
  - ../data/idempotency.md
last_reviewed: 2026-09-25
---

# SCIM provisioning

SCIM 2.0 is how an identity provider pushes accounts into an application. [RFC 7643](https://www.rfc-editor.org/rfc/rfc7643) (September 2015) is the core schema. [RFC 7644](https://www.rfc-editor.org/rfc/rfc7644) (September 2015) is the HTTP protocol. Both are Standards Track. A user resource and a group resource are the two objects most products need. `externalId` is the IdP's stable id for the user. Your internal id is separate.

SSO without SCIM tells you who is signing in now. It does not tell you who left the company yesterday.

## Decide

| Choose | Use when | Avoid when |
|---|---|---|
| SCIM as the source of truth | The tenant has an IdP and you must disable leavers without waiting for a login | You have no directory and every account is a direct signup |
| Just-in-time (JIT) from the SSO assertion | A tenant has no SCIM client, and creating the user on first login is acceptable | You need deprovision. JIT never hears about a user who stops signing in |
| SCIM plus a narrow JIT backfill | A group push can lag the first login by minutes and you accept that race | JIT creates users the IdP did not intend to provision, and you cannot name the rule |
| Soft disable on deprovision | The IdP says the user is gone and you may need to undo a bad sync | You are executing a retention deletion the customer already confirmed. That is a different job. See [retention](../compliance/retention.md) |
| Hard delete on the SCIM DELETE | Counsel and the retention policy say the row goes now, and the IdP's DELETE means erase | The IdP sends DELETE for "disable," which some deployments do. Confirm that in a test tenant before you map DELETE to erasure |

## Defaults

- One SCIM bearer token per tenant, stored as a secret, rotatable, and unable to read another tenant. See [secrets](secrets.md). A global admin token for "the SCIM integration" is a cross-tenant bug.
- Upsert on `externalId`. A replayed POST for the same `externalId` updates the same user. It does not create a second account. See [idempotency](../data/idempotency.md).
- `active=false` disables login immediately and revokes sessions and refresh tokens. Do not wait for the access token to expire if the user was an admin.
- Map IdP groups to your roles in a table the tenant admin can see. The group name is not a permission string you evaluate raw. See [authorization models](authorization-models.md).
- RFC 7644 lists resources with `startIndex`, `count`, and `totalResults`. Follow the pages. A client that stops at the first page will leave members out and then "remove" them.
- PATCH in RFC 7644 is a list of operations (`add`, `remove`, `replace`) against a path. Deployments differ. Some clients PUT the whole user. Some omit an attribute when they mean "leave it," and some omit it when they mean "clear it." Apply an operation only when it is explicit. Do not invent a vendor's quirk. Record the request shape you accepted, and test it.
- Rate-limit per token. Return 429 when a full-directory resync would starve interactive logins. The RFCs do not define one quota. Publish the limit you enforce and back off on the client you run yourself.
- Audit the actor (the token's tenant), the `externalId`, the operation, and the result. Do not log the bearer token or a password attribute. See [audit logs](../compliance/audit-logs.md).
- Deprovision is a tenant lifecycle event. Suspending the tenant is a different switch. See [tenant lifecycle](../tenancy/lifecycle.md).

## JIT and SCIM together

JIT reads attributes off the SSO assertion and creates or updates a user at login. It is the right default for a tenant that has not connected SCIM. Once SCIM is connected, SCIM owns create, update, and disable. Keep JIT only as a short race fill: the user is in a group the IdP already pushed, and the user record has not landed yet. A JIT user who is not in any provisioned group should not become an admin because the assertion contained a stale group name.

Leavers are the SCIM case. A disabled user who can still call the API with a refresh token was not deprovisioned.

## Checklist

- [ ] The same `externalId` posted twice yields one user.
- [ ] Group add and group remove change the role mapping, and a point read of a protected object follows.
- [ ] `active=false` kills sessions for that user in that tenant.
- [ ] A SCIM token for tenant A cannot address tenant B, including by guessing an id.
- [ ] Pagination returns every member of a large group in a test.
- [ ] PATCH and PUT both have a written rule for omitted attributes, and a test locks that rule.
- [ ] DELETE is either disable or erase, and the runbook says which.

## Anti-patterns

- JIT only, and a quarterly spreadsheet for "who should still have access."
- One SCIM token in a shared vault used by every tenant's sync job.
- Treating a failed page of a group sync as "those users were removed."
- Hard-deleting on the first DELETE during a pilot, then being unable to undo the IdP's bug.
- Logging the full SCIM body, including attributes you asked the IdP not to send.

## Related

- [OIDC and OAuth 2.0](oidc-oauth2.md) and [SSO and SAML](saml-sso.md) for the login that SCIM does not replace.
- [Authorization engines](authorization-engines.md) if group membership is replicated into a relationship store.

## Further reading

- [RFC 7643, SCIM Core Schema](https://www.rfc-editor.org/rfc/rfc7643)
- [RFC 7644, SCIM Protocol](https://www.rfc-editor.org/rfc/rfc7644)
