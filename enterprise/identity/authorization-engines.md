---
title: "Authorization engines"
summary: "Keep simple RBAC in the service that owns the row, and add a relationship or policy engine when many services must answer the same graph or the same policy."
tags: [identity, authorization, rebac, zanzibar, policy]
when_to_use: "Use when authorization no longer fits in one service's role table and you are choosing an engine, a cache, and a migration."
related:
  - authorization-models.md
  - scim-provisioning.md
  - oidc-oauth2.md
  - ../security/zero-trust.md
  - ../compliance/audit-logs.md
last_reviewed: 2026-09-25
---

# Authorization engines

[Authorization models](authorization-models.md) chooses RBAC, ABAC, or ReBAC. This page is where that decision runs. An engine is a policy decision point with its own store. An in-app check is the same decision written next to the query. Both have to default to deny, and both have to see the subject and the tenant from the credential.

## Decide

| Choose | Use when | Avoid when |
|---|---|---|
| Checks in the owning service | One service, a small role table, and the list query is a SQL predicate you can read | Every service grows its own copy of "who is an admin" |
| Zanzibar-style relationship engine | Access is a graph (user, group, folder, document) shared by many services | The only question is "does this user have role R in this tenant" |
| Cedar or another embedded policy language | Decisions are attributes and conditions you want one language for, evaluated in-process or as a managed service | The hard part is "list every object user X can see" over millions of tuples |
| OPA/Rego | Admission, infrastructure, or request-shaped policy shared across proxies and services | You need a durable relationship store. Rego evaluates data you hand it. It is not the system of record for the graph |

## What the engines are

[Zanzibar](https://www.usenix.org/conference/atc19/presentation/pang) (Pang et al., USENIX ATC 2019) is Google's paper on a global authorization system. The model is relationship tuples. A check asks whether a user has a relation on an object, including relations computed through other tuples (group membership, parent folders). Clients pass a consistency token, called a zookie in the paper, so a check is at least as new as a write the caller has already seen.

The new-enemy case is why that token exists. Someone is removed from a group, and new content is then shared with the group. If the content read sees the new object but the membership check still uses the old "user is in the group" snapshot, the removed person sees content created after they lost access. The check and the content have to be ordered. A token from the membership write, required on later checks, is one way to do that. Read the paper for the mechanism. This page does not copy it.

[OpenFGA](https://openfga.dev/) is a CNCF project that implements this style of check. The [CNCF project page](https://www.cncf.io/projects/openfga/) records that it was accepted on 14 September 2022 and moved to Incubating on 28 October 2025. [SpiceDB](https://github.com/authzed/spicedb) is another open-source store for the same kind of tuple check. Neither one removes the need for a point check on the read that returns the object.

[Cedar](https://cedarpolicy.com/) is an open-source policy language. [Amazon Verified Permissions](https://aws.amazon.com/verified-permissions/) is a managed service that evaluates Cedar. The implementation is also on [GitHub](https://github.com/cedar-policy/cedar). Cedar fits attribute rules ("this principal, this action, this resource, these context fields"). It is a poor place to hide a million parent-folder tuples unless you have already decided how those tuples are loaded.

[Open Policy Agent](https://www.openpolicyagent.org/) evaluates Rego. The [CNCF page](https://www.cncf.io/projects/open-policy-agent-opa/) records acceptance on 29 March 2018, Incubating on 2 April 2019, and Graduated on 29 January 2021. OPA is a strong fit for admission control and for request policy at a gateway. Hand it the attributes. Do not make it the only copy of your user-to-document graph unless you also own the sync and the list query.

## Defaults

- One decision for the point read and the list. A list of "documents user X can see" that uses a different rule than `GET /documents/{id}` will leak. If the engine has a list or expand API, use it, and still check the id you are about to return.
- List queries are the expensive ones. A loop of checks over every row in the table will time out. Model the question you actually ask (children of this folder, objects with this direct relation) and measure it. Caching a check does not make a bad list query cheap.
- Cache allow and deny for a short time on hot paths. Do not cache a privileged membership for minutes after a removal. [Authorization models](authorization-models.md) makes the same point for in-app checks.
- The relationship store is a replica. When SCIM removes a group member, or the app moves a document, the tuple write is part of that operation, not a nightly job. See [SCIM provisioning](scim-provisioning.md). A lag you have not bounded is an authorization bug.
- Log the decision: subject, action, resource id, allow or deny, policy or model version, and the consistency token or policy hash. Do not log the object body. See [audit logs](../compliance/audit-logs.md).
- Migrate from a role table by representing the old roles as tuples (`user` member of `role`, `role` granted `permission`) and running both checks. Compare denies in production traffic before you delete the old `if role == admin` branch. Cut over one action at a time.

## Checklist

- [ ] Default deny when the engine is down, for any action you cannot safely serve from a cache.
- [ ] A removal is visible to the next privileged check within a bound you have written down.
- [ ] The list endpoint and the point read use the same model version.
- [ ] Tuple writes from SCIM and from the app are idempotent on the same key.
- [ ] Decision logs are enough to explain a deny without a debugger.
- [ ] The old role check and the engine agree on a recorded sample before the old check is removed.

## Anti-patterns

- A Zanzibar service for a three-role admin console.
- Check on write, and a list that returns every row the database has.
- Two engines, one in the gateway and one in the service, with different tuples.
- Editing relationships in the engine's UI so they drift from the product database.
- A five-minute cache of "user is owner" on the export endpoint.

## Related

- [Zero trust](../security/zero-trust.md) for why the network is not the decision.
- [OIDC and OAuth 2.0](oidc-oauth2.md) for the subject the engine is allowed to believe.

## Further reading

- [Zanzibar, USENIX ATC 2019](https://www.usenix.org/conference/atc19/presentation/pang) ([paper PDF](https://www.usenix.org/system/files/atc19-pang.pdf))
- [OpenFGA](https://openfga.dev/) and the [CNCF project page](https://www.cncf.io/projects/openfga/)
- [SpiceDB](https://github.com/authzed/spicedb)
- [Cedar](https://cedarpolicy.com/), [cedar-policy on GitHub](https://github.com/cedar-policy/cedar), [Amazon Verified Permissions](https://aws.amazon.com/verified-permissions/)
- [Open Policy Agent](https://www.openpolicyagent.org/) and the [CNCF project page](https://www.cncf.io/projects/open-policy-agent-opa/)
