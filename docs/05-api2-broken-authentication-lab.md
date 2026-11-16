# API2:2023 — Broken Authentication (crAPI Lab Journal)

**Assessment started:** 2026-11-16  
**Current status:** In progress — discovery and legitimate password-recovery baseline. **No API2 weakness confirmed yet.**  
**Lab target:** `http://localhost:8888` (researcher's self-hosted OWASP crAPI only)  
**Tool:** OWASP ZAP  
**Accounts:** Researcher-owned `TesterA` and `TesterB`

## Reference and intent

The [OWASP API2:2023 Broken Authentication](https://api-security.owasp.org/editions/2023/en/0xa2-broken-authentication/) category includes authentication-flow weaknesses, insecure password recovery, weak brute-force protections, compromised or insufficiently validated tokens, and missing safeguards for sensitive account changes.

The upstream [crAPI challenge list](https://github.com/OWASP/crAPI/blob/develop/docs/challenges.md) includes **Challenge 3: Reset the password of a different user** under Broken User Authentication. This document is not evidence that the local version has the exact same endpoints or vulnerabilities. **Test the behavior of this local deployment, do not assume it.**

## Goal and scope

Test whether the reset-password flow securely verifies that a reset operation is authorized by a suitable one-time code or reset token. Learn to identify relevant API requests and responses, examine code/token lifetime and attempt restrictions, and propose safe remediations.

Never target other people's accounts. This exercise uses only the two accounts explicitly created for the local lab. Do not perform credential stuffing, large OTP brute-force sequences, high-volume automation or disruptive traffic. Protect the test accounts' credentials and reset codes.

## Teaching sequence

1. **Map the normal flow** using `Forgot Password?` on crAPI login.
2. **Capture the recovery initiation request** with ZAP History: method, local URL path, request content type, response status and generic message (no sensitive values).
3. **Check local MailHog** at `http://localhost:8025` for the message sent to the controlled test inbox. Do not publish reset links/codes.
4. **Inspect the verification and completion endpoints** when discovered naturally; collect an authorized control baseline.
5. **Controlled negative checks**: test one incorrect/expired code and compare server response to a legitimate valid-code attempt. Do not guess codes at scale.
6. **Inspect protections**: expiry, single-use, rate limiting under minimal controlled sampling, token binding to the intended account, and invalidation of old sessions after reset. Record what is and is not tested.
7. **Evidence & remediation**: confirmed/negative/not-applicable outcome, sanitized request/response, security impact and recommendations.

## Initial discovery checklist

- [ ] Open `http://localhost:8888/login` while using the ZAP-proxied Firefox.
- [ ] Click `Forgot Password?`.
- [ ] Request recovery for the researcher-owned **TesterB** test email.
- [ ] In ZAP, identify the newly generated HTTP request to the **local crAPI host**; note method, path, status code and response format only.
- [ ] Do not paste or commit the password, OTP, reset token, JWT, cookie or full email address.
- [ ] Before moving to any new scenario, verify the recovery mechanism's actual request shape on this deployment.

## First capture log

**First recovery initiation observed in ZAP History #202.** See A1 below. The verification and completion endpoints are still pending.

| Field | Observed |
|---|---|
| Timestamp | 2026-11-16 (screenshot) |
| ZAP History ID | 202 |
| Request method | POST |
| API endpoint | /identity/api/auth/forget-password |
| Response code | 200 |
| Response behavior | API reports OTP sent to TesterB test email |
| Verification method | Pending |

## Interpretation standards

- HTTP `200` alone does **not** demonstrate broken authentication.
- A successful recovery for the account that initiated a valid recovery is **expected**.
- Failure to deny unauthorized or invalid reset attempts, lack of appropriate attempt restrictions, or the ability to reset a second account without required proof can indicate an API2 flaw, but must be independently reproduced.
- Report rate-limit findings only after justified, controlled checks; absence of a CAPTCHA in a screenshot is not by itself proof that protection is absent.

## Evidence hygiene and portfolio

This repository is **public**. Store only sanitized summaries and permanently redacted screenshots. Do **not** commit recovery emails, one-time codes, reset URLs, JWTs, credentials, session cookies, database records or raw ZAP sessions.

## Sources

- [OWASP API2:2023 Broken Authentication](https://api-security.owasp.org/editions/2023/en/0xa2-broken-authentication/)
- [OWASP crAPI Challenge 3](https://github.com/OWASP/crAPI/blob/develop/docs/challenges.md)
- [ZAP Requester documentation](https://www.zaproxy.org/docs/desktop/addons/requester/)

## API2 baseline A1 — password-recovery initiation captured (2026-11-16)

**Source:** Screenshot from the researcher's own local OWASP ZAP session, selected History ID **202**.

| Field | Verified value |
|---|---|
| Method | `POST` |
| Path | `/identity/api/auth/forget-password` |
| Host | `http://localhost:8888` |
| Request Content-Type | `application/json` |
| Request body shape | `{"email":"<TESTER_B_EMAIL_REDACTED>"}` |
| HTTP response | `200 OK`, `application/json` |
| Sanitized response shape | `{"message":"OTP Sent on the provided email, <REDACTED>","status":200}` |
| ZAP History ID | `202` |

**Interpretation:** The local API accepted the password-recovery initiation for research-controlled account TesterB and returned a message saying an OTP was sent. This does *not* independently verify delivery of an email, OTP validity/expiry, rate limiting, or any authentication flaw. **No API2 vulnerability has been confirmed.**

**Evidence handling:** The source screenshot includes the full test email and a `chat_session_id` cookie. Do not commit the original screenshot or copy session identifiers, reset codes, or reset links into the repository.

**Next practical step:** Open the *local* MailHog interface at `http://localhost:8025` and locate the new password-reset message addressed to research-controlled TesterB. Confirm its existence, without sending the actual OTP or full reset link to public reports. Return to crAPI, observe the legitimate OTP/verification step and corresponding ZAP requests; do not perform guessing or automated attempts.
