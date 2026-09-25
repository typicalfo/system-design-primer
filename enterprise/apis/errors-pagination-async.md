---
title: "Errors, pagination, and async operations"
summary: "Return problem details with a stable type, page with opaque cursors, and point long work at a status resource."
tags: [api, errors, pagination, async]
when_to_use: "Use when you are fixing the contract for failures, list pages, or work that will not finish inside the request."
related:
  - styles.md
  - webhooks.md
  - rate-limiting.md
  - realtime.md
  - ../data/idempotency.md
  - ../data/sagas.md
  - ../reliability/retries-timeouts.md
  - ../../patterns/idempotency-keys.md
last_reviewed: 2026-09-25
---

# Errors, pagination, and async operations

Clients retry what they cannot tell apart. A body that changes shape per endpoint, a page that skips rows, and a request that times out while the server keeps working are the same bug: the contract does not say what happened or what to do next. [API styles](styles.md) already picks HTTP status codes and names problem details. This page is the shape of that body, of lists, and of work that outlives the connection.

## Decide

| Mechanism | Use when | Avoid when |
|---|---|---|
| Problem details (`application/problem+json`) | The caller is a program and will branch on the error | The response is a browser HTML page. Use the problem document for APIs |
| Cursor pagination | The list can change while someone pages, or the page number gets large | The collection is tiny, stable, and you truly need "jump to page 40" |
| Offset pagination | You need a page number on a small, quiet collection | The table is large or writers are active. Offset still walks the skipped rows |
| `202` plus a status resource | The work can outlast the HTTP timeout | The work finishes in a few hundred milliseconds. Return the result |
| A webhook as the completion signal | The client cannot poll, or you already deliver [webhooks](webhooks.md) | The webhook is the only record. Deliveries are at-least-once and sometimes lost |
| A bulk endpoint | The client must submit many items and can handle per-item results | One item failing should fail the whole business transaction. Use one request or a [saga](../data/sagas.md) |

## Problem details

