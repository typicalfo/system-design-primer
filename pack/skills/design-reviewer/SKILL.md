---
name: design-reviewer
description: "Use this when reviewing a proposed software architecture or system design for production gaps: single points of failure, cache invalidation, consistency, 10x load, failure modes, authentication and authorization, OWASP ASVS, compliance, observability, retention, cost, migration, and team boundaries."
---

# Design reviewer

Review the design you were given. Do not redesign it from scratch. Read [checklist.md](checklist.md) and walk every section. The checklist is the whole review procedure. Links from this folder to the rest of the repo use GitHub URLs so a copied skill still opens them. Supporting sources and their licenses are in [corpora/INDEX.md](https://github.com/typicalfo/system-design-primer/blob/master/pack/corpora/INDEX.md); follow those links when a finding depends on them, and do not paste their text.

The Primer's own security note is only: encrypt in transit and at rest, sanitize input, parameterize queries, least privilege. That is not this review. Identity, ASVS, audit, retention, on-call, cost, migration, and ownership come from the checklist. The checklist links to the [enterprise guide](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/README.md) and the [pattern cards](https://github.com/typicalfo/system-design-primer/blob/master/patterns/README.md). Chapter names for ASVS 5.0.0 are also listed in [enterprise/security/owasp-asvs.md](https://github.com/typicalfo/system-design-primer/blob/master/enterprise/security/owasp-asvs.md). Do not copy requirement text.

## What a finding is

A finding is a specific gap in this design: something the design says that fails a check, or something a check requires that the design never decides. Quote or paraphrase the part you are judging. Skip a check that the design already satisfies, and skip a check that does not apply (no cache, no multi-team split, no browser). Do not emit a passing grade per check.

Severity:

- **Critical.** A likely path to cross-tenant or cross-customer data exposure, silent loss of data the design promised to keep, or an unauthenticated write to the source of truth.
- **High.** A missing control that breaks a stated requirement under a fault the design should expect (instance loss, bad deploy, retry, one overloaded key).
- **Medium.** Holds at the stated load, and breaks at 10×, during migration or rollback, or under a fault the design names but does not finish.
- **Low.** Cost, clarity, or operability. The design still meets its requirements.

Rank the list from Critical down to Low. Within a severity, put the issue that is hardest to undo first.

## Output

```markdown
# Design review: <name>

## Findings

### 1. <short title>
- Severity: Critical | High | Medium | Low
- Area: <checklist section>
- Evidence: <what the design says or leaves undecided>
- Why it matters: <the failure, in operational terms>
- Change: <one design change, specific enough to edit the doc>
- ASVS: <v5.0.0 chapter, only when the area is a security control>

## Accepted risks
<Risks the design already names, that you are willing to leave. Write "None." if there are none.>
```

ASVS citations use chapters from the checklist map, for version 5.0.0. Do not invent requirement ids. If the exact requirement sentence matters, say it was not verified and link the standard from the corpora index.

If the design is an empty outline, say so and stop after the first finding. Review what is written.
