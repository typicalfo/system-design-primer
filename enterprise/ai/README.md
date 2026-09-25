---
title: "AI systems"
summary: "How to put a model behind a gateway, ground it with retrieval, constrain tools, and score the result."
tags: [ai, llm, index]
when_to_use: "Use when a design includes an LLM, a retrieval index, an agent, or an evaluation of model output."
related:
  - llm-app-architecture.md
  - rag.md
  - agents-and-tools.md
  - llm-security.md
  - evals-and-observability.md
  - ../reference-architectures/rag-assistant.md
  - ../tenancy/isolation-models.md
  - ../compliance/privacy.md
  - ../security/threat-modeling.md
  - ../apis/rate-limiting.md
last_reviewed: 2026-09-25
---

# AI systems

These pages are the production decisions around a model: who calls it, what it is allowed to see, what it is allowed to do, and how you know a change made it worse. They are not a model leaderboard. Vendor controls (retention switches, prefix caches, model aliases) move. As of 2026-09, follow the living source linked from the page rather than a paraphrase of a vendor feature.

## Read in this order

| Page | Decision |
|---|---|
| [LLM application architecture](llm-app-architecture.md) | Gateway, routing, fallbacks, token budgets, caching, and retention of prompts |
| [RAG](rag.md) | Ingestion, chunking, embeddings, hybrid retrieval, permissions, and deletion of every copy |
| [Agents and tools](agents-and-tools.md) | Tool authorization, MCP, approval gates, idempotency, and loop budgets |
| [LLM security](llm-security.md) | Injection, exfiltration, untrusted output, and the OWASP GenAI ids to cite |
| [Evals and observability](evals-and-observability.md) | Golden sets, judges, RAG metrics, and GenAI traces |

Then the worked design: [multi-tenant RAG assistant](../reference-architectures/rag-assistant.md).

## Nearby pages that already exist

- Tenancy: [isolation models](../tenancy/isolation-models.md), [data and keys](../tenancy/data-and-keys.md). A shared index is a pool. Say what a missing filter can leak.
- Privacy and deletion: [GDPR and CCPA basics](../compliance/privacy.md), [retention and deletion](../compliance/retention.md). Chunks, embeddings, caches, and eval sets are copies.
- Threats: [threat modeling](../security/threat-modeling.md), [ASVS chapter map](../security/owasp-asvs.md).
- Fairness of a shared provider quota: [rate limiting](../apis/rate-limiting.md), [noisy neighbors](../tenancy/noisy-neighbor.md).
- Traces in general: [OpenTelemetry](../observability/opentelemetry.md). The GenAI attribute namespace is still Development status. Details are on the evals page.

## Sources

The child pages cite their own sources. Start at the living ones:

- [OWASP GenAI Security Project](https://genai.owasp.org/)
- [NIST AI 600-1, Generative Artificial Intelligence Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- [Model Context Protocol specification](https://modelcontextprotocol.io/specification/2026-07-28)
- [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai)
