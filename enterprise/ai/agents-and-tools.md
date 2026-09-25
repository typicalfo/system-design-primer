---
title: "Agents and tools"
summary: "Let an agent call tools only with the user's scoped credentials, a budget, and an audit record."
tags: [ai, agents, tools, mcp]
when_to_use: "Use when a model can call tools, run code, or reach an MCP server, and you must bound what those calls can do."
related:
  - README.md
  - llm-app-architecture.md
  - llm-security.md
  - ../identity/authorization-models.md
  - ../identity/service-to-service.md
  - ../data/idempotency.md
  - ../compliance/audit-logs.md
  - ../security/zero-trust.md
last_reviewed: 2026-09-25
---

# Agents and tools

An agent is a loop: the model proposes a tool call, your process runs it, the result goes back to the model. The damage is in the tool, not in the prose. Treat the model as an untrusted planner. The tool runs as the user, with a credential you minted for that call, or it does not run.

As of 2026-09 the Model Context Protocol specification site marks revision 2026-07-28 as latest. Read that revision for transport and authorization. Older write-ups of the HTTP transport describe shapes that revision changed.

## Decide

| Choice | Use when | Avoid when |
|---|---|---|
| Tools run as the user | The action is something that user could do in the product, and you can mint a short-lived credential for it | The agent needs a capability no user has. That is a separate privileged worker with its own approval, not a hidden admin key |
| Human approval on the exact arguments | The action is irreversible or high-impact: pay, delete, send, change permissions, deploy | You put an approval on "continue" and the model is free to change the arguments after the click |
| Sandbox for generated code | The model emits code you are willing to run | The sandbox has the network, the cloud credential, or the repository token "so the agent can finish" |
| First-party tools only | You can review every tool description and every permission | A user can paste an unreviewed third-party server into a production agent |
| MCP for a remote tool host | You want a standard tool protocol and will apply its HTTP authorization | You point a stdio server at a secret in the environment and call that "the OAuth design" |

## Defaults

- The agent acts on behalf of the user. Authorization uses that user's permissions, checked in the tool, on each call. See [authorization models](../identity/authorization-models.md) and [zero trust](../security/zero-trust.md).
- Credentials for a tool are scoped and short-lived. They are not the user's session cookie and not a service admin key. Prefer workload identity where two of your services call each other ([service-to-service](../identity/service-to-service.md)).
- The set of tools is an allowlist versioned with the release. A new tool is a review.
- Every tool call is logged: tenant, user, agent, tool name, approval id if any, idempotency key, and outcome. Arguments and results are redacted. The audit record follows [audit logs](../compliance/audit-logs.md). A trace is not a substitute.

## MCP

MCP is a protocol for a client (the agent host) to talk to a server that offers tools and resources. The specification defines two standard transports: stdio, for a subprocess the client launches, and Streamable HTTP, for a remote endpoint. Details and the 2026-07-28 changes are on the transports page linked below.

Authorization in that specification is optional and is written for HTTP transports. At a high level, a protected MCP server is an OAuth resource server, the MCP client is the OAuth client, and the server points the client at an authorization server. The spec builds that on OAuth 2.1 and on protected-resource metadata. Stdio is different: the spec tells implementers not to use that HTTP authorization flow for stdio, and to take local credentials from the environment instead. A local secret in the environment is still a secret. Scope it to the one server process, and do not reuse a production admin token as a convenience.

A third-party MCP server is someone else's code and someone else's instructions. Tool definitions are text the model will read. Tool poisoning is a definition, or a resource the server returns, that tells the model to ignore the user and do something else (exfiltrate the conversation, call a different tool, hide an action). Pin the server you reviewed. Do not let end users add servers to a production agent. Re-review when the tool list changes. Give the server a credential that can do only what those tools need.

## Gates, idempotency, and budgets

Irreversible or high-impact tools stop for a person. The approval record stores the tool name and the canonical arguments. Execution uses that record. A later model turn that edits the arguments needs a new approval. Low-impact reads can run without a person if the credential already limits them.

Tools that write take an idempotency key, scoped by tenant and tool, as in [idempotency](../data/idempotency.md). The agent host generates the key and stores it with the arguments. A retry of the loop must not pay, send, or delete twice.

Budgets stop the loop even when every individual call is allowed:

- Steps: a maximum number of model turns and tool calls.
- Tokens: counted across the loop, not per call only. See [LLM application architecture](llm-app-architecture.md).
- Wall clock: a deadline, after which the host cancels in-flight tool calls that are still cancellable.
- Spend: a cap in your unit of currency, using the price you assigned to the model and to any paid tool.

Loop detection is part of the budget. The same tool with the same arguments, or a step that does not change the observable state, repeats up to a small limit you set and then stops. The user sees that the agent stopped, and why.

Generated code runs in a sandbox: no default network, no cloud credentials, a wall-clock and memory cap, and a filesystem you can throw away. Leaving the sandbox is a tool of its own, with the approval rule above. The model does not get a shell on the host.

## Checklist

- [ ] You can name, for each tool, the permission it checks and the credential it receives.
- [ ] A third-party MCP server cannot be added to production without a review, and its token cannot reach unrelated tools.
- [ ] An approval is bound to the arguments that will run.
- [ ] A retried agent step with the same idempotency key does not double-apply a write.
- [ ] The loop stops on step, token, time, and spend budgets, and the stop is logged.
- [ ] Tool audit records redact secrets and document bodies.

## Anti-patterns

- One long-lived token that can read every tenant, attached to the agent "so tools work."
- Trusting a tool description because the server speaks MCP.
- Approving a plan in natural language and then executing whatever calls the model emits next.
- Running model-written code on the application host because the sandbox was slower.
- A loop with no step cap that retries a failing tool until the provider quota is gone.

## Related

- [LLM security](llm-security.md) for injection, tool-mediated exfiltration, and excessive agency
- [Audit logs](../compliance/audit-logs.md), [idempotency](../data/idempotency.md)

## Sources

- Model Context Protocol specification, revision 2026-07-28 (latest on the spec site as of 2026-09): <https://modelcontextprotocol.io/specification/2026-07-28>
- Transports: <https://modelcontextprotocol.io/specification/2026-07-28/basic/transports>
- Authorization: <https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization>
- Protocol entry point: <https://modelcontextprotocol.io/>
- Agentic risk identifiers, named and not quoted, are in [LLM security](llm-security.md).
