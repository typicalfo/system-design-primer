---
title: "Passkeys and MFA"
summary: "Prefer phishing-resistant authenticators, treat recovery as part of the factor, and require the IdP to carry the assurance level you claim."
tags: [identity, passkeys, mfa, webauthn, authentication]
when_to_use: "Use when you are choosing a second factor, rolling out passkeys, or deciding where MFA runs for workforce and customer SSO."
related:
  - oidc-oauth2.md
  - saml-sso.md
  - secrets.md
  - authorization-models.md
  - ../security/zero-trust.md
  - ../compliance/audit-logs.md
last_reviewed: 2026-09-25
---

# Passkeys and MFA

A passkey is a discoverable public-key credential. The browser or platform authenticator speaks [W3C WebAuthn](https://www.w3.org/TR/webauthn-3/) (Level 3 is a W3C Recommendation dated 25 August 2026; [Level 2](https://www.w3.org/TR/webauthn-2/) remains a Recommendation). The authenticator side of the same family is FIDO2. The private key signs a challenge bound to the site's origin, so a look-alike page does not get a reusable secret.

This page uses authenticator assurance levels (AALs) from [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html) (final, July 2025), which superseded SP 800-63B. The suite is [SP 800-63 Revision 4](https://pages.nist.gov/800-63-4/). It is guidance for authentication strength, not a certification you can buy.

## Decide

| Choose | Use when | Avoid when |
|---|---|---|
| Synced passkey | People need to sign in on a new device without a hardware token, and AAL2 is enough | The account must meet AAL3. SP 800-63B-4 says syncable authenticators shall not be used at AAL3, because the key can be exported |
| Device-bound passkey or security key | Privileged access, AAL3, or a policy that the key must not leave the authenticator | You will block most users by refusing platform passkeys and you have no enrollment path |
| Phishing-resistant MFA at the IdP | Workforce or customer SSO. The application trusts the assertion | The customer IdP can only do SMS or push, and you still describe the session as phishing-resistant |
| OTP, SMS, or push as the only factor | A legacy population you have dated a removal for | New privileged access, or any flow you claim is phishing-resistant. SP 800-63B-4 says passwords and out-of-band methods are not phishing-resistant |
| Step-up | Export, billing, SSO changes, role grants, or a session that was opened at a lower AAL | Every API call. Step-up is for the action that needs a higher AAL |

## Defaults

- Offer a phishing-resistant option. At AAL2, SP 800-63B-4 requires verifiers to offer one, and requires federal agencies to require phishing-resistant authentication for staff, contractors, and partners accessing federal systems. AAL3 requires a phishing-resistant authenticator with a non-exportable private key, plus a second factor (a password or a local biometric or PIN that activates the key).
- Synced passkeys can be an AAL2 method only if the sync fabric meets the extra rules in SP 800-63B-4 Appendix B (approved cryptography, keys encrypted in the fabric, private-key operations on the local device, and AAL2-equivalent access to the fabric). They still fail AAL3.
- Attestation is how a relying party learns the authenticator model. Enterprise attestation lets you allow a known security-key fleet and refuse unknown or synced credentials. Consumer synced passkeys often have no useful attestation. Requiring attestation raises assurance and cuts adoption. Pick per population: device-bound with attestation for admins, synced passkeys without attestation for general workforce if AAL2 is the target.
- SMS and voice OTP are out-of-band secrets. They are SIM-swapable and not phishing-resistant. SP 800-63B-4 still allows the public telephone network as an out-of-band channel with extra verifier rules. Do not call that channel the phishing-resistant option.
- Push approval that asks the user to tap Allow, without moving a secret between the login screen and the phone, is the authentication-fatigue pattern SP 800-63B-4 rejects. The same section says that showing a short list of secrets and asking the user to pick one is not enough, because the list is guessable. A code the user transfers between the two channels meets the requirement. Number-matching that is only "pick 1 of 3" does not.
- Recovery is part of the authenticator. A helpdesk reset, an email link, or an SMS code that replaces a passkey drops the account to the strength of that reset. Bind a new authenticator inside a session that already met the target AAL. One-time recovery codes are look-up secrets: store them hashed, use each once, and do not treat them as phishing-resistant.
- Step-up raises the AAL of an existing session. SP 800-63B-4 describes that pattern. Keep the step-up result for the action, not for the rest of the day, when the action is privileged.
- For SSO, MFA belongs at the IdP. The application checks the authentication context (`acr` in OIDC, `AuthnContext` in SAML) and rejects a session that does not meet the policy. See [OIDC and OAuth 2.0](oidc-oauth2.md) and [SSO and SAML](saml-sso.md). A second weak factor in the app does not repair a weak IdP.
- Passwords remain a factor. SP 800-63B-4 requires single-factor passwords to be at least 15 characters, and at least 8 when the password is only one factor of a multi-factor flow. That change does not make a password phishing-resistant.

## Rollout

1. Admins and production access first, on device-bound keys, with attestation if you can name the models you allow.
2. Everyone else's workforce login next, on synced passkeys where AAL2 is the target, with a counted recovery path.
3. Turn off SMS and approve/deny push for any population that has a passkey, after the registration rate and the helpdesk-reset rate are both visible.
4. Customer SSO: write the required context into the enterprise contract. If the customer's IdP cannot meet it, the tenant is on a documented exception with an owner and an expiry, not on a silent fallback.
5. Session revocation on authenticator removal is part of the same change. A removed admin's refresh token must die. See [secrets](secrets.md).

## Checklist

- [ ] Privileged roles cannot enroll or reset with a factor weaker than the role's AAL.
- [ ] The IdP assertion carries an authentication context the app actually checks.
- [ ] Recovery codes and helpdesk resets are audited. See [audit logs](../compliance/audit-logs.md).
- [ ] A lost device has a path that does not leave a synced key enrolled forever.
- [ ] Push, if you still have it, transfers a secret. It does not offer a short multiple-choice list.
- [ ] You can say which populations are AAL2 with synced passkeys and which are AAL3 with non-exportable keys.

## Anti-patterns

- "We added MFA" when the only factor is SMS or an Allow button.
- Attestation required for every consumer signup, then a support bypass that skips it.
- Recovery email that is itself protected only by a password.
- App-level OTP on top of an IdP that already did WebAuthn, plus no step-up on the dangerous actions.
- Treating a synced passkey as AAL3 because the user also has a laptop PIN. Exportability is the AAL3 failure, not the absence of a PIN.

## Related

- [Authorization models](authorization-models.md) for what the session may do after it exists.
- [Zero trust](../security/zero-trust.md) for why network location is not a factor.

## Further reading

- [W3C WebAuthn Level 3](https://www.w3.org/TR/webauthn-3/) (Recommendation, 25 August 2026)
- [W3C WebAuthn Level 2](https://www.w3.org/TR/webauthn-2/)
- [NIST SP 800-63-4](https://pages.nist.gov/800-63-4/) and [SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html)
- [CSRC publication page for SP 800-63B-4](https://csrc.nist.gov/pubs/sp/800/63/b/4/final)
