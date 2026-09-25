---
title: "Post-quantum migration"
summary: "Inventory where classical public-key crypto protects long-lived data, prefer hybrid key agreement first, and treat NIST's 2030 and 2035 dates as a draft timeline until IR 8547 is final."
tags: [security, cryptography, post-quantum, tls, pki]
when_to_use: "Use when you are deciding what to inventory, what to migrate first, and which NIST and IETF documents are final."
related:
  - encryption-keys.md
  - supply-chain.md
  - ../compliance/iso27001-fedramp.md
  - ../identity/secrets.md
last_reviewed: 2026-09-25
---

# Post-quantum migration

A cryptographically relevant quantum computer would break today's widely deployed public-key algorithms (RSA and elliptic-curve Diffie-Hellman and signatures). Symmetric encryption and hashes need larger parameters, not a new family, for the same threat. The operational problem now is harvest-now-decrypt-later: an attacker records ciphertext today and decrypts it later. That hits data whose confidentiality must outlast the migration (TLS sessions that protect long-lived secrets, backups, archives, stored keys wrapped under a public key). A signature on a short-lived handshake is a different deadline. Signatures matter sooner when the signature must stay valid for years (firmware, documents, certificate chains) or when a forged signature would be accepted after the break.

Do not invent a post-quantum scheme. Use the standards below, and keep a way to change algorithms. See [encryption and keys](encryption-keys.md).

## Decide

| Choose | Use when | Avoid when |
|---|---|---|
| Hybrid key agreement in TLS (classical ECDH plus ML-KEM) | You need confidentiality against harvest-now-decrypt-later and you still want the classical algorithm if the new one fails | The peer has no hybrid group. Forcing it will break the handshake. Offer it, measure it, then require it |
| ML-KEM alone | Both ends are yours, you have tested the implementation, and hybrid is no longer buying you a fallback | You are wrapping a public protocol that clients have not moved |
| ML-DSA for new signatures | You control both signer and verifier and can carry the larger signatures | A certificate authority, a device, or a protocol in the path still only understands ECDSA. Test that path before you cut |
| SLH-DSA | You want a stateless hash-based signature as a backup with different math, and you can afford the size and the signing cost | You need the smallest, fastest signature. SLH-DSA is not the default general-purpose signature |
| Waiting for a finished FIPS 206 or an HQC standard | You are choosing a second signature or a backup KEM and the document is not final | You use the wait as a reason to skip hybrid key agreement. ML-KEM is already a final FIPS |

## What is final, and what is not

Final, published 13 August 2024, per NIST's [announcement](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) and the [CSRC PQC publications list](https://csrc.nist.gov/projects/post-quantum-cryptography/publications):

