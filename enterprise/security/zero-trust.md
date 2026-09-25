---
title: "Zero trust"
summary: "Authenticate and authorize every request, and treat network location as an untrusted hint."
tags: [security, zero-trust, identity]
when_to_use: "Use when you are deciding whether a private network, a VPN, or a security group is enough of a control for an internal system."
related:
  - threat-modeling.md
  - owasp-asvs.md
  - ../identity/service-to-service.md
  - ../identity/authorization-models.md
  - ../tenancy/isolation-models.md
  - ../../patterns/sidecar-service-mesh.md
last_reviewed: 2026-09-25
---

# Zero trust

Zero trust means a request is allowed because of the caller's identity, the device or workload posture you checked, and a policy on that resource. It is not allowed because the packet arrived from a "trusted" subnet.

The idea is widely documented, including [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final). This page does not copy that publication. It states the engineering defaults.

## Decide

| Choose | Use when | Avoid when |
|---|---|---|
| Identity on every hop | Callers are users, jobs, or services, including "internal" ones | The hop is a tightly coupled in-process function call with no network |
| Least privilege per workload | A service needs a small set of methods on one dependency | You are about to grant the whole data store to every service "so we can ship" |
| Segment by sensitivity | Card data, PHI, admin planes, or a large tenant must be reachable by few identities | You segment only by team name and every team can still reach every store |
| Continuous check of device or workload | The user path is a browser on an unmanaged laptop, or the cluster mixes tenants | You have no signal to check. A fake posture header is worse than a declared gap |
| VPN as the only control | Never as the only control | The resource is sensitive. A VPN proves the laptop joined a network, not that this user may export this tenant |

## Defaults

- No implicit trust for east-west traffic. Service A authenticates to service B.
- Admin access is separate: short-lived, named humans, multi-factor, audited, no shared break-glass password.
- Production data stores have no path from developer laptops except through a brokered, logged query path.
- Policy is default deny at the application. Security groups are a second layer, not the authorization model.
- Assume a single workload will be compromised. Its identity should not be able to list every tenant or mint tokens for other services.
- Encrypt on the path even inside the VPC. The threat includes a hostile or misconfigured neighbor.

## Checklist

- [ ] You can name, for the most sensitive store, every identity that can read it.
- [ ] Removing a person from the IdP removes their production access without waiting for a VPN cert to expire months later.
- [ ] A stolen service credential has a blast radius you have written down.
- [ ] "Internal" debug endpoints are authenticated or not routed.

## Anti-patterns

- A flat production network plus a wiki page that says "zero trust."
- Mutual TLS in permissive mode.
- Trusting an internal header (`X-User-Id`) that any pod can set.
- One shared admin role for all on-call across all products.

## Further reading

- [NIST SP 800-207, Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
