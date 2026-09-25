---
title: "Search"
summary: "Run lexical search, vector search, or both as a rebuildable projection, with tenant filters and a ranking eval you can recompute."
tags: [data, search, relevance, indexing]
when_to_use: "Use when a user or a service queries by words or by similarity and the database query is no longer the right index."
related:
  - cdc.md
  - transactional-outbox.md
  - idempotency.md
  - ../tenancy/data-and-keys.md
  - ../tenancy/isolation-models.md
  - ../ai/README.md
  - ../ai/rag.md
  - ../../patterns/cdc.md
last_reviewed: 2026-09-25
---

# Search

A search index is a projection of the source of truth. It can be rebuilt. It is not where the order is committed. Lexical engines (Elasticsearch, OpenSearch, Apache Solr) answer "which documents contain these terms, ranked." Vector indexes answer "which vectors are near this one." Hybrid search does both and merges the lists. Retrieval for an LLM is one consumer of the same projection. See [AI systems](../ai/README.md).

## Decide

| Approach | Use when | Avoid when |
|---|---|---|
| Lexical (inverted index, BM25) | Users type words, SKUs, or names, and you can explain a match by the terms | The query is a paragraph or an image and exact terms miss the neighbors |
| Vector ANN | Similarity over embeddings is the product, and approximate neighbors are acceptable | You need exact match on a keyword. ANN will not reliably do that |
| Hybrid | Both a rare term and a vague phrase should surface the same document | You have no judgment set, so you cannot tell whether fusion helped |
| Vectors in the OLTP database ([pgvector](https://github.com/pgvector/pgvector)) | The vectors sit on rows you already filter with SQL, and the working set fits that database | Search traffic or index builds contend with transactions, or the memory budget does not fit |
| A separate search or vector service | You need to scale query and indexing apart from the OLTP database | The corpus is small and a second store would only add lag |

## Lexical search

An inverted index maps a term to the list of documents that contain it (the postings), plus whatever you stored to rank or to highlight. A query intersects or unions those lists.

[BM25](https://en.wikipedia.org/wiki/Okapi_BM25) is the usual ranking function. One document `D` and query `Q` score as a sum over query terms `q`:

```text
score(D, Q) = sum over q in Q of
  IDF(q) * (f(q, D) * (k1 + 1))
           / (f(q, D) + k1 * (1 - b + b * |D| / avgdl))
```

`f` is the term's count in the document, `|D|` is document length, `avgdl` is the average length, `k1` saturates term frequency, and `b` scales length normalization. IDF falls as the term appears in more of the corpus. Engines differ in the IDF formula and in the default `k1` and `b`. Tune those against a judgment set, not against a single query you like.

[Elasticsearch](https://www.elastic.co/elasticsearch), [OpenSearch](https://opensearch.org/), and [Apache Solr](https://solr.apache.org/) are inverted-index engines in this family. Pick one and learn its mapping, refresh interval, and alias operation. This page does not compare their licenses or versions.

## Vector search

Exact nearest neighbor compares the query with every vector. That is the recall ceiling and the latency floor you leave behind when you approximate.

ANN structures:

- HNSW builds a layered graph. Search starts on a sparse upper layer and drops down. Spending more candidates at query time raises recall and latency. The graph stores neighbor ids, so memory is the vectors plus those links. The HNSW paper is [Malkov and Yashunin, arXiv:1603.09320](https://arxiv.org/abs/1603.09320).
- IVF clusters vectors under coarse centroids. The query probes a few lists (`nprobe`), not the whole set. Fewer probes are faster and recall less. Build time includes a training pass over the centroids.

[pgvector](https://github.com/pgvector/pgvector) documents exact search by default and two ANN index types, HNSW and IVFFlat. Its docs say HNSW has the better speed-recall tradeoff, costs more memory, and builds slower, and that IVFFlat has a training step. [Faiss](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes) documents both inverted-file and HNSW index families if you run the index in its own process.

A dedicated vector database is the same trade with an extra system: independent scaling and filtering, plus a sync path and an outage mode. Stay in Postgres while SQL filters and one backup story are worth more than that ceiling.

## Hybrid search

Run a lexical query and a vector query. Fuse the ranked lists. Reciprocal rank fusion scores a document by its rank in each list, which avoids mixing raw BM25 points with cosine similarity:

```text
RRF(d) = sum over lists of  1 / (k + rank_in_that_list(d))
```

`k` is a constant. This example uses `k = 60`. Document A is lexical rank 1 and vector rank 8. B is lexical 3 and vector 1. C is lexical 5 and vector 2.

```text
A = 1/(60+1) + 1/(60+8) = 1/61 + 1/68 = 0.016393 + 0.014706 = 0.031099
B = 1/(60+3) + 1/(60+1) = 1/63 + 1/61 = 0.015873 + 0.016393 = 0.032266
C = 1/(60+5) + 1/(60+2) = 1/65 + 1/62 = 0.015385 + 0.016129 = 0.031514
```

Order is B, then C, then A. A term hit at rank 1 does not automatically beat a document that is near the top of both lists. Any fusion you ship needs the eval below. Rank arithmetic on three documents is not that eval.

## Keeping the index in sync

The database commits. The index follows. Use an [outbox](transactional-outbox.md) or [CDC](cdc.md) into an indexer. The indexer upserts by document id and is [idempotent](idempotency.md). Lag from commit to searchable is an SLO. Deletes must reach the index or you serve ghosts.

Zero-downtime rebuild:

1. Build `index_v2` beside the live index. Readers still use a stable name (an alias or equivalent).
2. Backfill from the source, then tail the outbox or CDC until lag is inside the SLO.
3. Switch the read name to `index_v2` in one metadata update.
4. Keep the old index for the rollback window. Then delete it.

A mapping change that cannot be done in place is this procedure. It is not a lock on the live index during a full reindex.

## Tenants and permissions

| Layout | Use when | Avoid when |
|---|---|---|
| Index per tenant | Few large tenants, or a contract that the index files are physically separate | You would have tens of thousands of tiny indexes and their shard overhead |
| Shared index, mandatory tenant filter | Many small tenants and one cluster to operate | Any code path can run a query that omits the tenant predicate |

The tenant predicate is part of the server-side query builder. A client-supplied filter is not. Test that a missing tenant id is rejected. See [data and keys](../tenancy/data-and-keys.md) and [isolation](../tenancy/isolation-models.md).

Authorization is the same shape. Filter by ACL inside the query that produces hits, snippets, and totals. A check after the fact still leaks through counts and highlights, and it wastes the retrieval. An ACL bit stored in the index is stale until the permission change is indexed. If that window is unacceptable, re-check the surviving hits against the source of truth before you return them.

## Evaluating relevance

A judgment list is queries with graded documents (graded relevance, including zeros). Offline, before a ranking change ships:

- nDCG@k discounts gains deeper in the list and divides by the ideal list. This page uses gain `2^rel - 1` and discount `log2(rank + 1)`. Toolkits differ. State the formula next to the number.
- MRR is the mean of `1 / rank` of the first relevant hit. It ignores how good the second hit was.

One query, grades at ranks 1..4 of `3, 1, 0, 2`. Ideal order is `3, 2, 1, 0`. `log2(2) = 1`, `log2(3) = 1.584963`, `log2(4) = 2`, `log2(5) = 2.321928`.

```text
DCG  = (2^3 - 1)/log2(2) + (2^1 - 1)/log2(3) + (2^0 - 1)/log2(4) + (2^2 - 1)/log2(5)
     = 7/1 + 1/1.584963 + 0/2 + 3/2.321928
     = 7 + 0.630930 + 0 + 1.292030
     = 8.922960

IDCG = 7/1 + (2^2 - 1)/log2(3) + (2^1 - 1)/log2(4) + 0
     = 7 + 3/1.584963 + 1/2 + 0
     = 7 + 1.892789 + 0.5
     = 9.392789

nDCG = 8.922960 / 9.392789 = 0.950
```

Four queries whose first relevant ranks are 1, 3, 2, and 4:

```text
MRR = (1 + 1/3 + 1/2 + 1/4) / 4 = (25/12) / 4 = 25/48 = 0.5208
```

Online, watch clicks, abandonment, and reformulation. Clicks pile up on whatever you already put first, so a raw click-through rate is a biased label. Use it to notice a regression, and keep the judgment set for the change itself.

## Capacity

Planning assumptions: 8,000,000 documents, 120 postings each, 6 bytes per posting, a dictionary of 1,500,000 terms at 48 bytes, 400 bytes of stored fields per document, one replica.

```text
Postings       = 8,000,000 * 120 = 960,000,000
Postings bytes = 960,000,000 * 6 = 5,760,000,000
Dictionary     = 1,500,000 * 48 = 72,000,000
Stored fields  = 8,000,000 * 400 = 3,200,000,000
One copy       = 5,760,000,000 + 72,000,000 + 3,200,000,000 = 9,032,000,000 bytes
               = 9,032,000,000 / 1024^3 = 8.412 GiB
Primary+replica = 2 * 9,032,000,000 = 18,064,000,000 bytes = 16.823 GiB
```

GiB figures are the byte counts divided by 1024^3, rounded to three decimals.

Four primary shards hold `9,032,000,000 / 4 = 2,258,000,000` bytes, which is 2.103 GiB each. A query that must hit every shard costs the same fan-out on each primary. If a load test shows one primary serves 500 queries/s inside the latency SLO, and the cluster takes 200 queries/s that all fan out, each primary sees 200 queries/s and the headroom is `500 / 200 = 2.5×`. The 500 is a test result you have to produce. It is not a property of the engine.

Vector memory, separate assumptions: 5,000,000 vectors, dimension 768, float32, and 32 int32 neighbor ids per vector for an HNSW graph.

```text
Vectors = 5,000,000 * 768 * 4 = 15,360,000,000 bytes = 14.305 GiB
Graph   = 5,000,000 * 32 * 4 = 640,000,000 bytes = 0.596 GiB
Copy    = 14.305 + 0.596 = 14.901 GiB
```

Those GiB figures are rounded to three decimals. A second replica is `2 * 16,000,000,000 = 32,000,000,000` bytes, which is 29.802 GiB, before document text and filters. Raising the HNSW candidate list or IVF `nprobe` spends latency to buy recall. Measure recall on the judgment set at the latency you will actually allow.

## Checklist

- [ ] The index is named as a projection, with an owner and a rebuild.
- [ ] The feed is the outbox or CDC, and the indexer upserts by id.
- [ ] Readers use a switchable name, so a rebuild does not stop queries.
- [ ] A shared index rejects queries that lack a tenant predicate.
- [ ] A ranking change quotes nDCG or MRR on a fixed judgment list, with the formula written down.

## Anti-patterns

- Treating the search cluster as the system of record.
- Reindexing in place under a write lock as the only way to change a mapping.
- A tenant filter the caller can omit.
- Returning hits the caller is not allowed to see, then filtering in the UI.
- Tuning BM25 from one screenshot. Shipping the change with no judgment list.
- An ANN index whose recall at the production candidate-budget was never measured.

## Related

- [CDC](cdc.md), [outbox](transactional-outbox.md), [idempotency](idempotency.md), [events](event-driven.md)
- [Data and keys](../tenancy/data-and-keys.md), [isolation](../tenancy/isolation-models.md), [AI systems](../ai/README.md)
- [CDC](../../patterns/cdc.md), [CQRS](../../patterns/cqrs.md), [outbox](../../patterns/transactional-outbox.md)

## Sources

- [Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25)
- [Elasticsearch](https://www.elastic.co/elasticsearch), [OpenSearch](https://opensearch.org/), [Apache Solr](https://solr.apache.org/)
- [HNSW paper](https://arxiv.org/abs/1603.09320), [Faiss indexes](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes), [pgvector](https://github.com/pgvector/pgvector)
- [Discounted cumulative gain](https://en.wikipedia.org/wiki/Discounted_cumulative_gain), [mean reciprocal rank](https://en.wikipedia.org/wiki/Mean_reciprocal_rank)
