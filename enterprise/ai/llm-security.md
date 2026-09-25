---
title: "LLM security"
summary: "Treat model input and output as untrusted, and map the failures you build for to the OWASP GenAI lists by id."
tags: [ai, llm, security, owasp]
when_to_use: "Use when a design adds a model, retrieval, or an agent and you need the abuse cases and the official risk ids to cite."
related:
  - README.md
  - agents-and-tools.md
  - rag.md
  - ../security/threat-modeling.md
  - ../security/owasp-asvs.md
  - ../compliance/privacy.md
  - ../../pack/skills/threat-modeler/SKILL.md
  - ../../pack/skills/threat-modeler/reference/ai-threats.md
last_reviewed: 2026-09-25
---

# LLM security

The model is a fluent component that does not know your tenants. Anything it reads can redirect it, and anything it writes can be executed by a careless sink. Walk the data flow with [threat modeling](../security/threat-modeling.md). Use this page for the failures that show up once a model or an agent is on the diagram.

As of 2026-09 the OWASP GenAI project describes the 2026 LLM list as the current release (published 4 August 2026, per that project's repository). The 2025 ids are listed too: system prompt leakage is a 2025 title and is not a title on the 2026 list. Cite the edition with the id. Item names below are identifiers only. This page does not copy either list's wording. Both lists live on genai.owasp.org.

Application-security chapters for the surrounding system stay the [ASVS map](../security/owasp-asvs.md). Do not invent `V#.#.#` requirement ids.

## Decide

| Control | Use when | Avoid when |
|---|---|---|
| Separate instructions from retrieved data | The prompt contains documents, web pages, tool results, or other untrusted text | You have only a system prompt and a user question, and you still need the output checks below |
| Filter before the model sees data | The corpus is multi-tenant or permissioned | You plan to "instruct the model to respect ACLs" as the isolation mechanism |
| Encode and validate model output | The output is rendered, queried, or passed to a tool | The output is shown as inert text in a context that does not fetch URLs or interpret markup |
| Human gate on high-impact tools | The agent can pay, delete, send, or change access | The action is a read the user's own credential already allows |
| Spend caps | The caller can influence context length, retries, or tool loops | The only budget is the provider invoice at the end of the month |

## Defaults

- Direct prompt injection is the user typing instructions that override the task. Indirect injection is the same class of text arriving inside a document, a web page, a retrieval chunk, or a tool result. Assume both reach the model. The system prompt is not a boundary.
- Data exfiltration does not require the model to "hack" anything. Markdown or HTML it emits can contain an image or a link whose URL carries a secret, and a client that auto-loads remote images will send that secret. A tool that can send mail or HTTP can do the same with the secret in an argument. Render assistant output so remote images are not fetched, restrict link hosts, and deny tools that make arbitrary requests.
- Insecure output handling means the next component trusts the model. Encode for the sink you are in. Validate against a schema before a tool runs. Never `eval` model output, never build a shell command by concatenation, and never run model-written SQL as a privileged user.
- Excessive agency is a tool set wider than the task. Least privilege and approval gates are in [agents and tools](agents-and-tools.md).
- The system prompt will leak. Do not put credentials, cross-tenant policy, or unpublished vulnerability detail in it. Prefer checks in code.
- Supply chain covers the model, the embedding model, the dataset you fine-tune on, plugins, and MCP servers. Pin them, review them, and track them the way [software supply chain](../security/supply-chain.md) tracks other dependencies.
- Denial of wallet is unbounded consumption: long contexts, retry storms, agent loops, and a caller who is not the one paying. Quotas and loop budgets live in [LLM application architecture](llm-app-architecture.md).

## Identifier map

OWASP Top 10 for LLM Applications 2025, official titles:

| Id | Name |
|---|---|
| LLM01:2025 | Prompt Injection |
| LLM02:2025 | Sensitive Information Disclosure |
| LLM03:2025 | Supply Chain |
| LLM04:2025 | Data and Model Poisoning |
| LLM05:2025 | Improper Output Handling |
| LLM06:2025 | Excessive Agency |
| LLM07:2025 | System Prompt Leakage |
| LLM08:2025 | Vector and Embedding Weaknesses |
| LLM09:2025 | Misinformation |
| LLM10:2025 | Unbounded Consumption |

OWASP GenAI LLM Top 10 2026, official titles, current release as of 2026-09. Order and a few names differ from 2025. System prompt leakage is not a title on this list.

| Id | Name |
|---|---|
| LLM01:2026 | Prompt Injection |
| LLM02:2026 | Sensitive Information Disclosure |
| LLM03:2026 | Excessive Agency |
| LLM04:2026 | Supply Chain |
| LLM05:2026 | Data and Model Poisoning |
| LLM06:2026 | Unbounded Consumption |
| LLM07:2026 | Misinformation |
| LLM08:2026 | Hidden Context Exposure |
| LLM09:2026 | Vector and Embedding Weaknesses |
| LLM10:2026 | Improper Output Handling |

OWASP Top 10 for Agentic Applications 2026 (cover title of the December 2025 PDF; the project page titles the same document "OWASP Top 10 for Agentic Applications for 2026"). Names below are the glance-page forms. The PDF's section headings spell "and" in ASI02 and ASI03.

| Id | Name |
|---|---|
| ASI01 | Agent Goal Hijack |
| ASI02 | Tool Misuse & Exploitation |
| ASI03 | Identity & Privilege Abuse |
| ASI04 | Agentic Supply Chain Vulnerabilities |
| ASI05 | Unexpected Code Execution (RCE) |
| ASI06 | Memory & Context Poisoning |
| ASI07 | Insecure Inter-Agent Communication |
| ASI08 | Cascading Failures |
| ASI09 | Human-Agent Trust Exploitation |
| ASI10 | Rogue Agents |

How the failures on this page cite those ids:

| Failure on this page | Cite |
|---|---|
| Direct or indirect prompt injection | LLM01:2025 and LLM01:2026. When the injection redirects an agent's goals, also ASI01 |
| Disclosure of secrets or other tenants' data, including markdown or link exfiltration | LLM02:2025 and LLM02:2026. Tool-mediated exfiltration also ASI02 |
| Plugins, models, datasets, third-party servers | LLM03:2025 and LLM04:2026. For agents, ASI04 |
| Poisoned corpus, embeddings, or agent memory | LLM04:2025, LLM08:2025, LLM05:2026, LLM09:2026. For agent memory, ASI06 |
| Output passed into a sink that interprets it | LLM05:2025 and LLM10:2026. Code the agent runs, ASI05 |
| Tools wider than the task, or credentials broader than the user | LLM06:2025 and LLM03:2026. Also ASI02 and ASI03 |
| Secrets or private policy stuffed into the system prompt | LLM07:2025. Re-check the 2026 page before citing a replacement id |
| Spend, retries, or loops without a cap | LLM10:2025 and LLM06:2026 |

[NIST AI 600-1](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) is the Generative AI Profile of the AI Risk Management Framework (published 26 July 2024). Use it as the risk-management companion, not as a checklist of product settings. DOI: <https://doi.org/10.6028/NIST.AI.600-1>.

## Checklist

- [ ] Retrieved text and tool results are labeled untrusted, and the ACL filter runs before they enter the prompt.
- [ ] The UI does not auto-fetch images or other URLs from model output.
- [ ] No path evaluates model output as code or concatenates it into a command or a query.
- [ ] Tool allowlists, scoped credentials, and approval gates match [agents and tools](agents-and-tools.md).
- [ ] A per-tenant spend cap and a loop cap exist, and a test trips both.
- [ ] A review finding that cites an OWASP id also names the edition (2025 or 2026).

## Anti-patterns

- A longer system prompt as the mitigation for indirect injection.
- Hiding a document by omitting it from the citation list while leaving it in the context.
- Rendering assistant markdown with the same HTML pipeline as trusted admin content.
- Installing a third-party plugin or MCP server because the demo used it.
- Sharing one provider key across tenants so a single runaway loop spends everyone's quota.

## Related

- [RAG](rag.md), [agents and tools](agents-and-tools.md), [privacy](../compliance/privacy.md)
- [Threat modeling](../security/threat-modeling.md), [ASVS chapter map](../security/owasp-asvs.md)

## Sources

- [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/)
- [OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
- [OWASP Top 10 for Agentic Applications for 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [NIST AI 600-1 publication page](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- [AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
