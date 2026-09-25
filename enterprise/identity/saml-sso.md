---
title: "SSO and SAML"
summary: "Accept enterprise single sign-on through SAML 2.0 when a customer IdP requires it, and keep the assertion checks strict."
tags: [identity, saml, sso, authentication]
when_to_use: "Use when a customer's identity provider can only speak SAML, or when you are the identity provider for a partner that requires SAML."
related:
  - oidc-oauth2.md
  - authorization-models.md
  - ../tenancy/lifecycle.md
  - ../security/owasp-asvs.md
last_reviewed: 2026-09-25
---

# SSO and SAML

Single sign-on means the user authenticates once at an identity provider (IdP) and your app, the service provider (SP), trusts the result. New products should prefer OIDC. SAML 2.0 remains the protocol many corporate IdPs still require.

## Decide

| Choose | Use when | Avoid when |
|---|---|---|
| OIDC for SSO | The customer IdP supports it, or the users are yours | A named enterprise customer contractually requires SAML |
| SAML SP-initiated | The user starts at your app and you redirect to their IdP | You do not need the user to land on a specific tenant URL first |
| SAML IdP-initiated | The customer launches your app from their portal | You can require SP-initiated. IdP-initiated responses are easier to replay into the wrong session if you skip `InResponseTo` |
| Per-tenant IdP | Each customer brings Okta, Entra ID, ADFS, or similar | Tenants are small and you would rather own passwords. Owning passwords is the larger burden |

## Defaults

- One SAML connection per tenant. Issuer, certificate, ACS URL, and audience are tenant-scoped.
- Require signed assertions. Prefer signed responses as well. Reject unsigned, and reject assertions signed with SHA-1.
- Check audience, recipient, destination, `NotBefore` / `NotOnOrAfter` with a small clock skew (a minute or two), and one-time use of the assertion id.
- Bind the response to the request you sent (`InResponseTo`) for SP-initiated flows.
- Pin the IdP signing certificate. Rotate by accepting two certs during overlap, then dropping the old one.
- Map the assertion to a local user on a stable immutable id (`NameID` or a agreed attribute), not on an email address that the customer can reassign without telling you. Email can change; the stable id should not.
- Provision with just-in-time creation only if the tenant admin has allowed that domain. Otherwise require SCIM or an explicit invite.
- Disable XML external entities on every parser that touches metadata or assertions. Metadata is an XML document from outside your trust boundary.

## Checklist

- [ ] ACS URL is exact and tenant-specific, or the tenant is derived from a checked assertion field, not from a query parameter the caller can edit.
- [ ] A stolen assertion cannot be replayed after the validity window.
- [ ] Tenant A's certificate does not validate tenant B's assertion.
- [ ] Turning off SSO for a tenant has an immediate effect on new logins.
- [ ] You have a tested break-glass path for your own operators that does not share the customer's IdP.

## Anti-patterns

- "If the XML parses, the user is in."
- Trusting a self-signed assertion because the metadata URL was fetched once over plain HTTP.
- Using the email attribute as the primary key and letting it silently move a user across tenants.
- Building a new SAML stack when the customer can enable OIDC on the same IdP.

## Related reading

Browser session lifetime after SAML is your session, not the assertion lifetime. Session rules belong with ASVS V7. See [OIDC and OAuth 2.0](oidc-oauth2.md) for the protocol to offer first.
