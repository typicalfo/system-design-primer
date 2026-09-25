---
title: "Retrieval-augmented generation"
summary: "Index tenant documents into chunks and embeddings, retrieve with filters and hybrid search, and delete every copy."
tags: [ai, rag, retrieval, embeddings]
when_to_use: "Use when a model must answer from a corpus you control, and the answer has to respect tenant and document permissions."
related:
  - README.md
  - llm-security.md
  - ../compliance/privacy.md
  - ../compliance/retention.md
  - ../tenancy/data-and-keys.md
  - ../data/search.md
  - ../data/caching-at-scale.md
  - ../reference-architectures/rag-assistant.md
last_reviewed: 2026-09-25
---

# Retrieval-augmented generation

RAG answers from your documents. The model sees a small set of passages the retriever selected. Quality is mostly the retriever: what you chunk, what you filter, and what you delete. The model does not enforce access control. If a forbidden passage is in the prompt, the model can quote it.

Worked numbers for a multi-tenant assistant are in the [RAG assistant](../reference-architectures/rag-assistant.md) reference architecture. Lexical search mechanics sit in [search](../data/search.md). Cache lifetime and invalidation sit in [caching at scale](../data/caching-at-scale.md), [cache-aside](../../patterns/cache-aside.md), and [cache invalidation](../../patterns/cache-invalidation.md).

## Decide

| Choice | Use when | Avoid when |
|---|---|---|
| Structure-aware chunking | The source has headings, sections, tables, or records you can split on without cutting a unit in half | The file is a blob with no structure. You will invent boundaries the author did not write |
| Fixed size with overlap | Prose has no reliable structure, and you have measured that overlap recovers the cut sentence | You overlap so heavily that the index stores the corpus several times and recall barely moves |
| Hybrid retrieval (lexical plus vector) | Users search with rare identifiers, exact phrases, and paraphrases | The corpus is tiny and a single lexical index already returns the right page |
| Rerank a small candidate set | The first-stage list is recall-heavy and a second model can reorder a few dozen passages | You send the unfiltered candidate set, including other tenants' text, to a third-party reranker |
| Query-time ACL filter | Document permissions change, or users in one tenant do not all see the same documents | You are tempted to "tell the model what not to say" instead of removing the passage |
| Per-tenant index | A tenant's contract requires a separate store, or one tenant's volume dominates the shared index | You would operate thousands of tiny indexes and the failure mode is ops, not isolation |

## Defaults

- The source object is the system of record. Chunks, embeddings, lexical postings, and answer caches are derived. They can be rebuilt, and they must be deletable.
- Every derived row carries `tenant_id`, `document_id`, and a source version. The retriever sets `tenant_id` from the credential, never from the question text.
- Retrieve, then authorize, as one query: the filter is in the index request. A post-filter after a global top-k both under-fills the context and can send forbidden text to the next hop.
- Cite chunk ids that were actually in the prompt. Store those ids with the answer.

## Ingestion and chunking

Ingestion is a pipeline with a version: fetch the object, extract text, record the content hash, chunk, embed, and upsert into the lexical index and the vector index under the same document version. A failed embed leaves the previous version queryable. Do not delete the old chunks until the new version is committed.

Structure-aware splitting keeps a section, a heading path, and a table together, then breaks a long section into windows. Fixed windows are the fallback. Window size and overlap trade recall against index size. A larger window gives the model more local context and costs more tokens at answer time. Overlap exists so a sentence cut at the boundary still appears in one window. Overlap that approaches the window size stores nearly two copies. Pick the size with a labeled set, using the retrieval metrics in [evals and observability](evals-and-observability.md), and record the numbers in the index metadata.

Count windows explicitly. For token length L, window C, and overlap O, with stride S = C − O, the window count is 1 when L ≤ C, and otherwise ceil((L − C) / S) + 1. The same count is ceil((L − O) / S) for L > O. Re-check it when you change C or O. The reference architecture shows the arithmetic on one assumed corpus.

## Embeddings

Choose an embedding model for the languages and the document types you have, and pin the model id. Vectors from two models are not comparable, even at the same dimension. Changing the model, or the dimension, means a new index and a re-embed of every chunk you still serve. Dual-write the new index and cut reads over after the recall check passes. Do not mix old and new vectors in one nearest-neighbor list.

