---
title: "LLM application architecture"
summary: "Put a gateway in front of model providers, and bound cost, latency, failover, and what data leaves the tenant."
tags: [ai, llm, gateway, cost]
when_to_use: "Use when a product calls a model provider and you must choose routing, fallbacks, budgets, caching, and what is logged."
related:
  - README.md
  - rag.md
  - agents-and-tools.md
  - llm-security.md
  - ../apis/rate-limiting.md
  - ../reliability/retries-timeouts.md
  - ../data/idempotency.md
  - ../cost/unit-economics.md
last_reviewed: 2026-09-25
---

# LLM application architecture

An LLM feature is a remote call with a variable price, a variable latency, and a copy of the prompt leaving your process. The gateway is the place that makes those three things explicit. Application code asks for a task ("answer this question", "embed this passage"). The gateway picks a model, enforces the tenant's budget, and records what ran.

Provider features move quickly. As of 2026-09, treat any claim about a vendor's cache, retention switch, or model alias as stale until someone re-reads that vendor's current docs. This page is the shape of the control, not a catalog of products.

## Decide

| Choice | Use when | Avoid when |
|---|---|---|
| One gateway in front of every provider | More than one service calls a model, or you need a quota, a kill switch, or an audit trail | A single batch job whose only caller is the team that owns the key, and a gateway would be a second deploy with no second caller |
| Route by task, with a cost and latency class | Classification, embeddings, and long answers have different prices and different SLOs | You want one "best" model for every call. You will overpay for the cheap tasks |
| Pin a model version on paths that must be reproducible | Evals, regulated answers, or a prompt you have scored | The provider only offers a moving alias and you have an eval gate in front of alias changes |
| Fallback to a second provider | The feature must degrade when the primary errors or hits a quota | The fallback lacks a capability the call requires (tools, schema, images). A silent drop is a behavior change |
| Exact-match response cache | The same tenant, model, and canonical prompt recur, and a stale answer is acceptable for a TTL you named | The answer depends on live authorization or on a corpus that changed since the cache write |
| Semantic cache | Near-duplicate questions are common, the domain tolerates a wrong neighbor, and the key includes the tenant | Permissioned retrieval, or any case where a near miss is worse than a cache miss |
| Provider prompt-prefix cache | The provider offers one and the prefix is stable | You are using it as an isolation or retention boundary. It is a bill control |

## Defaults

- All application traffic goes through the gateway. The provider credential lives there, not in each service.
- The gateway's request log stores tenant id, caller, task class, model id that actually ran, token counts, latency, and whether the response was cached. It does not store the raw prompt by default.
- Every call has a max output tokens, a deadline, and a tenant budget. A missing budget is a bug, not an unlimited plan.
- Record the prompt-template version and the model id on the stored answer so you can reproduce or invalidate it.

## Routing, failover, and abstraction

Route on the task, then on cost and latency. A short classification call and an embedding call should not share a route with a long grounded answer. Write the policy as data: task, maximum input tokens, maximum output tokens, latency class, and whether the call is allowed to leave a region or to use a provider that trains on customer content.

Keep a small provider interface: complete, stream, embed. Capabilities sit beside it (tools, structured output, images, prefix caching). When the primary fails, the gateway may send the call to the next provider on the same route only if that provider advertises every capability the call set. Otherwise fail the request. Feature drift across providers is normal. An abstraction that pretends the intersection is the union will drop tools and still return prose.

Pin production routes to a model identifier the provider promises not to move silently. If the only name you can call is an alias, record the concrete id returned on the response, and promote a new alias only after the eval gate in [evals and observability](evals-and-observability.md). A fallback model is a different quality. Say so in the product, or keep the fallback for outage only and surface the degradation.

## Budgets, limits, and caching

Attribute spend to a tenant and a feature. The unit is tokens in, tokens out, and the price you assumed for that model, written next to the real invoice when it arrives. See [unit economics](../cost/unit-economics.md).

