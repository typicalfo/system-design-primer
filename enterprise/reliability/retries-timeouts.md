---
title: "Retries, backoff, and timeouts"
summary: "Bound every remote call with a timeout, and retry only idempotent work with jittered backoff."
tags: [reliability, retries, timeouts, backoff]
when_to_use: "Use when a caller depends on a network hop that can be slow, dropped, or temporarily unavailable."
related:
  - circuit-breaker-bulkhead.md
  - load-shedding.md
  - ../data/idempotency.md
  - ../apis/rate-limiting.md
  - ../../patterns/retry-with-backoff.md
  - ../../patterns/idempotency-keys.md
---

# Retries, backoff, and timeouts

A timeout is how long you will wait before you give up. A retry is another attempt after you gave up or got a retryable error. Without a bound, a slow dependency becomes a slow process, then a stuck fleet, then a retry storm.

## Defaults

- Every remote call has a timeout shorter than the caller's own deadline. Leave budget for the caller to return a controlled error.
- Deadlines propagate. A request that has 50 ms left does not start a 2 s downstream call.
- Retry only when the call is safe to repeat: a read, or a write protected by an [idempotency key](../data/idempotency.md). If you are not sure, do not retry automatically.
- Retry on timeouts, connection resets, and explicit overload responses (`429`, `503`). Do not retry `400` or `403`.
- Exponential backoff with full jitter: sleep a random fraction of the growing cap so clients do not retry in lockstep. Cap the number of attempts and the total time.
- Honor `Retry-After`. A client that retries faster than the server asked is part of the incident.
- A retry budget per client (for example, only 10% extra attempts) stops a partial failure from multiplying load.
- Idempotency storage must outlive the retry window. A key that expires while the client is still retrying creates a duplicate.

The pattern card is [retry with backoff](../../patterns/retry-with-backoff.md).

## Decide

| Symptom | Response |
|---|---|
| Downstream is timing out and your success rate is falling | Shorten timeouts, shed, open the circuit. Do not add retries first |
| A single dropped response on an otherwise healthy dependency | One or two jittered retries are appropriate |
| Error says the request was invalid | Fail the caller. Retrying will not change the bytes |
| Queue consumer crashed after a partial side effect | Retry is correct only if the side effect is idempotent or transactional |

## Checklist

- [ ] No call uses an infinite timeout or a library default you have not read.
- [ ] The write path documents whether a retry can double-charge, double-send, or double-insert.
- [ ] Client and server clocks are not required for backoff. Use durations, not absolute timestamps, unless you also handle skew.
- [ ] Load tests include a dependency that returns slow `503`s, and the caller's concurrency stays bounded.

## Anti-patterns

- Immediate retries in a loop, three layers deep (browser, gateway, and service), so one failure becomes dozens of calls.
- The same timeout for a metadata lookup and a multi-gigabyte export.
- Treating "at least once" delivery as "exactly once" because you retry until the log line says success.
- Cancelling the client request and letting the server continue a payment anyway, with no idempotency key to reconcile.
