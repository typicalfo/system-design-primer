---
title: "Software supply chain"
summary: "Know what you build, produce an SBOM, sign the artifact, and deploy only what you verified."
tags: [security, sbom, slsa, signing, supply-chain]
when_to_use: "Use when a pipeline builds an artifact that production will run, or when you take a dependency you did not write."
related:
  - owasp-asvs.md
  - ../identity/secrets.md
  - ../delivery/cicd.md
  - ../delivery/iac-environments.md
  - ../../pack/corpora/INDEX.md
  - post-quantum.md
last_reviewed: 2026-09-25
---

# Software supply chain

The supply chain is everything that can change what production runs: source, dependencies, the build, the registry, the deploy, and the running cluster. A vulnerability scanner on a laptop image is one control, not the chain.

## Decide

| Choose | Use when | Avoid when |
|---|---|---|
| SBOM per artifact (SPDX or CycloneDX) | You ship software and must answer "what is in this build" during an incident | You generate an SBOM and never store it with the digest it describes |
| Signed artifacts (keyless sigstore-style or a managed key) | Production should refuse images and packages it cannot verify | The signing key lives in the same repo as the code and every developer can use it |
| Isolated, hermetic builds | You want provenance that says which source and which builder produced the digest | The build pulls unpinned tools from the network as root on a shared runner |
| Dependency pinning and review | Libraries and base images move under you | A floating `latest` tag is how you "stay patched." Patch by rebuilding a pin |
| SLSA-style provenance | A customer or an internal policy asks how the artifact was built | You paste a level number into a slide without a generator that emits the attestation |

[SLSA](https://slsa.dev/) describes levels of build integrity and provenance. Use the project documentation when you need the level definitions. This page does not copy that spec. Prefer the properties: source is identified, the build runs in isolation, the provenance is signed, and deploy checks it.

## Defaults

- Build once. Promote the same digest from staging to production. Do not rebuild from a branch and call it the same release.
- Record source revision, build instructions, and builder identity in provenance next to the digest.
- The registry and the cluster verify the signature before schedule. Unverified tags do not run in production.
- Pin direct dependencies. Own a process for transitive updates (automated PRs are fine) with a human or a policy gate for sensitive packages.
- Separate the role that can push code from the role that can push a production deploy, or require a second approver.
- CI identities are workload identities, not long-lived cloud keys. See [secrets](../identity/secrets.md).
- A compromised dependency has an owner: who is paged, how you roll forward to a patched digest, how you prove what ran.

## Checklist

- [ ] Every production image is addressed by digest, not only by a mutable tag.
- [ ] An SBOM for that digest is retained at least as long as the release might still be running or restorable.
- [ ] Deploy fails closed when the signature or the expected issuer is missing.
- [ ] Runners are ephemeral or rebuilt. A poisoned runner is in the threat model.
- [ ] You can list the third-party actions or plugins the pipeline runs, and pin them.

## Anti-patterns

- Signing an artifact on a developer laptop after an untrusted CI build, and treating the signature as provenance.
- Disabling verification the first time it blocks a Friday deploy, with no expiry on the exception.
- Storing the SBOM in a wiki and the image in a registry, with no digest linking them.
- Assuming a language lockfile covers the base image, the OS packages, and the CI plugins. It does not.

## Further reading

- [SLSA](https://slsa.dev/)
