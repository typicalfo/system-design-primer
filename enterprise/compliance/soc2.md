---
title: "SOC 2 basics"
summary: "Treat SOC 2 as an attestation that named controls operated over a period, and build the evidence those controls need."
tags: [compliance, soc2, audit]
when_to_use: "Use when a customer asks for SOC 2 or when you are deciding which operational controls a product system must emit evidence for."
related:
  - audit-logs.md
  - privacy.md
  - ../observability/alerting-oncall.md
  - ../delivery/cicd.md
  - ../identity/authorization-models.md
  - ../../templates/runbook.md
  - iso27001-fedramp.md
last_reviewed: 2026-09-25
---

# SOC 2 basics

SOC 2 is an attestation engagement. An auditor reports on controls relevant to the AICPA Trust Services Criteria you include. Security is the common criterion. Availability, confidentiality, processing integrity, and privacy are optional. A Type I report looks at design at a point in time. A Type II report looks at whether the controls operated over a period (often 3–12 months).

This page is engineering guidance, not an audit opinion and not legal advice.

## What engineering is usually asked to show

| Control area | Evidence that holds up | Weak evidence |
|---|---|---|
| Access | IdP groups, named admins, periodic access review tickets, leavers removed | A shared root password and a spreadsheet of "should have access" |
| Change management | Reviewed pull requests, CI checks, deploy logs tied to a commit | SSH onto the box and editing live config |
| Logging and monitoring | Security and admin audit log, alert routing, an on-call roster | A log bucket nobody pages on |
| Incident response | A runbook, a channel, a postmortem with actions | "We figure it out" |
| Vendor management | A list of subprocessors and what data they hold | Unknown SaaS tools with production tokens |
| Backup and recovery | A tested restore with a date | "The provider snapshots" with no restore drill |

## Defaults

- Pick criteria you actually operate. Do not advertise availability criteria if you have no SLO and no failover test.
- One system of record for production access. Reviews compare that system to the people who are employed and on the team.
- Changes to production are attributable: who approved, what digest, when.
- Time is synchronized. Audit logs are retained for the examination window and longer if contracts require. See [audit logs](audit-logs.md).
- Exceptions have an owner and an expiry. A permanent "temporary" firewall hole becomes a finding.
- Collect evidence continuously. A month of screenshots before the auditor arrives is how controls fail Type II.

## Checklist

- [ ] You can export, for a chosen week, the production deploys and the approver.
- [ ] You can show a leaver who lost access on a known date.
- [ ] A backup restore has been done and the date is recorded.
- [ ] Customer data locations (regions, vendors) match what the report describes.
- [ ] The system description the auditor saw matches the architecture you run now.

## Anti-patterns

- Buying a tool called "compliance" and leaving production access unchanged.
- Writing policies for controls the deployment pipeline does not enforce.
- Sharing a SOC 2 report under NDA and then building a feature that contradicts the system description without telling anyone who owns the report.
- Confusing SOC 2 with a product security certification or with ISO "compliance" as a badge.
