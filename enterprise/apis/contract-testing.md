---
title: "Contract testing"
summary: "Check producer and consumer agreements in CI so a shared staging environment is not the only integration test."
tags: [api, testing, contracts]
when_to_use: "Use when two deployables share an API or an event and can ship on different days."
related:
  - versioning.md
  - styles.md
  - ../data/schema-evolution.md
  - ../delivery/cicd.md
  - ../delivery/testing-strategy.md
last_reviewed: 2026-09-25
---

# Contract testing

A contract is the slice of behavior a consumer relies on: method, path or message type, required fields, and error shapes. Contract tests check that slice without standing up the whole system. End-to-end tests in a shared environment still have a place. They are slow, brittle, and late.

## Decide

| Approach | Use when | Avoid when |
|---|---|---|
| Schema compatibility (protobuf, Avro, OpenAPI diff) | The break is structural and a registry or a diff can see it | The break is semantic ("this field is now in cents"). A schema check will not catch it |
| Consumer-driven contract | Many consumers each rely on a different subset, and you want the producer to verify those subsets | There is one client you deploy yourself. A simpler integration test may be enough |
| Producer contract published for consumers | You own a public API and consumers test against your fixtures | Consumers invent expectations you never agreed to, and you treat their wish as binding |
| Record/replay of production | You need realistic payloads and you have scrubbed them | The recording contains personal data or the behavior under test is a write you must not replay |

## Defaults

- The contract lives in version control or a registry, reviewed when it changes.
- CI on the producer runs the consumer expectations, or runs a compatibility gate against the last released schema. A failure blocks the merge.
- CI on the consumer runs against a stub generated from the contract, so the consumer does not need the real producer to unit-test its parser.
- Include the error you actually return (`409` on idempotency conflict, `429` on limit), not only the happy JSON. For HTTP APIs that body is a problem-details document. See [API styles](styles.md) and [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457).
- Version the contract with the API. See [versioning](versioning.md).
- Pact-style broker workflows are one implementation. The requirement is the check, not the product. Use what the team will keep green.
- Semantic versioning of events and a fixture for the oldest reader you still support beat a thousand end-to-end UI tests for this particular risk.

## Checklist

- [ ] A field removal fails CI before deploy.
- [ ] At least one consumer test runs against a stub, so a producer outage does not empty the consumer pipeline.
- [ ] Fixtures contain no production personal data.
- [ ] The contract covers the authz failure mode if clients branch on it.

## Anti-patterns

- A staging environment called "the contract," broken by whoever deployed last.
- Consumer tests that duplicate the producer's implementation instead of the agreed responses.
- Ignoring contract failures to meet a release date, then debugging them in production with a partner.
- Schema checks only, while the money field silently changes units.

## Further reading

- [RFC 9457, Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457)
