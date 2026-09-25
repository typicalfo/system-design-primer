---
title: "Idempotency"
summary: "Make a retried request return the original result, and reject the same key when the body differs."
tags: [data, idempotency, api]
when_to_use: "Use when a client, a queue, or a saga may send the same write more than once and a duplicate effect would be wrong."
related:
  - sagas.md
  - transactional-outbox.md
  - event-driven.md
  - ../reliability/retries-timeouts.md
  - ../apis/webhooks.md
  - ../../patterns/idempotency-keys.md
---

# Idempotency

At-least-once delivery and automatic retries will repeat writes. An idempotent handler makes the repeat a no-op that returns the same outcome. It does not make two different requests the same just because they share an id.

Pattern card: [idempotency keys](../../patterns/idempotency-keys.md).

## Defaults

- The client sends an idempotency key on unsafe methods (`POST` payment, `POST` order). Scope the key by tenant and operation, not globally.
- Store the key, a hash of the canonical request, the response status and body, and the expiry. Do this in the same transaction as the side effect, or reserve the key before the side effect with a state machine (`in_progress`, `completed`).
- Same key and same request: return the stored response. Do not run the side effect again.
- Same key and different request: return `409`. Do not apply the second body.
- A key still `in_progress` when a retry arrives: return `409` or `425` with a retry hint, or wait briefly. Do not start a second execution.
- Keep the record longer than the client's retry budget and longer than broker redelivery. A day is a common default for payments. Shorter is fine for low-stakes creates if you have measured the retry window.
- Natural idempotency is better when you have it: a unique constraint on `(tenant, external_ref)`. The key store is for cases without a natural key.
- Updates that are "set status to shipped" can be idempotent without a client key if the transition is guarded (`WHERE status = 'packed'`).

## Decide

| Approach | Use when | Avoid when |
|---|---|---|
| Unique constraint on a business key | The domain already has an external id | The only identifier is "whatever the client generated once," and you still need the original HTTP response |
| Idempotency-Key store | HTTP creates that must return the original body | A purely internal state transition that a conditional write already protects |
| Dedup table on consumer | Events may be redelivered | You dedupe in memory only. A restart forgets |

## Checklist

- [ ] The key store and the side effect commit together, or the `in_progress` fence is correct under two concurrent requests.
- [ ] Expiry cannot delete a key while a payment provider might still call you back.
- [ ] The response replay does not leak another tenant's body. The lookup includes tenant id.
- [ ] GET remains safe. You do not require idempotency keys on reads.

## Anti-patterns

- Hashing the entire request including a timestamp, so every retry looks new.
- Returning success on a duplicate without storing the result, when the first attempt actually failed after the client timed out.
- One global key space so tenant A's key collides with tenant B's.
- Idempotent receiver and a non-idempotent side effect (send email, charge card) inside it.
