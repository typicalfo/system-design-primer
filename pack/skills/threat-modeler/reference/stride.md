---
title: "STRIDE reference"
summary: "Six questions to ask of each element and each trust-boundary crossing, plus the severity scale the threat-modeler skill uses."
tags: [security, stride, threat-model]
when_to_use: "Use when walking a data-flow description for spoofing, tampering, repudiation, disclosure, denial of service, and elevation of privilege."
related:
  - ../SKILL.md
  - ai-threats.md
  - ../../../../templates/threat-model.md
  - ../../../../enterprise/security/threat-modeling.md
last_reviewed: 2026-09-25
---

# STRIDE reference

STRIDE is a prompt, not a quota. One real abuse is a row. Six empty letters are not.

The filled document, when you need one, is the [threat model template](https://github.com/typicalfo/system-design-primer/blob/master/templates/threat-model.md).

## Questions

Ask these of the element and of the flow that crosses a trust boundary.

| Letter | Question | A mitigation is specific |
|---|---|---|
| Spoofing | Can a caller pretend to be a user, a tenant, a service, or the model? | Authenticate the caller. Bind the tenant to the credential, not to a field the client sends |
| Tampering | Can the payload, the record, or the tool argument change without detection? | TLS where the bytes cross a network. Integrity on records you must trust later. Reject unexpected fields |
| Repudiation | Can someone take a privileged action and later deny it, with no record? | An append-only audit of actor, object, action, and time. The actor comes from the credential |
| Information disclosure | Can this caller read another tenant, a secret, or fields they were not owed? | Authorize every read. Do not log the secret. Do not return the whole row by default |
| Denial of service | Can one caller exhaust a shared pool, a quota, or a bill? | A timeout, a limit, and a bulkhead. An unbounded retry is not a control |
| Elevation of privilege | Can a normal caller reach an admin action, or a tool act with a broader role? | The check runs on the server. The client's role claim is not the decision |

## Where to look

- Each process that accepts a request.
- Each store, including the backup, the export, and the log pipeline.
- Each flow that crosses a boundary you listed.
- The operator path and the CI path, if the description has them.

A health check can wait until the flows that touch credentials, tenant data, money, or admin actions are done.

## Severity

Same four levels as the [design reviewer](https://github.com/typicalfo/system-design-primer/blob/master/pack/skills/design-reviewer/SKILL.md), applied to an abuse:

| Severity | Use when |
|---|---|
| Critical | A likely path to cross-tenant or cross-customer disclosure, silent loss of data the design promised to keep, or an unauthenticated write to the source of truth |
| High | A missing control that fails under a fault the design should expect: a stolen token, a replay, a flooded caller, a dependency timeout |
| Medium | Holds for the callers you named, and breaks if a boundary the diagram already shows is left out (admin tool, export, backup) |
| Low | Harder to operate or explain. The requirement still holds |

Do not raise severity because the story is clever. Raise it because the path is likely and the harm is large.

## Accepted risk

An accepted risk names the residual harm, the owner, and the signal that would tell you it is happening. An accepted risk of "insiders are trusted" is not available on a multi-tenant system.
