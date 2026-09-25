---
title: "AI threat prompts"
summary: "Extra abuses to walk when a design calls a model, retrieves untrusted text, or lets a model invoke tools."
tags: [security, ai, threat-model]
when_to_use: "Use with the STRIDE reference when the data flow includes a model, a retriever, or a tool call."
related:
  - ../SKILL.md
  - stride.md
  - ../../../../enterprise/security/threat-modeling.md
  - ../../../../enterprise/ai/llm-security.md
last_reviewed: 2026-09-25
---

# AI threat prompts

These are questions, in this pack's words, for designs that send text to a model or let a model act. They do not replace STRIDE. They tell you which element to ask the six questions of. Do not copy catalogs from outside sites into the threat table. Name the abuse in this design.

Outside lists are indexed, with licenses, in [corpora/INDEX.md](https://github.com/typicalfo/system-design-primer/blob/master/pack/corpora/INDEX.md). The OWASP LLM and agentic lists linked from that index are CC BY-SA. Link them. Do not paste them.

## What to add to the diagram

- The caller, and whether their text is instructions, data, or both.
- The retriever and the corpus it can see, including other tenants' documents if the index is shared.
- The model endpoint, and who operates it.
- Each tool: the credential it uses, the side effect, and whether a retry repeats that side effect.
- The log, the trace, and the vendor's retention of prompts. Those are stores.

## Abuses to consider

**Untrusted text is obeyed.** A document, a ticket, a web page, or a tool result can contain instructions. If the architecture does not separate that text from the system instructions, the model will treat it as orders. Ask spoofing and elevation on that flow.

**Confused deputy.** The tool's credential is often broader than the person who typed the prompt. A request to read another tenant succeeds when the tool does not check authorization again. Ask information disclosure and elevation on every tool.

**Copies of sensitive data.** The prompt, the retrieved chunk, the log line, and the vendor's stored request are copies. Encryption of the application database does not cover them. Ask disclosure on each copy.

**Output used as code.** Model text placed into HTML, SQL, a shell, or a policy document is an injection. Ask tampering on the consumer of the output.

**Too much agency.** A tool that sends mail, moves money, deletes, or deploys needs a check on the irreversible step, by a policy or a person. A retry of a tool that is not idempotent is a second side effect. Ask elevation and tampering.

**Cost and availability.** A loop of long prompts or tool calls spends the quota and the budget. Cap tokens, steps, and concurrency per caller. Ask denial of service, including denial you pay for.

**Supply chain of the model path.** The model version, the system prompt, the index, and each plugin are dependencies. Changing the prompt is a release. Ask tampering on that path.

**Training and fine-tune data.** A secret or one customer's records in a training set can come back out. Do not put them there. Ask disclosure on the training store if the design has one.

## Severity

Use the scale in [stride.md](stride.md). Cross-tenant retrieval and a tool that writes with a shared admin credential are Critical when the path is likely. An unbounded prompt loop that only spends money is High when one caller can run it, and Low when a hard cap already holds.

## What not to write

- "The model is non-deterministic" as a threat, with no element and no harm.
- A mitigation that is only "a stronger model."
- A pasted list of ten items that this design does not contain.