[RFC 9457](https://www.rfc-editor.org/rfc/rfc9457) defines a problem-details document and obsoletes RFC 7807. For JSON APIs the content type is `application/problem+json`. The members are:

| Member | Role |
|---|---|
| `type` | A URI that identifies the problem class. Clients branch on this string. They do not need to fetch it to handle the error |
| `title` | A short, stable summary of that class. Do not put the occurrence's specifics here |
| `status` | The HTTP status. It matches the response status |
| `detail` | What happened this time, safe to show the caller |
| `instance` | A URI for this occurrence, often a request id the operator can find |

`about:blank` is the type RFC 9457 registers for "no more specific type than the HTTP status." Prefer a stable type of your own once the client must distinguish two 400s. Extension members carry safe extras (a retry hint, a field name). Do not put stack traces, SQL, internal host names, or another tenant's data in `detail` or in extensions.

```json
{
  "type": "https://example.com/problems/out-of-stock",
  "title": "Item is out of stock",
  "status": 409,
  "detail": "SKU 1842 has 0 on hand.",
  "instance": "/requests/01J9Z",
  "sku": "1842"
}
```

Treat `type` as an API. Renaming it is a break. See [versioning](versioning.md).

## Retryability

Say whether a retry can help. Honor `Retry-After` ([RFC 9110](https://www.rfc-editor.org/rfc/rfc9110)). The retry rules live in [retries and timeouts](../reliability/retries-timeouts.md).

| Status | Retry on its own? | Client action |
|---|---|---|
| 400, 404, 409, 422 | No | Fix the request. A blind retry sends the same mistake |
| 401, 403 | No, until credentials change | Refresh a token once if you know it expired. Do not loop on 403 |
| 408, 429, 500, 502, 503, 504 | Only if the operation is safe to repeat | Wait for `Retry-After` when it is present, then back off. [Rate limiting](rate-limiting.md) is why 429 exists |
| 202 | The request was accepted, not finished | Poll the status resource. Do not resubmit as if the first attempt vanished |

Unsafe methods retry only with an [idempotency key](../data/idempotency.md). A 500 after a charge may have charged.

## Pagination

Offset asks for "skip 199,950, then take 50." Cursor asks for "the next 50 after this key."

Page size 50, page 4,000:

```text
Rows skipped = (4,000 - 1) * 50 = 199,950
```

A naive `OFFSET 199950` still reads and discards those rows. The cost grows with the page number. A cursor seeks an index at the last sort key.

Defaults:

- The cursor is opaque. Clients send it back. They do not parse it.
- The sort is totally ordered. A timestamp alone ties. Use `(created_at, id)` or another unique key so a row is not duplicated or skipped when values collide.
- The filter and the sort are fixed for the life of the cursor. Changing the filter means a new query, not an edited cursor.
- Sign or MAC the cursor if a client could otherwise widen it. The signature is not authorization. The tenant and the ACL are still applied on the server for every page.
- Publish a default page size and a maximum. Reject a larger `limit` with a problem document. Do not silently cap and return a cursor that looks complete.
- Say what a live collection does. Inserts behind the cursor can be missed. Deletes can open gaps. A snapshot (one read view for the whole walk) is the stronger promise and costs a snapshot. "May skip or duplicate under concurrent writes" is an acceptable promise if you write it down.

## Long-running operations

[RFC 9110](https://www.rfc-editor.org/rfc/rfc9110) defines `202 Accepted`: the request has been accepted and processing has not finished. Acceptance is not success. HTTP will not later call the client back with the real status.

Return `202` with a `Location` header, or the same URL in the response body, pointing at a status resource: `queued`, `running`, `succeeded`, `failed`, or `canceled`. The client polls that resource. Put `Retry-After` on the poll response while the job is unfinished so clients do not busy-loop.

A [webhook](webhooks.md) can say the job finished. Keep the status resource anyway. Webhook delivery is at-least-once and can be down. The status resource is the record.

Cancellation is its own idempotent call. It stops work that has not happened. It does not undo a charge that succeeded. That undo is a compensation. See [sagas](../data/sagas.md).

Expire the result. Document the TTL. After it, the status resource returns `404` or `410`. A client that still holds an idempotency key inside that key's lifetime gets the stored outcome. After both are gone, a retry is a new operation. Store the idempotency record at least as long as the result.

## Bulk operations

Bound the request by item count and by bytes. Reject the whole request when either cap is exceeded, before any item runs. Planning example: max 100 items and 1 MiB. At 2 KiB average, 100 items are:

```text
100 * 2 * 1,024 = 204,800 bytes = 200 KiB
```

which is under 1 MiB (`1,048,576` bytes). A client that sends 1,000 such items sends:

```text
1,000 * 2,048 = 2,048,000 bytes = 1.953 MiB
```

which is over the cap. That request is a `413` or a `400` problem, not a partial apply.

When the batch is accepted, the body lists one result per input item: the item's id, its status, and a problem document if it failed. The top-level status means "the batch was processed and the list is authoritative." It does not mean every item succeeded. A retry of the batch uses an idempotency key for the batch, and each item write is idempotent so a replay does not repeat a success. See [idempotency keys](../../patterns/idempotency-keys.md).

Do not fail the HTTP call after committing half the items and leave the client to guess which half. If you did commit some, the response still lists them.

## Checklist

- [ ] Errors are `application/problem+json` with a stable `type` and no stack trace.
- [ ] Retryable statuses are documented, and `Retry-After` is set when you want the client to wait.
- [ ] Lists use an opaque cursor over a unique sort, with a max page size.
- [ ] Work that outlives the request has a status resource, a poll hint, and a result TTL.
- [ ] Bulk responses have a per-item status. Over-size batches are rejected up front.
- [ ] Creates and batches that clients retry carry an idempotency key.

## Anti-patterns

- A different error JSON on every endpoint, plus the exception text in production.
- `type` values that include a sentence, a timestamp, or a user id.
- Offset pagination on a table that grows, exposed as `page=4000`.
- A cursor the client is told to build from a timestamp with no tie-break.
- Returning `200` with an empty body while a job runs, or `202` with nowhere to look.
- A bulk `200` that hides three failed items.
- Retrying a bulk request so the successful items run twice.

## Related

- [API styles](styles.md), [versioning](versioning.md), [webhooks](webhooks.md), [rate limiting](rate-limiting.md), [gateways](gateways.md), [realtime](realtime.md)
- [Idempotency](../data/idempotency.md), [sagas](../data/sagas.md), [retries](../reliability/retries-timeouts.md)
- [Idempotency keys](../../patterns/idempotency-keys.md)

## Sources

- [RFC 9457, Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457)
- [RFC 9110, HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)
