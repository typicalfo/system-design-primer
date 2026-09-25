---
title: "Encryption and key management"
summary: "Encrypt in transit and at rest with managed keys, separate data keys from key-encryption keys, and do not invent a cipher."
tags: [security, encryption, kms, cryptography]
when_to_use: "Use when data moves across a network or sits on disk, in a backup, or in a queue, and you must decide who can read it."
related:
  - supply-chain.md
  - owasp-asvs.md
  - ../identity/secrets.md
  - ../tenancy/data-and-keys.md
  - ../compliance/residency.md
  - ../compliance/retention.md
---

# Encryption and key management

Encryption reduces who can read bytes. It does not replace authorization. A database role that can `SELECT` the plaintext column has already passed the control encryption was supposed to provide, unless the application encrypts before the database sees plaintext.

ASVS 5.0.0 chapters V11 Cryptography and V12 Secure Communication are the review map. Do not copy requirement text; see [OWASP ASVS](owasp-asvs.md).

## Decide

| Choose | Use when | Avoid when |
|---|---|---|
| TLS 1.2 or later, prefer 1.3 | Any hop that leaves a process, including inside the VPC | You terminate TLS at the edge and then talk cleartext across a shared network you do not fully control, without a reason |
| Provider encryption at rest with a customer-managed key | Disks, buckets, and volumes should be unreadable if the media escapes, and you want a key you can disable | You need the database administrator to be unable to read a column. Disk encryption does not do that |
| Application-level encryption (envelope) | A column, file, or backup must stay opaque to the store's admins, or each tenant must have a key you can destroy | You only needed "encrypted at rest" on a questionnaire and the provider already encrypts disks |
| Per-tenant key | Contract or blast-radius requires destroying one tenant's key without touching others | You have thousands of tiny tenants and no lifecycle for that many keys. Use a smaller set of keys plus strict auth, and say so |
| Hashing for passwords | You store a password verifier | You need to recover the password. You should not need to |

## Defaults

- Use an authenticated cipher the platform already provides (AES-GCM or ChaCha20-Poly1305). Do not design a mode, an IV scheme, or a password hash.
- Envelope encryption: a data-encryption key (DEK) encrypts the payload. A key-encryption key (KEK) in a KMS or HSM wraps the DEK. Store the wrapped DEK next to the ciphertext.
- Rotate DEKs by writing new data under a new DEK. Re-wrap DEKs when you rotate the KEK. Do not confuse the two.
- Bind associated data (tenant id, record id) into the AEAD tag so ciphertext cannot be swapped across tenants.
- Passwords and other verifiers: Argon2id, bcrypt, or scrypt with a unique salt. Never SHA-1, SHA-256, or a single unsalted hash.
- Keys do not enter logs, traces, or source. Access to use a KEK is an audit event.
- Disabling a key is a kill switch. Know what breaks (login, backups, one tenant) before you offer it as a control.
- TLS certificates are automated and short-lived. Alert on expiry with enough time to renew, and fail closed on invalid certificates. Do not disable verification in clients.

## Checklist

- [ ] You can point at the component that sees plaintext for each sensitive store.
- [ ] Backups are encrypted, and the key to open them is not inside the same backup blob unprotected.
- [ ] A restore drill has opened a backup with the key-management path, not with a copy of the key in a ticket.
- [ ] Ciphertext is tenant-bound where tenants share a store.
- [ ] You have a written path to crypto-shred a tenant or a person by destroying the DEK, if that is your deletion story. See [retention](../compliance/retention.md).

## Anti-patterns

- ECB mode, homemade XOR, or "encrypt then forget the IV."
- A single application-wide AES key checked into the deploy config.
- Hashing passwords with a fast hash and calling it encryption.
- Claiming field-level encryption while logging the same field at `INFO`.
- Using encryption at rest as the answer to a missing tenant filter in the query.
