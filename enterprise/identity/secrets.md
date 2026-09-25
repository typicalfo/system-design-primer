---
title: "Secrets management"
summary: "Keep secrets in a manager, inject them at runtime, scope who can read them, and rotate them without a redeploy heroics story."
tags: [identity, secrets, security]
when_to_use: "Use when a workload needs a credential, key, or token that must not appear in source, images, or logs."
related:
  - service-to-service.md
  - oidc-oauth2.md
  - ../security/encryption-keys.md
  - ../security/supply-chain.md
  - ../delivery/iac-environments.md
  - ../compliance/audit-logs.md
---

# Secrets management

A secret is anything that grants access or decrypts data: passwords, API tokens, private keys, connection strings, webhook signing keys. Configuration that is not sensitive does not belong in the same store, or the store becomes a junk drawer with production access.

## Decide

| Choose | Use when | Avoid when |
|---|---|---|
| Runtime injection from a secret manager | The workload can fetch, or the platform can mount, a secret at start or refresh | You are tempted to bake the value into the image "so it starts offline" |
| Dynamic database credentials | The database can issue a short-lived user bound to the workload identity | The database client cannot refresh, or the operational cost exceeds the leak window you actually have |
| Envelope encryption with a KMS key | You need to store ciphertext (tokens at rest, backups) and the key must not sit next to the data | You only needed TLS. See [encryption and keys](../security/encryption-keys.md) |
| Sealed secret in git | A small platform team needs a reviewable ciphertext in the deploy repo and the controller unseals it | Several teams will copy the unsealed value into their own pipelines |
| `.env` in the repo, CI variables copied into the image | Never for production | Always for production |

## Defaults

- One secret per purpose, per environment. Production and staging do not share a database password.
- Access policy is the workload identity, not a human's standing admin role. Humans use break-glass that is audited.
- Mount or fetch at start. Refresh before expiry for leased secrets. Crash if the secret is missing; do not fall back to a default password.
- Rotation is a procedure you have run: add new, deploy or reload consumers, revoke old. Dual-accept during the overlap.
- Logs, traces, and exception reporters redact `Authorization`, cookies, connection strings, and private keys.
- CI jobs that need a secret use the platform's OIDC federation into the cloud account. The long-lived CI token is the thing you are trying to eliminate.
- Reading a secret is an audit event for high-value keys (payment, SSO signing, root database).

## Checklist

- [ ] A search of the repo and the image history does not find production secrets.
- [ ] Revoking one leaked secret does not require editing source.
- [ ] Developers cannot read production secrets with their everyday credentials.
- [ ] Backup of the secret store is separate from backup of the data those secrets open, and both restores are tested.
- [ ] A leaked secret has an owner and a rotation path written down.

## Anti-patterns

- Encrypting a secret with a key that is in the same repository.
- "Kubernetes Secret" as the only control. It is base64 plus etcd encryption you must turn on. It is not a full manager unless you add policy, audit, and rotation.
- Sharing one cloud key across CI, the app, and a contractor's laptop.
- Printing the secret manager's response in a debug build that is the production build.
