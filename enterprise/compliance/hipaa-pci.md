---
title: "HIPAA and PCI DSS basics"
summary: "Shrink the systems that touch PHI or cardholder data, and put the extra controls only on what remains."
tags: [compliance, hipaa, pci, security]
when_to_use: "Use when a design might store or transmit protected health information or payment card data and you need the architectural consequences."
related:
  - privacy.md
  - audit-logs.md
  - residency.md
  - ../security/encryption-keys.md
  - ../security/zero-trust.md
  - ../tenancy/isolation-models.md
last_reviewed: 2026-09-25
---

# HIPAA and PCI DSS basics

This page is engineering scope control, not legal advice and not an attestation. HIPAA applies to protected health information (PHI) handled by covered entities and their business associates in the United States. PCI DSS applies to systems that store, process, or transmit cardholder data, and to connected systems that can affect their security. If you are unsure whether you are in scope, stop and ask counsel or the compliance owner before inventing a lighter design.

## Defaults for PHI

- Sign a business associate agreement before any PHI flows. A product decision, not a footer.
- Define the minimum data the feature needs. Do not send the whole chart to a logging vendor.
- Access is per user, audited, and limited to the people and services that perform the function.
- Encrypt in transit and at rest. Treat encryption as expected, and still authorize every read.
- Audit access to PHI, not only changes. "Who viewed this record" is often the question.
- Do not put PHI in tickets, chat, metrics labels, or exception text.
- A breach assessment needs to know which records were exposed. Immutable access logs make that possible.
- Prefer a silo or a separate account for workloads that handle PHI if the rest of the platform does not.

## Defaults for card data

- The cheapest compliant architecture is to keep cardholder data out of your systems. Use a payment provider's hosted fields, checkout, or tokenization so your servers see a token, not a PAN.
- Never store the CVV, even encrypted. Do not log it on the way to the provider.
- If a PAN must exist in your boundary, segment that environment. Systems that can initiate a connection into it are in scope too. Scope spreads through flat networks.
- Keys for card data live in a KMS or HSM, with split duties. Application logs do not contain the PAN. Truncate or tokenize at the edge of the zone.
- Quarterly scanning, access control, and logging requirements attach to the in-scope zone. The way to make them affordable is to make the zone small.

## Decide

| Integration | Typical scope | Prefer |
|---|---|---|
| Provider-hosted payment page or fields, you store a token | Your app is usually out of PAN scope if the integration really never sees the PAN. Confirm the SAQ with the provider and the acquirer | Yes for new payments |
| PAN posted to your API and forwarded | Your API, logs, and anything downstream that might retain the body are in scope | Avoid |
| Analytics on "payment succeeded" with amount and your order id | Usually not cardholder data if no PAN, track, or CVV | Fine |
| Clinical notes in the same database as the marketing site | The marketing site's bugs become PHI incidents | Split the stores |

## Checklist

- [ ] A diagram shows where PHI or PAN is allowed to exist, including vendors.
- [ ] Log and trace configuration drops those fields.
- [ ] Production access to that zone is named, multi-factor, and audited.
- [ ] Tokens are useless outside the provider that minted them.
- [ ] A test transaction proves the PAN does not land in your database or your log index.

## Anti-patterns

- Emailing a spreadsheet of claim details to "move faster."
- Storing the full card "just in case the charge fails" and retrying from your database.
- One shared production database for the healthcare feature and the rest of the SaaS.
- Copying the in-scope database into an unscanned analytics account.
