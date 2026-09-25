---
title: "DPIA template"
summary: "A Data Protection Impact Assessment outline aligned to GDPR Article 35: processing description, necessity, risks to people, and measures."
tags: [templates, privacy, gdpr, dpia]
when_to_use: "Use when a processing activity may be high risk to people and you need a written assessment before you build or change it."
related:
  - ../enterprise/compliance/privacy.md
  - ../enterprise/compliance/eu-regulations.md
  - ../enterprise/compliance/retention.md
  - ../enterprise/compliance/residency.md
  - ../enterprise/compliance/audit-logs.md
  - threat-model.md
last_reviewed: 2026-09-25
---

# DPIA: <processing activity>

**Not legal advice.** Counsel decides whether Regulation (EU) 2016/679 requires this assessment, whether you are the controller or the processor, which lawful basis applies, and whether residual risk needs prior consultation. This file is the engineering record of what the system actually does.

The regulation text used for this outline is the English HTML on EUR-Lex: <https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679>. Article 35 is the impact assessment. Article 36 is prior consultation when residual risk stays high. Engineering consequences of privacy law, short of this assessment, are in [privacy](../enterprise/compliance/privacy.md).

| Field | Value |
|---|---|
| Controller | The party that decides why and how. Not a vendor name by habit |
| Processor, if we are one | The customer is then the controller. Say so |
| DPO or privacy contact | Article 35 asks the controller to seek the DPO's advice where a DPO is designated |
| Author and date | |
| Status | Draft, in review, or accepted |
| Review trigger | What change would make this stale |

## Do we need one

*Article 35 is aimed at processing likely to result in a high risk to people's rights and freedoms, in particular with new technology. It calls out three cases especially: systematic extensive evaluation of people by automated processing, including profiling, that produces legal or similarly significant effects; large-scale processing of special-category data or criminal-offence data; systematic large-scale monitoring of a public place. A supervisory authority's list can add or remove cases. If counsel says no DPIA is required, write that conclusion and the reason. Do not leave a blank.*

| Question | Answer |
|---|---|
| High risk to rights and freedoms? | |
| Which listed case, if any? | |
| Counsel's conclusion | DPIA required, or not, and why |

## Description of the processing

*Article 35 asks for a systematic description of the operations and the purposes, including the legitimate interest where that is the basis.*

| Item | Answer |
|---|---|
| Purposes | Why, not the vendor feature name |
| Lawful basis counsel named | Contract, legal obligation, legitimate interest, consent, or another basis they named. Engineering does not pick this |
| People affected | Customers, their employees, end users, children, or the public |
| Data | Fields, including identifiers in logs and support tools |
| Source | The person, the customer tenant, or a third party |
| Recipients and subprocessors | |
| Retention | Link [retention](../enterprise/compliance/retention.md) |
| Where it is stored and processed | Link [residency](../enterprise/compliance/residency.md) |
| Transfers outside the stated region | The mechanism counsel accepted, or "none" |

## Necessity and proportionality

*Whether these operations are necessary for the purposes, and no broader.*

| Purpose | Data you need for it | Data you collect that this purpose does not need | What you will cut |
|---|---|---|---|
| | | | |

*If a field exists "because we might want it," it fails this section until a purpose owns it.*

## Risks to rights and freedoms

*Harm to people, not only harm to the company. Unauthorized disclosure, inability to access or delete, discrimination from automated decisions, loss of confidentiality of special-category data, and being unable to object. Pair with the [threat model](threat-model.md) where the abuse is technical.*

| Id | Risk to people | Likelihood and severity, in words | Affected group |
|---|---|---|---|
| R1 | | | |

## Measures

*Safeguards, security, and how you will show they operate. A measure names a control you can point at.*

| Risk | Measure | Evidence | Residual risk |
|---|---|---|---|
| R1 | | | Accept, or still high |

*If residual risk stays high after the measures, Article 36 requires the controller to consult the supervisory authority before processing. That consultation is counsel's step. Engineering stops the launch until they say otherwise.*

## Views of the people affected

*Article 35 says to seek the views of the people affected, or their representatives, where appropriate, without prejudice to commercial or public interests or the security of the processing. Record whether you did, or why you did not.*

## Review

*Revisit when the risk changes: a new purpose, a new subprocessor, a new model, a broader retention, or a breach. Article 35 also expects a review of whether processing still matches this assessment when the risk changes.*

| Date | What changed | Outcome |
|---|---|---|
| | | |