- Per tenant: a token quota per day or per month, and a concurrent-request cap. Exhaustion returns a specific error the product can show. It does not queue forever.
- Per request: max input tokens (reject or truncate with a recorded flag) and max output tokens.
- Per provider account: the provider's tokens-per-minute and requests-per-minute quotas are a shared pool. Put a per-tenant token bucket in front of that pool so one tenant cannot consume the whole TPM. A global bucket sits at the provider limit. When it is empty, shed by the priority you wrote down. See [rate limiting](../apis/rate-limiting.md) and [noisy neighbors](../tenancy/noisy-neighbor.md).

Exact-match cache key: tenant, model id, template version, sampling parameters, and a hash of the canonical messages. For a RAG answer, include a fingerprint of the retrieved chunk ids. TTL is a product decision. Invalidate on corpus deletes for that tenant rather than waiting out the TTL when the answer could cite removed text.

A semantic cache returns a previous answer for a nearby embedding. Near misses are wrong answers. The key still includes the tenant. Do not share entries across tenants. For permissioned corpora, prefer a miss over a neighbor hit.

Provider prompt caching, where a vendor offers it, charges less for a repeated prefix. The match is on the prefix, so a change at the start of the prompt misses. Confirm, in that provider's current docs, what is stored and for how long. It does not separate tenants for you. Your gateway still isolates.

## Calls, timeouts, and data handling

Streaming is the default for interactive answers so the deadline is time-to-first-token plus a cap on the stream, not one silent wait for the full body. If the client disconnects, cancel the upstream call. Tokens already generated still count against the budget.

Timeouts follow [retries and timeouts](../reliability/retries-timeouts.md). Generation is not idempotent at the provider: a retry after the provider accepted the call can bill you twice and produce a second answer. The gateway stores an idempotency key for the client request, as in [idempotency](../data/idempotency.md). Same key and same body returns the stored completion. Same key and a different body returns a conflict. Retry the provider only when the attempt failed before any acceptance you cannot see (connection error with no response), and the key is still in progress under a lock. A timeout after tokens started is a failure returned to the client, not a second call.

Data handling is a route property. Redact identifiers you do not need before the prompt is built, and keep the redaction in your process. Retention is whatever the provider's current setting actually covers: prompts, outputs, embeddings, and abuse-monitoring exceptions are different switches. A setting named zero data retention or no-training often still has an exception. Read it. Do not send a tenant's content on a route whose retention is wider than the contract.

## Checklist

- [ ] Every model call in production is visible on the gateway, with tenant, model id, and token counts.
- [ ] A tenant quota and a per-request max tokens are enforced, and the error is distinct from a provider 429.
- [ ] Fallback routes declare required capabilities and fail closed when the backup lacks one.
- [ ] The exact-match cache key includes the tenant. A test writes as tenant A and reads as tenant B and gets a miss.
- [ ] Client retries of one completion do not create a second billed provider call.
- [ ] The route's retention setting matches the contract for that data class.

## Anti-patterns

- A provider SDK and a long-lived key inside each service, with spend visible only on the monthly invoice.
- Retrying a timed-out generation with backoff until one returns, and counting each attempt as one user request.
- Caching answers on the prompt text alone, so two tenants with the same question share an answer.
- A "provider-agnostic" client that drops tool calls on failover and still marks the response successful.
- Logging full prompts in application logs because the gateway already redacts its own log.

## Related

- [RAG](rag.md), [agents and tools](agents-and-tools.md), [LLM security](llm-security.md), [evals and observability](evals-and-observability.md)
- [Rate limiting](../apis/rate-limiting.md), [idempotency](../data/idempotency.md), [unit economics](../cost/unit-economics.md)

## Sources

- [NIST AI 600-1, Generative Artificial Intelligence Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) (publication page, 26 July 2024). DOI: <https://doi.org/10.6028/NIST.AI.600-1>
- [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai) for the `gen_ai.*` usage attributes the gateway should be ready to emit. Status is covered in [evals and observability](evals-and-observability.md).
