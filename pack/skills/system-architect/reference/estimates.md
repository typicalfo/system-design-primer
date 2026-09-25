# Estimates

Adapted from the System Design Primer. Attribution: [pack README](../../../README.md#attribution).

Show every multiplication. Round at the end, and say which unit (decimal GB is 10^9 bytes; GiB is 2^30). A peak multiplier is an assumption you state, not a constant the Primer defines.

## Formulas

**Requests.** Average rate = (events per day) / 86,400. Peak = average × peak multiplier. Split reads and writes. A 100:1 or 1000:1 read/write ratio is the Primer's typical case for user-facing apps; an ingest pipeline can be the opposite. Use the ratio the request implies.

**Bandwidth.** bytes/s = rate × payload bytes, computed separately for ingress and egress. Multiply egress by the fraction of requests that return a body.

**Storage.** bytes = new records per day × bytes per record × days retained × copies you actually operate. A managed store's multi-AZ durability is not automatically "×3 disks on the bill"; say which one you mean. Add a stated overhead factor for indexes, and only for the store that has them.

**10× check (for the reviewer, not a second design).** Multiply rate, bandwidth, and the hot working set by 10. Say what saturates first: partitions, connections, index disk, or a single hot key.

**Latency budget.** Add only the hops on the critical path, using the table below. A same-datacenter round trip is 0.5 ms class. A cross-continent round trip is 150 ms class. Sequential hops add. Parallel hops take the slow one. Aim for the Primer's rule: as much throughput as the requirement needs, at an acceptable latency.

**Availability in combination.** Two components both at availability A, required together (sequence): A × A. Either is enough (parallel): 1 − (1 − A) × (1 − A). The Primer's illustration: two 99.9% components in sequence land at 99.8% (the product is 99.8001%); in parallel they land at 99.9999%. Stacking five 99.9% hops in sequence is about 99.5%. Put the redundancy on the hop that dominates the product.

### Downtime the Primer publishes

These are the Primer's published figures. They sit within about a second of 0.1% and 0.01% of a 365.25-day year.

| Target | Per year | Per month | Per week | Per day |
|---|---|---|---|---|
| 99.9% (three 9s) | 8h 45min 57s | 43m 49.7s | 10m 4.8s | 1m 26.4s |
| 99.99% (four 9s) | 52min 35.7s | 4m 23s | 1m 5s | 8.6s |

Quote a target only after naming the window and the user-visible failure. "The API returns 5xx" and "a queued export is an hour late" are different availabilities.

## Powers of two

The Primer's table. Use it to convert between addressable sizes and SI-ish words so a "10 million rows × 1 KB" estimate does not drift by 10×.

| Power | Exact | Approx | Bytes |
|---|---|---|---|
| 7 | 128 | | |
| 8 | 256 | | |
| 10 | 1,024 | 1 thousand | 1 KB |
| 16 | 65,536 | | 64 KB |
| 20 | 1,048,576 | 1 million | 1 MB |
| 30 | 1,073,741,824 | 1 billion | 1 GB |
| 32 | 4,294,967,296 | | 4 GB |
| 40 | 1,099,511,627,776 | 1 trillion | 1 TB |

The Primer's "KB/MB/GB" column is powers of two (1 KB = 2^10 bytes), not decimal SI. Say so when you mix it with GB-as-10^9 pricing.

## Latency numbers every programmer should know

Reprinted from the Primer, which sources Jeff Dean's figures via the ["Latency Numbers Every Programmer Should Know"](https://gist.github.com/jboner/2841832) gist. These are order-of-magnitude tools.

**Dated.** The SSD line (~1 GB/s, 150 µs for a random 4 KB read) and the 1 Gbps Ethernet line predate NVMe and 10/25/100 Gbps networks. Same-datacenter RTTs on a modern cloud network are often well under 500 µs, and a regional object store is not an HDD. Do not replace this table with invented "current" numbers. Keep the ratios: memory is far faster than disk, disk is far faster than a cross-region round trip, and a cross-continent trip dominates any local cache hit. Measure the hop you are betting the design on.

| Operation | Time |
|---|---|
| L1 cache reference | 0.5 ns |
| Branch mispredict | 5 ns |
| L2 cache reference | 7 ns |
| Mutex lock/unlock | 25 ns |
| Main memory reference | 100 ns |
| Compress 1 KB with Zippy | 10 µs |
| Send 1 KB over 1 Gbps | 10 µs |
| Read 4 KB randomly from SSD | 150 µs |
| Read 1 MB sequentially from memory | 250 µs |
| Round trip in the same datacenter | 500 µs |
| Read 1 MB sequentially from SSD | 1 ms |
| Disk seek (HDD) | 10 ms |
| Send 1 MB over 1 Gbps | 10 ms |
| Read 1 MB sequentially from HDD | 30 ms |
| Packet CA → Netherlands → CA | 150 ms |

The Primer's derived sequential rates, same vintage: memory ~4 GB/s, SSD ~1 GB/s, 1 Gbps Ethernet ~100 MB/s, HDD ~30 MB/s. About 2,000 same-datacenter round trips per second, and 6–7 cross-continent round trips per second. A design that needs a cross-region read on the user path cannot also promise an interactive p99 under 100 ms.
