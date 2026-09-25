---
title: "Service-to-service auth"
summary: "Give every workload an identity and a short-lived credential, using workload identity, SPIFFE, or mutually authenticated TLS."
tags: [identity, mtls, spiffe, workload-identity, service-mesh]
when_to_use: "Use when one service, job, or pipeline calls another and no human is in the request."
related:
  - oidc-oauth2.md
  - secrets.md
  - authorization-models.md
  - ../security/zero-trust.md
  - ../security/supply-chain.md
  - ../../patterns/sidecar-service-mesh.md
last_reviewed: 2026-09-25
---

# Service-to-service auth

A workload is a caller. It needs a name the callee can check, and a credential that expires. Network location ("it came from the VPC") is not a name.

## Decide

| Choose | Use when | Avoid when |
|---|---|---|
| Cloud workload identity | The workload runs on a cloud that can mint short-lived tokens from an instance or service account | The caller and callee sit in unrelated trust domains with no federation |
| [SPIFFE](https://spiffe.io/) / SPIRE | You want a stable workload id (`spiffe://trust-domain/ns/sa`) across clusters or clouds, issued as an X.509-SVID or JWT-SVID | You have one cluster and the platform identity already answers the question |
| Mutual TLS | You need encryption and authentication at the connection, often terminated by a mesh sidecar | You only needed application-level authorization and TLS is already terminated elsewhere. mTLS without a name check is just encryption |
| OAuth client credentials | A partner or a non-mesh job must call an HTTP API you already protect with an authorization server | Both sides are your workloads and a platform identity exists. A second static client secret is a step backward |
| Static API key or long-lived cert on disk | Almost never | You can issue a short-lived credential. Static keys leak into images, tickets, and logs |

## Defaults

- Identity is the workload (service account, SPIFFE ID), not the host, and not a shared "backend" key used by every service.
- Credentials last minutes to hours. The platform renews them. Applications do not embed them in images.
- Callees check the peer identity and the permission. "Presents any cert from our CA" is too wide.
- Internal admin ports (metrics, debug) require the same identity or they are not routed. Scrape jobs get their own identity.
- Rotate trust bundles. A CA compromise plan exists: which issuers are live, how fast you can stop trusting one.
- Cross-region and cross-account calls use the same identity story. A private link is transport, not authentication.
- Log the peer id on writes. Do not log the raw token or the private key path.

## Checklist

- [ ] No production secret is a long-lived cloud access key checked into env files.
- [ ] Each service has a distinct identity. Compromise of one does not equal compromise of all.
- [ ] The authorization check uses that identity (payments may call ledger; the web app may not call ledger's admin method).
- [ ] Certificate or token expiry is monitored before it becomes an outage.
- [ ] Local development uses a scoped stand-in, not a copy of production credentials.

## Anti-patterns

- A mesh that injects sidecars but runs in permissive mode, so missing identity still works.
- mTLS to the sidecar and then plain HTTP to the app with the peer identity dropped on the floor.
- One Kubernetes `cluster-admin` binding used by CI "temporarily."
- Trusting the `X-Forwarded-Client-Cert` header from any caller, not only from the proxy you control.

## Further reading

- [SPIFFE](https://spiffe.io/)
