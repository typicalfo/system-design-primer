---
title: "ISO 27001 and FedRAMP"
summary: "Treat ISO/IEC 27001:2022 as an ISMS with a statement of applicability, and treat FedRAMP as an authorization boundary with evidence that keeps moving."
tags: [compliance, iso27001, fedramp, security]
when_to_use: "Use when a customer asks for ISO/IEC 27001 or FedRAMP and you need the engineering consequences, not a legal opinion."
related:
  - soc2.md
  - audit-logs.md
  - residency.md
  - privacy.md
  - eu-regulations.md
  - ../security/encryption-keys.md
  - ../delivery/cicd.md
  - ../observability/incidents.md
last_reviewed: 2026-09-25
---

# ISO 27001 and FedRAMP

This page is engineering guidance. It is not legal advice, not an accreditation opinion, and not a FedRAMP authorization.

ISO/IEC 27001 is a management-system standard. You certify an information security management system (ISMS): scope, risk assessment, risk treatment, and evidence that the system operates. FedRAMP is a US federal program for authorizing cloud services. A control can feed both. A certificate is not an authorization, and an authorization is not a certificate.

## Decide

| Choose | Use when | Avoid when |
|---|---|---|
| ISO/IEC 27001:2022 ISMS | Customers want an accredited certification of how you run security, and you will keep the scope honest | You want a badge for a product that is outside the certified scope. The scope statement is the control |
| Statement of Applicability as a living list | You need to show which reference controls apply, which you exclude, and why | The spreadsheet is updated the week of the audit and ignored after |
| FedRAMP Rev5 | An agency path still requires it, or you run infrastructure that the 2026 rules still send down that path | You are starting from zero in 2026 and have not read whether 20x is the path FedRAMP tells you to use |
| FedRAMP 20x | The service is the kind of cloud offering the 2026 rules tell to use 20x, and you can produce the evidence those rules name | You describe a pilot slide from 2025 as if the rules had not moved |

## ISO/IEC 27001:2022