- [FIPS 203](https://csrc.nist.gov/pubs/fips/203/final), ML-KEM, the primary key-encapsulation mechanism.
- [FIPS 204](https://csrc.nist.gov/pubs/fips/204/final), ML-DSA, the primary lattice signature.
- [FIPS 205](https://csrc.nist.gov/pubs/fips/205/final), SLH-DSA, the stateless hash-based signature.

Not final, as of that publications list (page updated 5 August 2026; re-check before you claim a standard):

- FN-DSA, the FALCON-derived signature NIST intends to publish as FIPS 206. FIPS 206 does not appear on that list as a draft or a final publication. A [NIST talk on 25 September 2025](https://csrc.nist.gov/presentations/2025/fips-206-fn-dsa-falcon) described an initial public draft as forthcoming. Do not treat FN-DSA as a finished FIPS.
- HQC. NIST [selected HQC on 11 March 2025](https://www.nist.gov/news-events/news/2025/03/nist-selects-hqc-fifth-algorithm-post-quantum-encryption) as a backup key-encapsulation mechanism on different math from ML-KEM. [IR 8545](https://csrc.nist.gov/pubs/ir/8545/final) is the selection report. Selection is not a published FIPS.

[NIST IR 8547](https://csrc.nist.gov/pubs/ir/8547/ipd), *Transition to Post-Quantum Cryptography Standards*, is an initial public draft (12 November 2024). The same publications list still marks it Draft. It is not a FIPS. In the draft tables, classical signature and key-establishment schemes at the 112-bit security strength (including RSA, ECDSA, and finite-field and elliptic-curve Diffie-Hellman at that strength) are deprecated after 2030 and disallowed after 2035. Parameters at 128 bits of classical security and above, including EdDSA, are marked disallowed after 2035. Plan against those dates, and read the final report when NIST publishes one. The draft is a transition proposal, not by itself a procurement mandate.

## Defaults

- Inventory first. A cryptographic bill of materials lists algorithms, key sizes, protocols, libraries, certificate lifetimes, and where ciphertext or signatures are stored. You cannot prioritize what you have not listed. Keep it next to the software bill of materials. See [supply chain](supply-chain.md).
- Crypto agility means the protocol and the code can change the KEM or the signature without a flag day you cannot rehearse. Prefer an existing TLS stack's named groups over a private hybrid.
- Migrate key establishment before signatures when the asset is long-lived confidentiality. Recorded TLS and stored public-key wraps are the harvest-now-decrypt-later case. Signature cutover follows once verifiers, CAs, and devices accept the new algorithm and the larger objects.
- Hybrid TLS 1.3 key agreement is specified in [RFC 10024](https://www.rfc-editor.org/rfc/rfc10024) (August 2026, Standards Track). It defines `X25519MLKEM768` (supported-group value 4588, Recommended: Y), `SecP256r1MLKEM768`, and `SecP384r1MLKEM1024`. Confirm the group in the TLS libraries and the clients you actually run. A standard does not mean every installed browser or appliance offers it.
- Certificates get larger, and so do handshakes and anything that stores a chain. HSM and token firmware may need an update before they will hold or sign with the new keys. Test a full issuance and a full verification, including intermediates, before you announce a cutover date.
- Performance is part of the design. ML-KEM public keys and ciphertexts are much larger than a 32-byte X25519 share. ML-DSA signatures are larger than ECDSA signatures. SLH-DSA signatures are larger still, and signing is slower, which is why it is a backup rather than the default. Measure on your path. Do not copy a byte count from a blog into a capacity plan without checking the parameter set in the FIPS.
- Federal and regulated buyers may point at FIPS 140 validation of the module, not only at the algorithm name. Track validation separately from "the library implements ML-KEM." See [ISO 27001 and FedRAMP](../compliance/iso27001-fedramp.md) for how that shows up in an authorization boundary.

## Checklist

- [ ] You can list the places a public key protects data that must stay secret past 2035.
- [ ] TLS hybrids are measured on the clients you support, including the ones that will not offer the group.
- [ ] Certificate issuance, storage, and MTU or token limits have been tried with the new sizes.
- [ ] The inventory names the library and the parameter set, not only the word "post-quantum."
- [ ] Someone re-reads IR 8547's status before a compliance claim quotes 2030 or 2035 as a finished NIST rule.

## Anti-patterns

- A slide that says "quantum safe" because one internal service speaks ML-KEM and the public edge does not.
- Disabling classical key agreement before clients can negotiate the hybrid, and calling the outage a migration.
- Adopting an unstandardized "quantum" product that is not FIPS 203, 204, or 205.
- Treating FN-DSA or HQC as required algorithms before NIST finishes those documents.
- Ignoring signatures on firmware because the memo said "key exchange first," when that firmware must still verify in ten years.

## Related

- [Encryption and keys](encryption-keys.md)
- [Secrets](../identity/secrets.md)

## Further reading

- [FIPS 203](https://csrc.nist.gov/pubs/fips/203/final), [FIPS 204](https://csrc.nist.gov/pubs/fips/204/final), [FIPS 205](https://csrc.nist.gov/pubs/fips/205/final)
- [NIST IR 8547 initial public draft](https://csrc.nist.gov/pubs/ir/8547/ipd) and the [PQC publications list](https://csrc.nist.gov/projects/post-quantum-cryptography/publications)
- [NIST HQC selection, 11 March 2025](https://www.nist.gov/news-events/news/2025/03/nist-selects-hqc-fifth-algorithm-post-quantum-encryption)
- [RFC 10024, hybrid key agreement for TLS 1.3](https://www.rfc-editor.org/rfc/rfc10024)
