---
title: "Capacity estimate worksheet"
summary: "A worksheet for request rate, bandwidth, storage, the first bottleneck, and the cost driver."
tags: [templates, capacity, estimates]
when_to_use: "Use when a design needs back-of-the-envelope numbers that a reviewer can recompute."
related:
  - design-doc.md
  - ../enterprise/cost/capacity.md
  - ../enterprise/cost/unit-economics.md
  - ../pack/skills/system-architect/reference/estimates.md
last_reviewed: 2026-09-25
---

# Capacity estimate: <system>

*Formulas: [estimates reference](../pack/skills/system-architect/reference/estimates.md). Mark every input given or assumed.*

## Inputs

| Input | Value | Given or assumed |
|---|---|---|
| Events or requests per day | | |
| Peak multiplier | | |
| Average payload bytes | | |
| Read:write ratio | | |
| Retention days | | |
| Copies you operate | | |
| Index overhead | | |

## Arithmetic

- Average rate = (per day) / 86,400 = 
- Peak rate = average × peak multiplier = 
- Ingress bytes/s = write rate × payload = 
- Egress bytes/s = read rate × response bytes × fraction returned = 
- Storage = per day × payload × retention days × copies × (1 + overhead) = 

*Say whether GB means 10^9 or 2^30.*

## 10× check

*Multiply peak rate, bandwidth, and the hot working set by 10. What saturates first: partition throughput, connections, disk, lock, quota, or a single hot key?*

## Bottleneck and headroom

| Resource | Limit | Expected at peak | Headroom action |
|---|---|---|---|
| | | | |

## Cost driver

| Driver | Unit cost assumption | Monthly order of magnitude |
|---|---|---|
| Storage, requests, egress, or replicas | | |

*One sentence on what you would shed if the forecast is low. Link [load shedding](../enterprise/reliability/load-shedding.md) if you need the pattern.*
