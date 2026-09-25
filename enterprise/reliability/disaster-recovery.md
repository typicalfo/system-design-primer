---
title: "Disaster recovery, RPO, and RTO"
summary: "Name how much data you can lose and how fast you must be back, then test the restore that those numbers require."
tags: [reliability, disaster-recovery, rpo, rto, backups]
when_to_use: "Use when you must survive zone, region, or data-corruption events and a backup policy is being treated as a plan."
related:
  - multi-region.md
  - chaos.md
  - ../compliance/retention.md
  - ../compliance/residency.md
  - ../observability/incidents.md
  - ../../patterns/availability-failover.md
last_reviewed: 2026-09-25
---

# Disaster recovery, RPO, and RTO

RPO is the maximum age of data you can afford to lose (the recovery point). RTO is the maximum time to restore the service to a useful state (the recovery time). Both are product requirements. A backup that cannot be restored inside the RTO does not meet it.

Primer availability patterns (active-passive, active-active) are the topology vocabulary. The pattern card is [availability and failover](../../patterns/availability-failover.md). This page is the planning layer.

## Decide

| Target | Strategy that can meet it | Cost note |
|---|---|---|
| RPO hours, RTO hours to days | Nightly backups, restore onto new capacity | Cheap until you test the restore and discover the steps take a weekend |
| RPO minutes, RTO under an hour | Continuous replication or frequent log shipping, plus a warm standby you have promoted before | You pay for the replica and for the runbook |
| RPO near zero, RTO minutes | Synchronous replication and an automated, tested failover | Write latency and a true split-brain procedure. Do not claim this because a vendor checkbox says "multi-AZ" |
| Corruption, not just crash | Point-in-time restore and an immutable backup that replication will not overwrite | Synchronous replicas copy the bad write. They are not a backup |

## Defaults

- Write RPO and RTO per user-visible promise. The audit log, the cache, and the primary store do not share a number.
- Backups are encrypted, access-controlled, and stored outside the failure domain of the primary (another zone at minimum; another region only if residency allows).
- A restore drill runs on a schedule. Record the duration and the first step that was wrong. That duration is your honest RTO.
- Failover is a procedure with a decision maker. Automatic failover requires a fencing story so the old primary cannot accept writes after the new one does.
- Define "useful": read-only mode may meet a shorter RTO than full writes. Say so in the SLO.
- Game-day the loss of a zone before you promise the loss of a region.
- Know the difference between a snapshot (crash-consistent or application-consistent) and a logical export. Databases with a hot working set need a quiesced or log-coordinated snapshot, or the restore will not open.

## Checklist

- [ ] RPO and RTO are numbers in the design, with units.
- [ ] Someone has restored onto a clean account or cluster in the last release cycle, or you have scheduled the first drill before launch.
- [ ] Backup retention matches [deletion policy](../compliance/retention.md), including the case where a restore would bring back deleted personal data.
- [ ] Credentials to restore are not only stored inside the system being restored.
- [ ] A region loss has an owner and a communications step. See [incidents](../observability/incidents.md).

## Anti-patterns

- "The cloud is durable" with no RPO. Durable disks still lose a dropped table.
- Replication lag ignored, so the real RPO is "whatever the lag was" and nobody graphs it.
- A failover script that has never run except in the incident.
- Backups in the same account with the same admin role as production, deleted by the same bug.
