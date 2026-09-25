---
title: "Schema evolution"
summary: "Change events and tables so old and new producers and consumers overlap for at least one release."
tags: [data, schema, compatibility]
when_to_use: "Use when a stored record, an event, or an API payload will change and more than one deployable reads or writes it."
related:
  - event-driven.md
  - cdc.md
  - ../apis/versioning.md
  - ../delivery/database-migrations.md
  - ../../patterns/cdc.md
---

# Schema evolution

A schema change is a deployment problem. For one release, the previous binary and the new binary both exist. Both must read what the other writes, or you have ordered the rollout so that only a compatible direction happens. The database version of this rule is [expand/contract](../delivery/database-migrations.md).

## Compatibility

| Rule | Meaning | Typical change |
|---|---|---|
| Backward compatible | New code reads old data | Add an optional field. New consumer tolerates its absence |
| Forward compatible | Old code reads new data | Old consumer ignores an unknown field. Do not reuse a removed field's tag or column meaning |
| Full | Both directions | Optional additive changes only, during the overlap |
| Breaking | Not safe to mix | Remove or rename, change a type, or narrow an enum. Requires a version bump and a migration window |

## Defaults

- Protobuf and similar numeric tags: never reuse a field number. Reserve removed numbers. Avro and JSON schemas need an explicit compatibility check in CI.
- Add fields as optional with a documented default. Consumers treat missing as the default.
- Prefer a new event type or a new major version over mutating the meaning of an existing field.
- A registry (or a checked-in schema with a compatibility gate) rejects incompatible changes before they ship.
- Expand/contract for databases: add the new column, dual-write, backfill, switch readers, stop the old write, drop the old column later. Never rename in place in one deploy.
- CDC consumers see the database's schema. Coordinate column changes with connector and warehouse owners. A renamed column is a broken pipeline, not a refactor.
- Version is explicit on events (`schema_version` or the registry id), so a consumer can branch or dead-letter an unknown version.

## Checklist

- [ ] CI fails a pull request that breaks the declared compatibility level.
- [ ] Rollback of the app is possible while the new column still exists (expand is backward compatible; drop is not).
- [ ] Replay of a year-old event still has a reader, or you have a documented cutoff.
- [ ] Defaults are safe. "Missing boolean means true" is how a permission opens up.

## Anti-patterns

- Shipping a renamed JSON field because "we deploy the producer and consumer together." You will not, the moment one of them rolls back.
- Overloading a string field with a new format.
- A database migration that locks and rewrites a hot table inside the API deploy.
- Topic reuse for an unrelated event because the name was convenient.
