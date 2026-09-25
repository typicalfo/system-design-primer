---
title: "Build versus buy"
summary: "Score differentiation, total cost, time, skill, vendor risk, compliance, and the exit, then revisit the score at renewal."
tags: [organization, build-vs-buy, vendors, procurement]
when_to_use: "Use when a team is about to build a capability that already exists as a product, or adopt a vendor for something customers will notice."
related:
  - decisions.md
  - ownership.md
  - ../security/supply-chain.md
  - ../compliance/soc2.md
  - ../cost/finops.md
  - ../../templates/vendor-evaluation.md
  - ../../templates/adr.md
last_reviewed: 2026-09-25
---

# Build versus buy

Build when the capability is why a customer picks you, or when a vendor would sit on the critical path with no exit. Buy when the capability is necessary and undifferentiated, and a vendor already operates it better than you will in the next year. Open source with a support contract is a third column, not a slogan: you still own integration, upgrades, and the failure.

Write the decision down. See [ADRs and RFCs](decisions.md) and the [vendor evaluation](../../templates/vendor-evaluation.md) outline.

## Decide

| Choose | Use when | Avoid when |
|---|---|---|
| Build | The behavior is the product, or the data and the control model cannot leave your boundary | You are rebuilding a queue, an IdP, or a log pipeline because the team's last vendor was annoying |
| Buy | Time to a supported outcome beats the differentiation, and you can name the exit | The vendor's outage is your outage and you have no degraded mode |
| Open source you run, with a support contract | You need the code and the option to patch, and you will staff upgrades | "It's free" is the whole analysis. Your on-call is the license fee |
| Open source as a hosted service | You want the project and not the pager | The hosted fork lags the project, or the export format is private |

## What goes in the cost

Total cost is more than the invoice.

- License or support, for the term you will actually sign.
- Integration: identity, data mapping, network, and the glue you will still be debugging next year.
- Operations: on-call, capacity, upgrades, and the people who know the system. A bought system you cannot configure is still your incident.
- Exit: export, rewrite, dual-run, and the months of contract you must pay while you leave. If export is a professional-services engagement, put that number in the score.
- Switching cost that shows up as lock-in: proprietary query languages, private APIs, and data that is only useful inside the tool.

A one-year price that ignores exit will beat a build you should have done, and the reverse mistake is also common.

## A score you can recompute

Use the same weights for every option. This example uses seven weights that sum to 100: differentiation 25, total cost 20, time to value 15, team capability 15, vendor risk 10, data and compliance 10, exit 5.

Check: 25 + 20 + 15 + 15 + 10 + 10 + 5 = 100.

Score each cell from 1 to 5, where 5 is better for you (cheaper, faster, safer, easier to leave, more differentiated). Weighted points are score times weight. The maximum is 5 × 100 = 500.

Worked example, not a recommendation:

| Factor | Weight | Build (score) | Build points | Buy (score) | Buy points |
|---|---:|---:|---:|---:|---:|
| Differentiation | 25 | 4 | 100 | 2 | 50 |
| Total cost | 20 | 2 | 40 | 3 | 60 |
| Time to value | 15 | 2 | 30 | 5 | 75 |
| Team capability | 15 | 4 | 60 | 3 | 45 |
| Vendor risk | 10 | 5 | 50 | 2 | 20 |
| Data and compliance | 10 | 4 | 40 | 3 | 30 |
| Exit | 5 | 4 | 20 | 2 | 10 |
| Total | 100 |  | 340 |  | 290 |

Build points: 100 + 40 + 30 + 60 + 50 + 40 + 20 = 340. Buy points: 50 + 60 + 75 + 45 + 20 + 30 + 10 = 290. Both out of 500. In this example build scores higher because differentiation and exit outweigh a slower start. Change the weights if time to value is the constraint, and recompute. Do not reuse a weight set you would be embarrassed to show the team that has to live with the result.

An option under a hard constraint loses before the arithmetic. If the data cannot sit in that vendor's region, the compliance cell is not a 2. The option is out. See [data residency](../compliance/residency.md) and [SOC 2](../compliance/soc2.md).

## Defaults

- One owner for the decision and for the system after it ships. See [service ownership](ownership.md).
- A spike with an end date beats a six-month proof of concept that has production data in it.
- The exit plan is a paragraph in the decision: format, time, and who does the work. "We can always export" is not a plan.
- Revisit at renewal, after a material outage, when the capability becomes customer-visible, and when the team that knew the system has left.
- Supply-chain questions (what the vendor runs, how you get updates, what happens when the project is abandoned) belong in the vendor-risk cell. See [supply chain](../security/supply-chain.md).
- Cost after the first year belongs in the total-cost cell, not in a footnote. See [FinOps](../cost/finops.md).

## Checklist

- [ ] The weights sum to 100 and every option used the same weights.
- [ ] Exit cost is a number or a range, not an adjective.
- [ ] A hard compliance or data-location fail removed an option before scoring.
- [ ] The team that will operate the winner was in the room.
- [ ] The decision says when it will be reopened.

## Anti-patterns

- Scoring the vendor's demo and not the integration you will write.
- Build, because buying feels like a loss of control, with no one to page.
- Buy, because the invoice is smaller than four salaries, ignoring the exit and the glue.
- Open source with no owner for upgrades.
- A score that cannot be recomputed because the weights were adjusted after the favorite won.

## Related

- [ADRs and RFCs](decisions.md) for how the decision is recorded.
- [Vendor evaluation](../../templates/vendor-evaluation.md) for the questions to ask before the score.

## Further reading

- [Service ownership](ownership.md)
- [SOC 2 basics](../compliance/soc2.md)
- [Software supply chain](../security/supply-chain.md)