Storage for a raw float32 matrix is chunks × dimensions × 4 bytes. Quantized or graph indexes add or subtract from that. Size the extra from the engine you run. The raw figure is the lower bound for the vectors themselves, not the bill. Dimension and model id are part of the index name so a mistake fails at open time.

## Retrieval

Hybrid retrieval runs a lexical query (BM25 or the equivalent in your search engine) and a vector query, both with the same tenant and ACL filter, then fuses the two ranked lists. Reciprocal rank fusion scores a document as the sum, over each list, of 1/(k + rank), where k is a positive constant you freeze and then tune on labeled queries. The method is the one in Cormack, Clarke, and Buettcher's SIGIR 2009 paper, linked below. [Search](../data/search.md) walks a numeric example with k = 60. Fusion is not a reason to drop the filter on either list.

Rerank the fused candidates, on the order of a few dozen, and pass a smaller top set to the generator. The reranker sees passage text. It runs only after the filter. If the reranker is a third party, it is a subprocessor: region and retention belong in the design, next to [residency](../compliance/residency.md).

## Permissions, freshness, and deletion

Permission-aware retrieval filters at query time by the caller's current access, not by a hope that the model will refuse. Copying an ACL onto the chunk at index time goes stale when someone loses access. Either join to the current ACL in the query, or reindex on ACL change inside a lag SLO you measure.

Freshness is incremental. Upsert changed documents by content hash. A lagging event must not resurrect a deleted document: write a tombstone first, and teach the indexer to drop events older than the tombstone.

Right to erasure deletes the source object and every derivative: chunks, embeddings, lexical postings, exact-match and semantic answer caches, prompt-prefix caches you control, and copies sitting in eval sets. Backups either expire inside the retention window or cannot be restored into a serving index without re-applying tombstones. See [retention](../compliance/retention.md) and [privacy](../compliance/privacy.md). A verification job, given a deleted document id, expects zero rows in each of those stores. "We re-embedded last week" is not a verification.

## Grounding and citations

Return citations as chunk ids (and a span, if you have one) that were in the context. The product can show the passage. The model is instructed to rely on those passages. That instruction does not prove the sentence follows from them. Score groundedness separately from retrieval recall, on a set that includes questions with no supported answer. Wire those sets the way [evals and observability](evals-and-observability.md) describes, and keep deleted documents out of them.

Retrieved text is untrusted data. It can contain instructions aimed at the model. The control is still the filter, the tool policy, and output handling in [LLM security](llm-security.md), not a longer system prompt.

## Checklist

- [ ] A query for tenant A cannot return tenant B's chunk, including through the cache and the reranker.
- [ ] A user removed from a document stops retrieving it inside the lag you published.
- [ ] Changing the embedding model builds a new index rather than appending vectors.
- [ ] Deleting one document removes source, chunks, postings, vectors, caches, and eval copies, and a check confirms it.
- [ ] Cited chunk ids on a stored answer are a subset of the ids that were retrieved for that answer.

## Anti-patterns

- One shared index with the tenant id trusted from the user message.
- Retrieving a global top-k and then asking the model not to mention the other tenants.
- Re-embedding on every deploy because the pipeline has no content hash.
- Leaving deleted passages in a "golden" eval file because the file is in git and feels immutable.
- Overlap so large that you pay to embed the same paragraph many times and never measure recall.

## Related

- [LLM application architecture](llm-app-architecture.md) for the gateway, prompt cache, and token budget around the generator
- [Search](../data/search.md) and [caching at scale](../data/caching-at-scale.md)
- [RAG assistant reference architecture](../reference-architectures/rag-assistant.md)

## Sources

- Cormack, Clarke, and Buettcher, reciprocal rank fusion, SIGIR 2009: <https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf>
- [NIST AI 600-1, Generative Artificial Intelligence Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) (26 July 2024). DOI: <https://doi.org/10.6028/NIST.AI.600-1>
- Vector and embedding risks are named, not quoted, in the OWASP GenAI lists linked from [LLM security](llm-security.md).