ISO published ISO/IEC 27001:2022 on 25 October 2022. [IAF MD 26:2023](https://iaf.nu/iaf_system/uploads/documents/IAF_MD26_Issue_2_15012023.pdf) (Issue 2, 15 February 2023) is the accreditation document for the transition from ISO/IEC 27001:2013. It sets a 36-month transition. Certification bodies were to finish transitioning certified clients by 36 months from the last day of the publication month, which the document gives as 31 October 2025. That date has passed. A 2013 certificate is outside that transition arrangement.

Annex A of the 2022 edition is normative and references the controls in ISO/IEC 27002:2022. IAF MD 26:2023 records that this reference set went from 114 controls in 14 clauses to 93 controls in 4 clauses: 11 new, 24 merged, 58 updated (11 + 24 + 58 = 93). Those four clauses are the organizational, people, physical, and technological themes. The ISMS clauses (context, leadership, planning, support, operation, performance evaluation, improvement) stayed in the management-system shape. Annex A is the reference set you compare against, not a list you must implement blindly.

The Statement of Applicability is the output of that comparison (ISO/IEC 27001 clause 6.1.3). For each reference control: applicable or not, the justification, and where the control lives. Engineering owns the evidence for the controls marked applicable: access reviews, change records, logging, backup tests, supplier lists. An exclusion needs a reason tied to the risk assessment. "We use the cloud" is not a reason to drop a control that still applies to how you configure the cloud.

ISO/IEC 27001 and [SOC 2](soc2.md) both ask whether named controls operated. ISO is a certification of an ISMS against the standard. SOC 2 is an attestation against the Trust Services Criteria you include. Map evidence once (the same access review, the same deploy log) and keep the system description and the ISMS scope pointing at the same architecture. They do not replace each other.

## FedRAMP

FedRAMP authorizes a cloud service offering for US federal use. The historic Rev5 baselines are Low, Moderate, and High, selected from [NIST SP 800-53 Rev. 5](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final). Do not quote a control count from a vendor blog. Use the baseline file for the path you are actually on.

The program is mid-transition. On 25 June 2026 FedRAMP [wrote](https://www.fedramp.gov/2026-06-25-propelling-change-fedramp-launches-consolidated-rules-for-2026/) that FedRAMP 20x is no longer only a pilot and is a widely available certification path, with the Consolidated Rules for 2026 as the ruleset. The [2026 timeline](https://www.fedramp.gov/2026/timeline/) publishes these dates:

- 6 July 2026: marketplace listings for the initial implementation phase.
- 28 July 2026: FedRAMP Ready submissions stop; the page points providers at 20x Class A instead.
- 3 August 2026: 20x Class A pipeline opens.
- 10 August 2026: temporary Rev5 pipelines (Ready Conversion and Lost Sponsor) open for Class B and Class C, for limited providers, without an agency sponsor.
- 31 August 2026: 20x Class B and Class C pipelines open.
- 1 January 2027: mandatory adoption of the consolidated rules, with the page's own caveat about applicability and effective dates inside specific areas.
- 11 June 2027: no new Rev5 certification applications.

[Choosing a certification type](https://www.fedramp.gov/2026/providers/start/type/) describes two types. 20x is processed by FedRAMP and does not require an active agency contract or sponsor. Rev5 typically does require an agency sponsor, and the same page says it remains the route for offerings that run their own infrastructure or need a Class D certification. The page says FedRAMP anticipates piloting 20x Class D in late 2026 and offering it formally in early 2027. This page does not equate a class letter with Low, Moderate, or High. Read the current rule for the offering you have. The dates above are from that timeline page; confirm them on fedramp.gov before you plan a submission, because the program is still moving.

Continuous monitoring is part of staying authorized. Significant change, vulnerability handling, and ongoing evidence are operating work, not a PDF you file once. Incident handling still needs an owner and a clock. See [incidents](../observability/incidents.md).

## What engineering has to make true

- **Boundary.** Draw the authorization or ISMS boundary around the components that actually handle the data, including the identity provider, the log pipeline, the backup region, and the support tool. A dependency outside the picture is a finding when an assessor traces a request.
- **Cryptography.** Federal baselines expect validated cryptographic modules where the control says so, not a homemade cipher. See [encryption and keys](../security/encryption-keys.md).
- **Location and people.** Federal customers often require the service and the people who can reach production data to sit where the authorization says. Do not promise "US persons only" or a region you have not enforced. See [data residency](residency.md).
- **Change and logging.** Production changes are attributable. Privileged actions and access to federal or customer data are in the [audit log](audit-logs.md), with time sync and a retention period that covers the review.
- **Vulnerabilities.** The baseline you adopted has remediation windows by severity. Put those windows in the scanner workflow and measure them. This page does not restate a day count, because the 2026 rules and the Rev5 baseline are not the same document.
- **Restore and incident drills.** A backup you have not restored, and an incident path you have not named, will not survive either an audit or an authorization review.

## Checklist

- [ ] The ISMS scope or the authorization boundary matches the architecture diagram.
- [ ] The Statement of Applicability, if you claim 27001, has an owner and a date.
- [ ] 2013-edition certificates are not described as current.
- [ ] The FedRAMP path (20x class or Rev5) is the one the current fedramp.gov page tells this offering to use.
- [ ] Crypto, regions, and who can reach production are the same in the package and in the system.
- [ ] A vulnerability older than its remediation window is visible as a breach of the window, not as a backlog anecdote.

## Anti-patterns

- Certifying the corporate laptop fleet and letting the sales page imply the product is certified.
- Copying Annex A into a policy wiki and not changing a deploy pipeline.
- A FedRAMP boundary that excludes the identity provider or the backup account.
- Treating 20x marketing from early 2025 as the rule after the June 2026 rules landed.
- Sharing an authorization package and then adding a region the package does not name.

## Related

- [SOC 2 basics](soc2.md)
- [EU regulations](eu-regulations.md) for a different set of duties that can share the same evidence.
- [Threat modeling](../security/threat-modeling.md)

## Further reading

- [IAF MD 26:2023, transition to ISO/IEC 27001:2022](https://iaf.nu/iaf_system/uploads/documents/IAF_MD26_Issue_2_15012023.pdf)
- [NIST SP 800-53 Rev. 5](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- [FedRAMP, 25 June 2026: consolidated rules](https://www.fedramp.gov/2026-06-25-propelling-change-fedramp-launches-consolidated-rules-for-2026/)
- [FedRAMP 2026 timeline](https://www.fedramp.gov/2026/timeline/)
- [Choosing a FedRAMP certification type](https://www.fedramp.gov/2026/providers/start/type/)
