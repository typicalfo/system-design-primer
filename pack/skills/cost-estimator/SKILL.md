---
name: cost-estimator
description: "Use this when turning a system design into a cost estimate: workload drivers, unit costs labeled as assumptions, formulas before totals, sensitivity, and unit economics."
---

# Cost estimator

Turn the design into a cost estimate a reviewer can recompute. Follow [reference/method.md](reference/method.md). Do not present a unit price as a vendor's current price unless the user gave that price or you are quoting a page you actually read and dated. Otherwise label it **assumed**.

Rate, storage, and bandwidth formulas that this estimate should stay consistent with are in the [estimates reference](https://github.com/typicalfo/system-design-primer/blob/master/pack/skills/system-architect/reference/estimates.md). The human worksheet is the [capacity estimate template](https://github.com/typicalfo/system-design-primer/blob/master/templates/capacity-estimate.md). How to read the result as a business unit is in [unit economics](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/cost/unit-economics.md). Headroom and lead time are in [capacity planning](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/cost/capacity.md). The FinOps framing is in [FinOps](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/cost/finops.md).

## Steps

1. Name the workload drivers the design actually has: write rate, read rate, payload bytes, retention, copies, egress fraction, scanned bytes, or GPU time. Drop a driver the design does not use.
2. Write each unit cost as an assumption or as a dated quote. State the unit (per GB-month, per 1,000 requests) and whether GB means 10^9 bytes or 2^30 bytes.
3. Write the formula, then substitute. Show every multiplication. Round money at the end and say so.
4. A peak multiplier sizes capacity. Do not multiply it into a monthly request bill unless the bill is for provisioned peak.
5. Sensitivity: change one assumption at a time, recompute, and say which assumption moves the total.
6. Unit economics: divide the monthly total by the business unit (events, tenants, orders). Show the division.
7. Say what you left out (people, support, the application fleet) so the total is not mistaken for a full company cost.

## Output

```markdown
# Cost estimate: <name>

## Drivers
<Table: name, value, given or assumed.>

## Unit costs
<Table: price, unit, assumed or quoted, date if quoted. GB base stated.>

## Formulas and arithmetic
<Formula, substitution, result. One block per cost line.>

## Monthly total
<Sum, shown.>

## Sensitivity
<One changed input per row. New total and the delta, both shown.>

## Unit economics
<Cost per unit, division shown.>

## Left out
<What this number does not include.>
```
