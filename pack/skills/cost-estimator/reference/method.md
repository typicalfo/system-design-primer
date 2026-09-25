---
title: "Cost estimate method"
summary: "Formulas for a design cost estimate, then a worked object-storage example with every product shown."
tags: [cost, estimates, unit-economics]
when_to_use: "Use when substituting workload drivers and assumed unit prices into a monthly cost and a per-unit cost."
related:
  - ../SKILL.md
  - ../../system-architect/reference/estimates.md
  - ../../../../templates/capacity-estimate.md
  - ../../../../enterprise/cost/unit-economics.md
  - ../../../../enterprise/cost/capacity.md
last_reviewed: 2026-09-25
---

# Cost estimate method

Write the formula before the number. A unit price in this file is an assumption for the example, not a cloud vendor's current price. Decimal GB means 10^9 bytes. A month in the example is an assumed 30 days, not 365.25/12.

Peak rate is for capacity. Object storage in this example bills requests and bytes, so the peak multiplier is not applied to the monthly total.

## Formulas

- Average write rate (requests/s) = events per day / 86,400.
- Peak write rate = average × peak multiplier. Use this for capacity, not for the monthly request bill below.
- Stored bytes at steady state = events per day × bytes per event × retention days × copies.
- Stored GB = stored bytes / 10^9.
- Storage cost per month = stored GB × price per GB-month.
- Request cost per month = (events per day × days in the assumed month / 1,000) × price per 1,000 requests. Compute puts and gets separately.
- Egress GB per month = reads per day × fraction that leave the region × bytes per object / 10^9 × days in the assumed month.
- Egress cost = egress GB × price per GB.
- Monthly total = storage + puts + gets + egress.
- Cost per million events = monthly total / (events per day × days in the assumed month / 1,000,000).

Change one assumption at a time when you test sensitivity. Recompute the lines that assumption touches. Do not scale the whole bill by the same factor unless every line actually scales.

## Worked example

An audit ingest writes objects and almost never reads them. Every input below is **assumed**.

| Driver or price | Value |
|---|---|
| Events per day | 50,000,000 |
| Bytes per event | 1,000 |
| Retention | 365 days |
| Copies | 2 |
| Reads per day | 5,000,000 |
| Egress fraction of reads | 0.10 |
| Assumed month | 30 days |
| Storage price | $0.02 per GB-month |
| PUT price | $0.005 per 1,000 |
| GET price | $0.0004 per 1,000 |
| Egress price | $0.09 per GB |
| Peak multiplier | 4, for capacity only |

**Rate, for capacity.**

50,000,000 / 86,400 = 578 + 19/27 ≈ 578.704 writes/s.

Peak = 4 × (578 + 19/27) = 2,314 + 22/27 ≈ 2,314.815 writes/s.

The monthly bill below does not use 2,314.815. It uses the day's event count.

**Storage.**

Daily bytes = 50,000,000 × 1,000 = 50,000,000,000 bytes = 50 GB.

Steady state = 50 GB/day × 365 days × 2 copies = 36,500 GB.

Storage cost = 36,500 × 0.02 = $730 per month.

**Puts.**

Requests in the assumed month = 50,000,000 × 30 = 1,500,000,000.

Thousands = 1,500,000,000 / 1,000 = 1,500,000.

PUT cost = 1,500,000 × 0.005 = $7,500.

**Gets.**

5,000,000 × 30 = 150,000,000 reads.

150,000,000 / 1,000 = 150,000 thousands.

GET cost = 150,000 × 0.0004 = $60.

**Egress.**

Bytes per day that leave = 5,000,000 × 0.10 × 1,000 = 500,000,000 bytes = 0.5 GB/day.

Month = 0.5 × 30 = 15 GB.

Egress cost = 15 × 0.09 = $1.35.

**Total.**

730 + 7,500 = 8,230.

8,230 + 60 = 8,290.

8,290 + 1.35 = $8,291.35 per month.

PUT share = 7,500 / 8,291.35 ≈ 0.905, so about 90% of this bill is the write requests, not the disks.

## Sensitivity

**Event size doubles to 2,000 bytes.** Storage doubles to $1,460. Egress doubles to $2.70. Puts and gets are priced per request, so they stay $7,500 and $60.

New total = 1,460 + 7,500 + 60 + 2.70 = $9,022.70.

Delta = 9,022.70 - 8,291.35 = $731.35.

731.35 / 8,291.35 ≈ 0.0882, about 8.8% higher. Doubling the object size does not double this bill.

**PUT price doubles to $0.01 per 1,000.** PUT cost = 1,500,000 × 0.01 = $15,000. Other lines stay.

New total = 730 + 15,000 + 60 + 1.35 = $15,791.35.

15,791.35 / 8,291.35 ≈ 1.905, about 1.90× the original. The assumed request price dominates the error bar.

**Retention is 90 days, not 365.** Storage GB = 50 × 90 × 2 = 9,000. Cost = 9,000 × 0.02 = $180.

New total = 180 + 7,500 + 60 + 1.35 = $7,741.35.

Cutting retention by more than 4× removes $550 of storage (730 - 180 = 550) and leaves the $7,500 of puts. Retention is the wrong knob if the goal is to move this total.

## Unit economics

Events in the assumed month = 50,000,000 × 30 = 1,500,000,000 = 1,500 million.

Cost per million events = 8,291.35 / 1,500 = $5.527566….

Rounded to the cent: **$5.53 per million events**.

Per event = 8,291.35 / 1,500,000,000 = $0.0000055276….

The unit hides the shape. Almost all of the $5.53 is the put price. A second copy or a longer retention barely moves it, which is the opposite of a design that stores large objects and writes them once.

## Left out of the example

The API fleet, the queue, support, and people are not in the $8,291.35. Add them as their own lines with their own assumptions. Do not spread them silently into the per-event number and still call it an infrastructure unit cost.
