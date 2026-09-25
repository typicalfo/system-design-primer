---
name: threat-modeler
description: "Use this when turning a data-flow description into a STRIDE threat model: one row per element or trust boundary, with severity and a mitigation or an accepted risk."
---

# Threat modeler

Build a threat model from the data-flow description you were given. Do not invent components, trust boundaries, or attackers the description does not support. Read [reference/stride.md](reference/stride.md) and apply it. If the system calls a model, retrieves untrusted text, or lets a model invoke tools, also read [reference/ai-threats.md](reference/ai-threats.md).

The worksheet shape, when the user wants a filled document, is the [threat model template](https://github.com/typicalfo/system-design-primer/blob/master/templates/threat-model.md). The same walk is explained in [threat modeling](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/security/threat-modeling.md). License limits on outside sources are in [corpora/INDEX.md](https://github.com/typicalfo/system-design-primer/blob/master/pack/corpora/INDEX.md). Do not paste those sources.

## Steps

1. List external entities, processes, data stores, and data flows. Mark each trust boundary (user to edge, tenant to tenant, service to store, operator to production, CI to production, model to tool). If the description has no boundaries, write the list you can defend and stop after one finding: the model is incomplete. Do not fill six STRIDE rows per box to look finished.
2. For each element, and for each flow that crosses a boundary, ask the six questions in the STRIDE reference. Emit a row only when the abuse fits this design. Skip a letter that does not apply.
3. Set severity with the scale in the STRIDE reference. That scale matches the [design reviewer](https://github.com/typicalfo/system-design-primer/blob/master/pack/skills/design-reviewer/SKILL.md).
4. Every row ends in a mitigation you can point at, or an accepted risk with an owner and how you would notice it. "Be careful" and "use a WAF" are not mitigations for a missing authorization check.
5. Call out admin tools, exports, backups, and support impersonation if the description includes them. They are part of the model.

## Output

```markdown
# Threat model: <name>

## Boundaries
<One line per boundary you actually walked. Say which part of the description names it.>

## Threats

| Id | Element | Boundary | STRIDE | Threat | Severity | Mitigation or accepted risk |
|---|---|---|---|---|---|---|
| T1 | | | | | | |

## Open items
<Rows whose mitigation is still a promise. Cross-tenant disclosure and silent loss of promised data block release.>

## Accepted risks
<Owner, residual harm, and how you would notice. Write "None." if there are none.>
```

Rank the table from Critical down to Low. Within a severity, put the abuse that is hardest to undo first.
