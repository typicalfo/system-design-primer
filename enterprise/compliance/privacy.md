---
title: "GDPR and CCPA basics"
summary: "Inventory personal data, minimize it, and build export and deletion as product paths rather than as tickets."
tags: [compliance, privacy, gdpr, ccpa]
when_to_use: "Use when the system stores information about people, including customer employees, and you need the engineering consequences of privacy law."
related:
  - retention.md
  - residency.md
  - audit-logs.md
  - soc2.md
  - ../tenancy/lifecycle.md
  - ../data/governance.md
---

# GDPR and CCPA basics

GDPR (EU/UK) and CCPA/CPRA (California) are legal regimes. This page is not legal advice. It lists the engineering capabilities teams are usually expected to have when they process personal data. Counsel decides lawful basis, whether you are a controller or a processor, and which requests are valid. Engineering makes those decisions executable.

Personal data includes more than a name. Identifiers, online identifiers, and data that can be linked to a person count. In a B2B product, the customer's employees are still people.

## Defaults

- Keep a data inventory: what you collect, why, where it is stored (including logs, warehouses, support tools, and backups), and how long it lives.
- Minimize. Do not copy the production row into analytics, crash reports, or a third-party session-replay tool without a reason and a retention limit.
- Separate processor duties (you act on the customer's instructions, often under a DPA) from controller duties (you decide why you process, for example your own marketing site).
- Support export and deletion of a person's data inside a tenant. The customer admin often submits the request. Your workflow still has to find the copies.
- Record the request and the outcome. Do not put the person's payload into the audit record you keep forever.
- Subprocessors are listed and contracted. A new SaaS tool that receives personal data is a vendor review, not a developer convenience.
- CCPA-style "do not sell or share" and GDPR-style consent are product and legal questions. If the site uses advertising or cross-context tracking, engineering needs a flag that actually stops the downstream calls.
- Data about EU residents may need to stay in a chosen region. See [residency](residency.md).

## Decide

| Request | Build | Do not build |
|---|---|---|
| Access or export | A job that collects that person's fields from each system of record and delivers them to the tenant admin | A raw database dump of the whole tenant emailed to whoever asked |
| Deletion | Delete or irreversibly anonymize the person in primary stores, indexes, and vendors, subject to an allowed exception | A flag `deleted=true` that every reader remembers to check, with the payload left in place |
| Exception | Legal hold, security logs, invoices you must keep. The exception is a field and a date, not a reason to keep everything | Keeping all logs forever "in case legal wants them" |

## Checklist

- [ ] You can list every store that receives a new user profile field before you add the field.
- [ ] Crash and trace pipelines scrub emails, names, and tokens.
- [ ] A tested deletion of one user in a test tenant completes, including search and object storage.
- [ ] Backups either expire inside the retention window or cannot resurrect a deleted person. See [retention](retention.md).
- [ ] Marketing and product analytics are not the same pipeline as the system of record.

## Anti-patterns

- Putting personal data in the message of a metric label or a URL path that access logs retain.
- A privacy policy that lists controls the code does not implement.
- Training a model on customer content without a contractual basis the customer can see.
- Using production personal data in local development because staging is empty.
