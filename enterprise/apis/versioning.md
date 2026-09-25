---
title: "API versioning"
summary: "Evolve contracts compatibly, and introduce an explicit version only when a break is unavoidable."
tags: [api, versioning, compatibility]
when_to_use: "Use when a caller you do not deploy in lockstep depends on an API or an event."
related:
  - styles.md
  - contract-testing.md
  - ../data/schema-evolution.md
  - ../delivery/database-migrations.md
---

# API versioning

A version is a promise that some callers still need the old behavior. If you deploy the only client yourself, you can change the API and the client in one release train and skip the ceremony. The moment a mobile app, a customer integration, or another team lags, you need a compatibility rule.

## Defaults

- Additive changes are not a new version: new optional JSON fields, new endpoints, new enum values the server accepts but old clients do not have to send.
- Old clients must ignore unknown fields. Do not require clients to fail closed on a new field unless you enjoy coordinated releases.
- Breaking changes (remove a field, change a type, change an error code's meaning, tighten validation) ship as a new version or behind a negotiated media type.
- Prefer one or two live versions, not ten. A version has a published sunset date and a usage metric. Turning it off is a decision with a number, not a hope.
- URL prefixes (`/v1`) are easy to route and easy to leave forever. Use them when the break is large. Header or media-type versioning fits callers who already pin headers. Pick one scheme per API.
- Deprecation is a signal in the response (for example a `Sunset` header or a documented field) plus a notice to the owners of the credentials still calling the old version.
- Internal gRPC packages version on breaking protobuf changes. Do not overload field numbers.
- Events version the same way. See [schema evolution](../data/schema-evolution.md).

## Decide

| Change | Version bump? |
|---|---|
| Add an optional response field | No |
| Add a required request field | Yes, unless you default it and old callers still succeed |
| Change a default that affects money or permissions | Yes. Treat it as breaking |
| Fix a bug that clients silently depend on | Maybe. If a customer integration will break, it is a break even if the old behavior was wrong |
| New resource | No |

## Checklist

- [ ] You can list callers of the oldest version.
- [ ] Contract tests cover the versions you still claim to support. See [contract testing](contract-testing.md).
- [ ] Sunset dates are visible to API consumers.
- [ ] A rollback of the server does not strand clients that already depend on a new required behavior, or you do not roll the server back past that point.

## Anti-patterns

- A new `/v2` for every sprint, with `/v1` unmaintained but still routed.
- Versioning the entire platform because one endpoint changed.
- "Versionless" APIs that break mobile clients who cannot refresh today.
- Encoding the version only in documentation, not in the route, the package, or the schema id, so nobody can see what is live.
