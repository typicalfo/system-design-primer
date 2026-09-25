---
title: "OWASP ASVS chapter map"
summary: "Point a design at the ASVS 5.0.0 chapter that covers the control, without copying the standard's requirement text."
tags: [security, asvs, owasp]
when_to_use: "Use when a review or a design must name the security control area for an API, token, session, or data store."
related:
  - threat-modeling.md
  - zero-trust.md
  - encryption-keys.md
  - ../identity/oidc-oauth2.md
  - ../identity/authorization-models.md
  - ../compliance/audit-logs.md
  - ../../pack/skills/design-reviewer/checklist.md
  - ../../pack/corpora/INDEX.md
---

# OWASP ASVS chapter map

The Application Security Verification Standard is a catalog of security requirements for web apps and web services. This repo uses version 5.0.0 (May 2025) as the chapter map. The project content is CC BY-SA 4.0, as stated in the ASVS repository README. This page names chapters. It does not copy requirement sentences. The license check and the links live in [pack/corpora/INDEX.md](../../pack/corpora/INDEX.md).

Standard: <https://owasp.org/www-project-application-security-verification-standard/>
English PDF for 5.0.0: <https://github.com/OWASP/ASVS/raw/v5.0.0/5.0/OWASP_Application_Security_Verification_Standard_5.0.0_en.pdf>

When a finding needs the exact requirement sentence, say it was not verified here and follow that link.

## Chapter map

| If the design decides… | ASVS 5.0.0 chapter |
|---|---|
| Encoding, injection, output in the right context | V1 Encoding and Sanitization |
| Input validation and business rules | V2 Validation and Business Logic |
| Browser app, cookies, frontend sinks | V3 Web Frontend Security |
| HTTP or RPC API shape, auth on each operation | V4 API and Web Service |
| Uploads, exports, archives | V5 File Handling |
| Passwords, MFA, credential storage | V6 Authentication |
| Session cookies and server-side sessions | V7 Session Management |
| Access control, tenant isolation, function-level checks | V8 Authorization |
| JWTs and other self-contained tokens | V9 Self-contained Tokens |
| OAuth 2.0 and OpenID Connect | V10 OAuth and OIDC |
| Hashing, encryption, key handling, signatures | V11 Cryptography |
| TLS and internal encrypted transport | V12 Secure Communication |
| Secrets, hardening, default-deny config | V13 Configuration |
| Classification, retention, deletion, privacy | V14 Data Protection |
| Dependencies and architecture-level secure design | V15 Secure Coding and Architecture |
| Security logs, audit logs, errors that leak internals | V16 Security Logging and Error Handling |
| Realtime media, only if the design carries it | V17 WebRTC |

The same map is the checklist the design reviewer walks: [checklist.md](../../pack/skills/design-reviewer/checklist.md).

## Defaults

- Cite a chapter in a review finding. Do not invent `V#.#.#` requirement ids.
- Internal systems still meet the floor: TLS in transit, encryption at rest, parameterized data access, least privilege on stores, no secrets in the design doc or the image.
- Pick the chapter for the control you are discussing. A missing tenant check is V8, even if the transport is TLS (V12) and already fine.
- ASVS is a requirements list, not a threat model. Use [STRIDE](threat-modeling.md) to find the abuse, then point at the chapter that should have prevented it.

## Anti-patterns

- Pasting ASVS requirement text into this repository. The license allows reuse only if the copy stays under CC BY-SA 4.0 with attribution. This fork links.
- Claiming "ASVS level 2 compliant" without an assessment against the standard itself.
- Treating the OWASP Top 10 as a substitute for a verification standard. Top 10 is a priority list of risk categories; ASVS is the requirement catalog.
