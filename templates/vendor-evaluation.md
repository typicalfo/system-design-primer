---
title: "Vendor evaluation template"
summary: "A scored comparison of build, buy, or adopt: requirements, weights, security questions, a three-year cost, and how you leave."
tags: [templates, vendor, build-vs-buy]
when_to_use: "Use when a product decision depends on a vendor or an open-source project with a support contract, and the choice will be expensive to reverse."
related:
  - ../enterprise/organization/build-vs-buy.md
  - ../enterprise/cost/unit-economics.md
  - ../enterprise/cost/finops.md
  - ../enterprise/security/supply-chain.md
  - ../enterprise/compliance/soc2.md
  - ../enterprise/compliance/privacy.md
  - ../enterprise/compliance/residency.md
last_reviewed: 2026-09-25
---

# Vendor evaluation: <need>

*One paragraph. The job to be done, who the user is, and the date this comparison expires.*

This is an engineering and cost worksheet. It is not a legal review of the contract. Counsel reads the DPA, liability, and the subprocessors.

The decision framework around this outline is [build versus buy](../enterprise/organization/build-vs-buy.md).

## Requirements

*Must, should, and won't. A "must" that no option meets means the requirement is wrong or the search is.*

| Id | Requirement | Must or should | How we will check it |
|---|---|---|---|
| R1 | | Must | A proof on our data, not a slide |

## Weighted scoring matrix

*Use the same weights for every option. The defaults in [build versus buy](../enterprise/organization/build-vs-buy.md) sum to 100: differentiation 25, total cost 20, time to value 15, team capability 15, vendor risk 10, data and compliance 10, exit 5. Check: 25 + 20 + 15 + 15 + 10 + 10 + 5 = 100. Score each cell from 1 to 5, where 5 is better for you. Weighted points = weight × score. The maximum is 5 × 100 = 500. A weight of 20 and a score of 4 contribute 80. Do not change a weight after you have seen the scores in order to crown a favorite. A hard constraint (data cannot sit in that region) removes the option. It is not a low score.*

| Criterion | Weight | Option A score | Option A points | Option B score | Option B points | Build score | Build points |
|---|---:|---:|---:|---:|---:|---:|---:|
| Differentiation | 25 | | | | | | |
| Total cost | 20 | | | | | | |
| Time to value | 15 | | | | | | |
| Team capability | 15 | | | | | | |
| Vendor risk | 10 | | | | | | |
| Data and compliance | 10 | | | | | | |
| Exit | 5 | | | | | | |
| **Total** | **100** | | | | | | |

## Security and compliance questions

*Link the questionnaire you sent and the answer you got. Do not paste a vendor's policy in place of an answer about this product.*

| Question | Where it is answered | Gap |
|---|---|---|
| Who is the subprocessor, and where does our data sit? | [Residency](../enterprise/compliance/residency.md) | |
| What do they keep, for how long, and can we delete it? | [Privacy](../enterprise/compliance/privacy.md) | |
| Which report covers this product (SOC 2 type II, ISO, or none)? | [SOC 2](../enterprise/compliance/soc2.md) | |
| How do we get an SBOM, a vulnerability feed, and a signed artifact? | [Supply chain](../enterprise/security/supply-chain.md) | |
| Identity: SSO, SCIM, and an audit event for admin actions? | | |
| What happens to our data if they are down, or if we stop paying? | | |

## TCO over 3 years

*Every number is given or assumed. Say which. Currency and what a "year" is (calendar, or 12× the monthly quote). Default is an undiscounted sum. If you discount, write the rate and the factor for each year. Do not apply a factor you do not show.*

Three-year total = year 1 + year 2 + year 3.

| Cost | Year 1 | Year 2 | Year 3 | Given or assumed |
|---|---:|---:|---:|---|
| License or subscription | | | | |
| Support tier you will actually buy | | | | |
| Infrastructure you still run | | | | |
| Integration labor (hours × loaded rate) | | | | |
| Migration labor | | | | |
| Exit reserve (not spent, set aside) | | | | |
| **Year total** | | | | |

*Labor is hours × rate, written out. A rate with no hours is not a cost. Unit cost of the feature after launch belongs in [unit economics](../enterprise/cost/unit-economics.md), not only in this table.*

## Exit plan

| Question | Answer |
|---|---|
| Export format and completeness | What leaves, what is trapped in their model |
| Time to export and re-import | Measured, or an assumption |
| Contract notice period | |
| What we must rewrite | The integration, the auth model, the queries |
| Feature we lose on the way out | |
| Who owns the exit test | A drill, not a hope |

*An option with no export is a high score only if the requirement says you will not leave. That requirement belongs in the musts, not in a footnote.*

## References

| Source | Date read | What it settled |
|---|---|---|
| Vendor doc or pricing page | | |
| Security report | | |
| Internal proof | | |

*Pricing pages change. Date them. A number with no date is not evidence.*
