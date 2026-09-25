---
title: "EU regulations for engineering"
summary: "Map the AI Act, DORA, NIS2, and the Cyber Resilience Act to logs, inventories, incident clocks, and tests, and separate adopted dates from the original calendar."
tags: [compliance, eu, ai-act, dora, nis2, cra]
when_to_use: "Use when a product may be offered in the EU and you need the engineering capabilities the current legal calendar implies."
related:
  - privacy.md
  - audit-logs.md
  - residency.md
  - iso27001-fedramp.md
  - ../observability/incidents.md
  - ../security/supply-chain.md
  - ../data/governance.md
  - ../../templates/dpia.md
last_reviewed: 2026-09-25
---

# EU regulations for engineering

This page is an engineering map. It is not legal advice. Counsel decides whether you are in scope: provider or deployer of an AI system, a financial entity, an essential or important entity under a national NIS2 law, or a manufacturer of a product with digital elements. The dates below are the ones in the acts cited. Where a later act changed a date, both are stated.

EUR-Lex HTML is often a bot check. The PDF links in [Further reading](#further-reading) are the copies whose text was read for this page.

## Decide

| Topic | Use when | Avoid when |
|---|---|---|
| AI Act calendar | You place an AI system or a general-purpose model on the EU market, or you deploy one in a way the regulation covers | You treat every internal script as high-risk. Scope is in the regulation, not in the word "AI" |
| DORA | You are a financial entity, or you sell ICT services into one and the contract flows the duties down | You copy the NIS2 24-hour clock onto a bank incident. DORA has its own reporting rules |
| NIS2 | You may be an essential or important entity under a member state's law | You implement the directive text and skip the national statute. NIS2 applies through that statute |
| Cyber Resilience Act | You manufacture a product with digital elements made available in the Union | You assume open-source maintained outside the course of a commercial activity is in the same bucket. Read the exclusions in the regulation |
| GDPR, already covered | The system stores data about people | You rebuild that program here. See [GDPR and CCPA basics](privacy.md) |

## AI Act

[Regulation (EU) 2024/1689](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:L_202401689) was done at Brussels on 13 June 2024 and published in the Official Journal on 12 July 2024 (OJ L, 12.7.2024). Article 113 says it enters into force on the twentieth day following publication. Counting from 12 July 2024, 13–31 July is 19 days and 1 August is the 20th, so entry into force is 1 August 2024. Recital 1 of the later amending regulation states the same date.

Article 113, as adopted in 2024, says the regulation applies from 2 August 2026, with three earlier or later slices:

- Chapters I and II from 2 February 2025. Chapter II is the list of prohibited AI practices.
- Chapter III Section 4, Chapter V, Chapter VII, Chapter XII, and Article 78 from 2 August 2025, except Article 101. Chapter V is where the general-purpose AI model obligations sit. The recitals tie those obligations to 2 August 2025.
- Article 6(1) and the corresponding obligations from 2 August 2027. Article 6(1) classifies a system as high-risk only when both of these hold: it is a safety component of a product, or is itself a product, covered by the Union harmonisation legislation in Annex I; and that product must undergo a third-party conformity assessment under that legislation.

That 2 August 2027 bullet is the original text. It is not the rule for high-risk systems after July 2026.

The Commission's proposal to simplify implementation, including the high-risk dates, went through the ordinary legislative procedure and is adopted as [Regulation (EU) 2026/1744](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:L_202601744) (Digital Omnibus on AI), done at Strasbourg on 8 July 2026, published 24 July 2026 (OJ L, 24.7.2026). It enters into force on the third day following publication: 25, 26, and 27 July 2026, so 27 July 2026. The [Commission's notice](https://digital-strategy.ec.europa.eu/en/news/ai-omnibus-enters-force) says the same. This is not a pending proposal. Other Commission simplification files, if any, are outside this page.

The amendment keeps a general application date of 2 August 2026 (recital 40). It replaces the high-risk application rule. Chapter III, Sections 1, 2, and 3, except Article 6(5), apply from:

- 2 December 2027 for AI systems classified as high-risk under Article 6(2) and Annex III.
- 2 August 2028 for AI systems classified as high-risk under Article 6(1) and Annex I.

The amendment also sets 2 December 2026 for Article 5(1), first subparagraph, points (ba) and (bb), and for Article 5(1a) and (1b). Articles 102 to 110 apply from 27 July 2026. Point (ba) covers an AI system that generates or manipulates realistic intimate or sexually explicit material of an identifiable person without that person's consent. Point (bb) covers material or performance within Article 2, points (c) and (e), of Directive 2011/93/EU. Paragraphs 1a and 1b limit when placing on the market, putting into service, or use is actually prohibited. Read those points before you treat a generator as banned.

As of 25 September 2026, the dates that were not deferred have passed: prohibited practices from 2 February 2025, the Chapter V general-purpose model slice from 2 August 2025, and the general application date of 2 August 2026. The deferred high-risk dates and the 2 December 2026 Article 5 points, (ba), (bb), (1a), and (1b), are still ahead. Read the consolidated text before you build a compliance program around a single sentence on this page.

## DORA

[Regulation (EU) 2022/2554](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32022R2554) (Digital Operational Resilience Act) was published in OJ L 333 on 27 December 2022. Article 64 says it applies from 17 January 2025. It is in application.

For financial entities it requires ICT risk management, incident reporting, resilience testing, and management of risk from ICT third parties. Advanced testing based on threat-led penetration testing (TLPT) applies to financial entities that meet the regulation's criteria, not to every firm and not to every microenterprise. Every financial entity keeps a register of information on contractual arrangements for ICT services from third-party providers. Incident reporting under DORA uses the regulation's own timelines. Do not paste the NIS2 clocks onto a DORA incident.

If you are the ICT provider rather than the financial entity, the duties arrive mainly by contract and, for providers designated critical, by the oversight framework. Confirm designation with counsel. Do not self-declare it from a blog.

## NIS2

[Directive (EU) 2022/2555](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32022L2555) was published in OJ L 333 on 27 December 2022. Article 41 required member states to adopt and publish the national measures by 17 October 2024 and to apply them from 18 October 2024. The directive does not itself apply as a single EU-wide statute. Essential entities and important entities are the two classes, with different supervision. Which organizations fall in which class, and whether a member state's law matches the deadline, varies. Check the statute of each state where you operate. The [Commission's NIS2 policy page](https://digital-strategy.ec.europa.eu/en/policies/nis2-directive) is the starting index, not a substitute for that statute.

The directive's incident pattern, which national law is supposed to carry over, is: an early warning without undue delay and in any event within 24 hours of becoming aware of a significant incident; an incident notification within 72 hours; a final report not later than one month after the incident notification. Build the pipeline so those three outputs can be produced. The content of each message is in the directive and then in national law.

## Cyber Resilience Act

The [Commission's summary](https://digital-strategy.ec.europa.eu/en/policies/cra-summary) of Regulation (EU) 2024/2847, the Cyber Resilience Act, states: entry into force on 10 December 2024; Chapter IV (notification of conformity assessment bodies) from 11 June 2026; reporting obligations in Article 14 from 11 September 2026; the main obligations from 11 December 2027. As of 25 September 2026 the Article 14 reporting date has passed. The summary also says reporting applies to products with digital elements made available on the Union market, including products placed before full application, and that products placed before 11 December 2027 are subject to the full requirements only if they are substantially modified after that date. The EUR-Lex PDF for this regulation did not return a document body to a non-browser client during review, so the summary is the source for these sentences. Read the regulation before you rely on an edge case.

## What to build

| Obligation | System capability |
|---|---|
| Prohibited AI practices, and the new Article 5 points | A use-case review that can stop a feature, plus a record of the decision |
| General-purpose model obligations, if you are a provider | Model documentation, a training-data summary path, and a way to file the incidents the chapter names |
| High-risk AI, once the deferred date applies to that annex | Risk management, logging of operation, human oversight, and the data governance the chapter requires |
| Transparency for synthetic content | A mark or label the product actually emits, not a policy sentence |
| DORA ICT risk and the register of information | An asset inventory and a supplier register that includes the contract, the data, and the exit |
| DORA testing, including TLPT where the criteria say so | A test program with a scope, a date, and a fix loop. See [testing strategy](../delivery/testing-strategy.md) |
| DORA or NIS2 incidents | An incident pipeline that can emit the right report at the right hour. See [incidents](../observability/incidents.md) |
| NIS2 24 h / 72 h / one month | Three templates, a clock that starts when you become aware, and an owner |
| CRA Article 14, already in date | A vulnerability and severe-incident report path for products with digital elements |
| GDPR | Inventory, export, and deletion. See [privacy](privacy.md) and the [DPIA outline](../../templates/dpia.md) |
| All of the above | [Audit logs](audit-logs.md), time sync, and a [supplier view](../security/supply-chain.md) you can hand to an assessor |

Evidence you already keep for [ISO 27001 or FedRAMP](iso27001-fedramp.md) (access, change, restore, vendors) is the same raw material. The legal trigger and the deadline are different. Do not file one packet and assume the others are done.

## Checklist

- [ ] Someone can say, for each product, which of these regimes counsel has marked in scope.
- [ ] The AI Act dates in your program match the Omnibus text, not only the 2024 article.
- [ ] NIS2 work cites the member-state law, and the 24 h / 72 h / one-month path has been timed in an exercise.
- [ ] The DORA register of information exists if you are a financial entity, or the contract asks you for your rows if you are the ICT provider.
- [ ] CRA reporting has an owner if you ship a product with digital elements in the Union.
- [ ] Personal-data handling still points at the privacy page.

## Anti-patterns

- A single "EU compliance" epic that does not name the regulation or the date.
- Treating the Digital Omnibus on AI as a draft after 27 July 2026.
- Using 2 August 2027 as the high-risk date after the Omnibus replaced it.
- An incident bridge that cannot produce a 24-hour early warning because the only record is a chat scroll.
- Assuming the directive text is the law in every member state.

## Related

- [GDPR and CCPA basics](privacy.md)
- [ISO 27001 and FedRAMP](iso27001-fedramp.md)
- [Incidents](../observability/incidents.md)

## Further reading

- [Regulation (EU) 2024/1689, AI Act (OJ PDF)](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:L_202401689)
- [Regulation (EU) 2026/1744, Digital Omnibus on AI (OJ PDF)](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:L_202601744)
- [Commission notice: AI Omnibus enters into force](https://digital-strategy.ec.europa.eu/en/news/ai-omnibus-enters-force)
- [Regulation (EU) 2022/2554, DORA (PDF)](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32022R2554)
- [Directive (EU) 2022/2555, NIS2 (PDF)](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32022L2555)
- [Commission NIS2 policy page](https://digital-strategy.ec.europa.eu/en/policies/nis2-directive)
- [Commission summary of the Cyber Resilience Act, Regulation (EU) 2024/2847](https://digital-strategy.ec.europa.eu/en/policies/cra-summary)
