---
title: "REST, gRPC, and GraphQL"
summary: "Pick one style per boundary from who the caller is, whether the shape is stable, and who pays for round trips."
tags: [api, rest, grpc, graphql]
when_to_use: "Use when two components must talk and you are choosing the contract style."
related:
  - versioning.md
  - gateways.md
  - contract-testing.md
  - ../data/schema-evolution.md
  - ../../patterns/api-gateway.md
  - ../../patterns/backend-for-frontend.md
---

# REST, gRPC, and GraphQL

The Primer contrasts REST and RPC: resources and verbs on public HTTP, procedures for tighter internal calls. gRPC is the usual modern RPC. GraphQL is a query language over HTTP that lets the client name the selection. None of them fixes a bad domain boundary.

Pattern context: [API gateway](../../patterns/api-gateway.md), [backend for frontend](../../patterns/backend-for-frontend.md). Primer anchors: [REST](../../README.md#representational-state-transfer-rest), [RPC](../../README.md#remote-procedure-call-rpc).

## Decide

| Style | Use when | Avoid when |
|---|---|---|
| REST or HTTP+JSON | Public or partner APIs, cacheable reads, broad client languages, resource-shaped domains | The client must assemble ten resources to paint one screen and you will not give them a composed endpoint |
| gRPC | Internal service-to-service calls, streaming, a schema you can check in CI, polyglot backends | A browser is the direct client, unless you add a translation layer. Human debugging of raw protobuf on the wire is worse than JSON |
| GraphQL | A product client needs to choose fields across a graph you are willing to make public, and you will enforce limits | You want a private database query tool exposed to the internet. Also avoid it as a chatty internal replacement for one gRPC method |
| Webhooks | You must tell another system about an event without them polling | The receiver must respond synchronously with business truth. That is an API call the other direction |

## Defaults

- One style per boundary. A service can speak REST outside and gRPC inside. It should not speak three styles to the same caller without a reason.
- Errors are stable and documented. HTTP status codes for HTTP. Richer error bodies with a code, a message safe to show, and a request id. Do not leak stack traces.
- Pagination is cursor-based when the list can change while someone pages. Offset pagination drifts and gets slow.
- Idempotency on creates that clients retry. See [idempotency](../data/idempotency.md).
- Timeouts and payload limits are part of the contract. A 50 MB JSON body is a decision, not an accident.
- GraphQL, if you use it: persisted queries or a depth and complexity limit, authorization per field or per object that can leak across tenants, and a plan for N+1 queries (loader batching).
- gRPC: deadlines on every call, and do not trust client-set deadlines blindly if they can pin a server. Version methods by package, not by editing a field's meaning.

## Anti-patterns

- REST that is a verb in the path for every operation (`POST /doTransfer`) with none of the caching benefits and all of the coupling. That can be fine. Do not also claim it is "RESTful" as a virtue.
- GraphQL as a gateway to every internal database table, with the client's query becoming your capacity plan.
- Exposing gRPC reflection and an admin service on the public port.
- Choosing a style because it is fashionable, then fighting it for the actual access pattern.
