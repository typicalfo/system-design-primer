---
title: "Evals and observability"
summary: "Score model and retrieval changes on versioned sets, and trace them with OpenTelemetry GenAI attributes that are still Development status."
tags: [ai, evals, observability, opentelemetry]
when_to_use: "Use when you need to know whether a prompt, model, or index change got better or worse, and what a production call cost."
related:
  - README.md
  - llm-app-architecture.md
  - rag.md
  - llm-security.md
  - ../observability/opentelemetry.md
  - ../observability/telemetry.md
  - ../observability/slos.md
  - ../delivery/cicd.md
  - ../compliance/privacy.md
last_reviewed: 2026-09-25
---

# Evals and observability

An eval is a test with a score instead of only a pass bit. It rots if the dataset, the prompt, the index, and the judge move independently. Observability tells you what production did: tokens, latency, errors, and which model id answered. Neither one is a security control. A high groundedness score does not mean the ACL held.

## Decide

| Practice | Use when | Avoid when |
|---|---|---|
| Offline golden set | You can label the right documents or the right answer, and you will version the set | You have ten hand-picked questions and you tune the prompt until those ten pass |
| Slices | The average hides a failure: language, doc type, no-answer, permission boundary | You only report one number for the whole corpus |
| Online sample plus feedback | The real questions are not in the golden set | You let thumbs-up replace the offline set. Feedback is biased toward people who bother to click |
| A/B on a prompt or model | You can split traffic and you have a cost metric beside the quality metric | The change affects authorization or retention. Those are not experiments |
| LLM-as-judge | You calibrated it against human labels on the slice you will gate | You need a guarantee about leakage or permissions. A model will not reliably grade those |
| CI threshold | The score is stable enough that a real regression clears the noise band | The metric flaps by more than your band on an unchanged build |

## Defaults

- Every scored run records the dataset version, prompt-template version, model id, embedding model id, and index snapshot. A number without those is not comparable to last week's number.
- Keep a permission-boundary slice: questions whose correct retrieval is empty for that user. A build that starts returning chunks there fails even if the average looks fine.
- Production traces sample. They are not the audit log. See [OpenTelemetry](../observability/opentelemetry.md) and [telemetry](../observability/telemetry.md).

## Offline, online, and gates

Offline evals run on a golden set you can rebuild. Store it like any other dataset: immutable versions, a changelog when you add or remove a case, and no customer document that has been deleted. When a [deletion](../compliance/retention.md) removes a source, it removes or rewrites the cases derived from it. Slices are filters on that set, reported separately, not one blended score.

Online evals sample live traffic. Sampling should keep errors and the permission-boundary path, not only the happy path. User feedback (a rating, a correction) is a label source with selection bias. Use it to propose new golden cases, not as the only gate. An A/B test of a prompt or a model needs a stop condition on quality and on cost per successful answer. Ship through the same flag path as any other change ([CI/CD](../delivery/cicd.md)).

An LLM-as-judge is another model call. Judges prefer the longer answer and the answer in a favored position when you show two at once. Pin the judge model id. Before a judge can block a release, score it against human labels on the same slice and write down the agreement you saw. Do not send the judge a broader corpus than the product model sees. The judge's prompt is also subject to injection from the answer it is grading.

RAG needs two families of metrics. Retrieval recall and precision at k, against labeled relevant chunks, tell you whether the right passage was available. Groundedness tells you whether the answer's claims are supported by the passages that were actually in the prompt. Citation accuracy is narrower: every cited id was retrieved, and the cited span supports the sentence. A high retrieval score with an ungrounded answer is a generator failure. A grounded answer from the wrong tenant's chunk is a filter failure, and it belongs on the permission slice, not in a quality average.

Regression gates in CI compare the new run to the pinned baseline on the same set. Set a floor (this slice must stay at or above X) and a noise band (a move smaller than Y does not fail the build). One flaky case should not page the team. A drop past the floor on the permission slice or on recall of the golden set should block promotion. Re-baseline only by changing the recorded baseline, not by rerunning until the number looks familiar.

## Tracing and dashboards

OpenTelemetry's GenAI semantic conventions use the attribute namespace `gen_ai.*`. As of 2026-09 the conventions document in the GenAI repository is status **Development**, not Stable. The previous pages under the core semantic-conventions site now say those documents have moved and are no longer maintained there. Development means the names can still change. Pin the convention version you emit and expect to revise it. Do not treat today's attribute list as a frozen contract.

The model-span conventions in that repository, still marked Development when this page was reviewed, include `gen_ai.operation.name`, `gen_ai.request.model`, `gen_ai.response.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, and cache-read usage attributes such as `gen_ai.usage.cache_read.input_tokens`. Emit those from the gateway so a dashboard can group cost and latency by model and tenant. Confirm the names against the repository before you add a new one. The same conventions discuss recording prompt and response content. Default to not recording it.

Dashboards, per tenant and per feature: tokens in, tokens out, cached tokens if the provider reports them, latency to first token, end-to-end latency, error rate, and estimated spend using the price in [LLM application architecture](llm-app-architecture.md). Alert on spend and on error rate against the SLO, not on a single slow call. See [SLOs](../observability/slos.md).

PII and document text do not belong on span attributes. Traces are sampled, retained on a different clock than the product, and often exported to a vendor. Redact at the collector the way the OpenTelemetry page describes. A tenant id attribute is acceptable when access to the trace backend is restricted to operators. A retrieved passage is not. If you must keep a debug sample, store it in a system with the same retention and access rules as the source, and delete it when the source is deleted ([privacy](../compliance/privacy.md)).

## Checklist

- [ ] The golden set has a version, and CI records that version next to the score.
- [ ] The permission-boundary slice fails the build when it regresses, independent of the average.
- [ ] The judge model id is pinned, and you have a written comparison to human labels before it gates a release.
- [ ] Retrieval recall and groundedness are separate numbers.
- [ ] Production traces do not contain raw prompts or document bodies by default.
- [ ] A dashboard shows tokens and estimated spend per tenant.

## Anti-patterns

- Editing the golden set in place so last month's score is no longer reproducible.
- Using the product model as the judge of its own answers with no human baseline.
- Failing CI on a 0.1 point move of a noisy metric, then ignoring the gate.
- Putting the full prompt on every span because the attribute existed in the convention.
- Treating a trace sample as proof that a deletion finished.

## Related

- [RAG](rag.md) for what the retrieval metrics are measuring
- [OpenTelemetry](../observability/opentelemetry.md), [SLOs](../observability/slos.md)

## Sources

- GenAI semantic conventions (status Development as of 2026-09): <https://github.com/open-telemetry/semantic-conventions-genai>
- Moved page on the core site: <https://opentelemetry.io/docs/specs/semconv/gen-ai/>
- Document status definitions: <https://opentelemetry.io/docs/specs/otel/document-status/>
