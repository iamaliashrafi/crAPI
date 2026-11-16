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

## API2 baseline A2 — OTP received in local MailHog (2026-11-16)

**Source:** Researcher-supplied screenshot of MailHog at `http://localhost:8025`.

- Local MailHog is connected and displays a test email with subject `crAPI OTP`.
- Recipient: research-owned TesterB test mailbox (full email deliberately omitted).
- The message contains a **four-digit numeric OTP**, confirming delivery after `POST /identity/api/auth/forget-password` returned HTTP `200` (History `202`).
- Do **not** upload the original screenshot: it exposes the active OTP and test email.
- Neither the OTP itself, reset link, account email, nor MailHog message headers are stored here.

**Security interpretation:** A four-digit decimal OTP provides at most 10,000 possibilities. Weakness depends on controls such as strict throttling/lockout, expiration, account/transaction binding and one-time use. None has yet been assessed. No API2 vulnerability has been confirmed.

**Next step:** Return to the research-owned TesterB password recovery form and map the next API endpoint with ZAP. If an OTP form is available, perform only a single wrong-code negative-control attempt and inspect its request/response; do not brute-force or automate attempts. A legitimate correct-code flow may follow.

## API2 negative control A3 — invalid OTP rejected, HTTP 500 returned (2026-11-16)

**Source:** Researcher-provided screenshot showing ZAP History entry **204** for a single invalid OTP submission against the research-controlled TesterB account.

| Property | Observed |
|---|---|
| Method | `POST` |
| Path | `/identity/api/auth/v3/check-otp` |
| Host | `http://localhost:8888` |
| Request format | `application/json` |
| Request keys | `email`, `otp`, `password` (all values intentionally redacted) |
| Response HTTP status | `500 Internal Server Error` |
| Response body (sanitized) | `{"message":"Invalid OTP! Please try again..","status":500}` |

**Result:** The tested incorrect OTP was *rejected* by the application's response. The HTTP 500 status is semantically inappropriate for an expected invalid-code condition, suggesting improper error-status mapping / error handling. It does **not** by itself show that authentication was bypassed, that the server crashed, or that attempt limits are missing. Whether the password remained unchanged is not yet independently verified by a subsequent login check.

**Sensitive data:** the screenshot includes a test password, an OTP attempt and a cookie; the raw image is **not** uploaded to this public repository. Do not paste those secrets or session identifiers into further reports.

**Next step:** Establish an authorized **valid OTP baseline** with TesterB's own current OTP from local MailHog, choosing a new lab-only password. If the previous code has expired, initiate one new password-recovery request and use that newly generated OTP. Capture ZAP Request/Response metadata and report the resulting status without exposing the OTP, password or cookie. Then confirm the new password works for TesterB only. Review limited negative tests and expiry / single-use separately; no automated OTP guessing.

**API2 finding status:** No Broken Authentication flaw confirmed. Invalid OTP rejection observed; potential error-handling quality issue to document separately if reproducible.

## API2 positive control A4 — valid OTP accepted (2026-11-16)

**Evidence:** Researcher-provided OWASP ZAP screenshot (History entry **206**). The browser submits a recovery confirmation for the researcher-owned **TesterB** account.

| Field | Observation |
|---|---|
| HTTP method | `POST` |
| Endpoint | `/identity/api/auth/v3/check-otp` |
| Host | `http://localhost:8888` |
| Request Content-Type | `application/json` |
| Request shape | `{"email":"<REDACTED>","otp":"<REDACTED>","password":"<REDACTED>"}` |
| HTTP response status | `200 OK` |
| Response body | `{"message":"OTP verified","status":200}` |
| Response time in History | 114 ms |

**Comparison with A3:** One deliberately invalid OTP resulted in HTTP `500` and the explicit message `Invalid OTP! Please try again..` (History **204**); the valid OTP produced HTTP `200` with message `OTP verified` (History **206**). These controls establish that the endpoint distinguishes those two code values. The `500` appears to be an unsuitable error mapping for a predictable invalid-code condition, **not evidence of an authentication bypass**.

**Important limitation:** The server message confirms OTP validation; it does **not by itself verify that the password has changed**. Next, log in to TesterB with the newly selected lab-only password to confirm the account's post-reset state. Separately, if needed, check that the prior password no longer authenticates. No login evidence from after the reset has been supplied yet.

**Current security outcome:** API2 assessment **in progress**; no broken-authentication vulnerability confirmed. Attempt throttling, code expiry, replay protection, reset binding to account, and invalidation of earlier sessions still need controlled evaluation.

**Disclosure policy:** The original screenshot includes an actual recovery code, test password, mailbox and session cookie. Do **not** upload that image unredacted to GitHub, Upwork or LinkedIn. No real code, password, cookie or email address is stored in this report.

## API2 positive control A5 — Login with newly reset password succeeds (2026-11-16)

**Evidence:** Researcher-provided ZAP screenshot, History entry **207**, showing the login transaction for the researcher-owned TesterB account *after* OTP verification / password reset.

| Item | Observation |
|---|---|
| Method | `POST` |
| Endpoint | `/identity/api/auth/login` |
| Target | `http://localhost:8888` (authorized local lab) |
| Request type | `application/json`, with `email` and `password` fields (values redacted) |
| Response status | `HTTP/1.1 200 OK` |
| Response fields | `token` JWT (value redacted), `message: "Login successful"`, `mfaRequired: false` |
| Related history | Subsequent authenticated `/identity/api/v2/user/dashboard` requests and auth verification succeeded with HTTP `200`. |

**Interpretation:** The newly chosen lab password works for TesterB and the API issued an authentication token. Together with A4, this supports a successful password-recovery flow. It does **not yet** prove the old password was invalidated or that the OTP cannot be replayed.

**Evidence hygiene:** The original screenshot visibly contains a plaintext test password, active-looking JWT and a session cookie. It is not uploaded here; this log contains no secret values.

**Next controlled check:** Log out of TesterB and try **one** login with its prior lab password. An HTTP `401` (or equivalent controlled denial) would show the old password is rejected. Return to login with the new password afterward. After this check, separately test whether the used recovery OTP can be reused using a new distinct test password (without large-scale guessing), and inspect the result carefully.

**API2 status:** Assessment in progress. No broken-authentication vulnerability confirmed.

## API2 negative control A6 — old password rejected after reset (2026-11-16)

**Evidence:** Researcher-supplied screenshot of a single unsuccessful login using the old lab password after a verified reset of TesterB's password.

| Property | Observed |
|---|---|
| ZAP History ID | `231` |
| HTTP request | `POST /identity/api/auth/login` |
| Host | `http://localhost:8888` |
| Request body | `email` and `password` (values excluded for privacy) |
| HTTP response | `401 Unauthorized` |
| Response message | `Invalid Credentials` |
| Response token field | `null` |

**Interpretation:** The earlier password was rejected in this specific authentication attempt; no new JWT was issued. In conjunction with a successful login using the new password (History `207`), this supports that the account's password was changed and the old password is no longer accepted. This **does not** establish that existing sessions or already-issued JWTs were revoked; that is a separate test.

**Evidence precautions:** The uploaded screenshot displays the earlier test password and `chat_session_id`; do not upload the original image to this public repository. The log stores only sanitized metadata.

**Next controlled check — single-use OTP:** Use the prior successful `check-otp` request (History `206`) in ZAP Requester, retaining the same previously consumed OTP and the same research-owned account, but set a different new lab-only password. Send **once** to test replay protection. A denial is expected. If a success response is observed, check which password actually authenticates before claiming replay or unauthorized password reset. No brute force or automation is necessary.

**Current status:** API2 assessment remains in progress. No demonstrated authentication bypass; old password correctly rejected. OTP replay, expiry, rate limiting, and older JWT/session invalidation not yet assessed.

## API2 negative control A7 — previously accepted OTP rejected on repeat (2026-11-16)

**Evidence:** Researcher-supplied screenshot of OWASP ZAP Requester and History, on the self-hosted crAPI lab (`http://localhost:8888`).

- History **232**: a fresh `POST /identity/api/auth/forget-password` returned `HTTP 200`.
- History **235**: `POST /identity/api/auth/v3/check-otp` returned `HTTP 200` (successful verification in the immediately preceding password-recovery flow); the selected response for 235 is not visible in the screenshot, but the History status is.
- History **236**: Source `Manual`, `POST /identity/api/auth/v3/check-otp`, returned `HTTP 500` roughly **30 seconds after** entry 235; Requester response text: `{"message":"Invalid OTP! Please try again..","status":500}`.
- The Requester body includes an `email`, a four-digit `otp`, and `password`. The actual values are deliberately omitted. The researcher followed instructions to reuse an already accepted OTP. The screenshot **does not independently show the full request body for 235**, so exact code equivalence and whether the two supplied passwords differed are not independently proven.
- This suggests the used OTP was **rejected on the second attempt**, consistent with one-time use. **However**, without verifying the post-test account password and the expiry policy, an expiry-based rejection or another state-dependent failure cannot be fully excluded. Do not treat this as independently proven single-use enforcement.
- As in A3, predictable invalid OTP states return `HTTP 500`; this is an error-response semantics issue, **not** evidence of password-reset bypass, service crash, or absent rate limits.
- **No API2 authentication bypass is confirmed.** Strong negative-control result, pending validation of whether the replay caused any password change.

### Next controlled verification

1. Log in to TesterB with the password chosen in the **first successful** reset transaction (History 235), confirming the account still accepts it.
2. If a **different** password was submitted in the replay (History 236), try that replay password **once**: expected `401` and no JWT; this checks that the 500 response did not silently change the password.
3. If both requests used the same password, the replay experiment cannot confirm password non-modification; repeat with a newly issued OTP and two deliberately distinct lab-only passwords if a stronger finding is required. No guessing or automated attempts are necessary.

### Evidence hygiene

The source screenshot exposes a lab OTP, lab password, account email and `chat_session_id` cookie. Do not upload it unchanged to the public GitHub repository. Only this redacted textual summary has been saved.

## API2 control A8 — login after OTP replay attempt (2026-11-16)

**Source:** Researcher-provided ZAP screenshot of a login to research-owned TesterB following the one-time-code replay experiment.

| Field | Observation |
|---|---|
| ZAP History ID | `237` |
| Method | `POST` |
| Endpoint | `/identity/api/auth/login` |
| Request structure | `email` and `password` (values intentionally not recorded) |
| HTTP response | `200 OK` |
| Response behavior | `Login successful`, a JWT is returned (not recorded) |
| Related events | Subsequent dashboard and token verification traffic returned HTTP `200` |

**Critical interpretation:** The supplied screenshot establishes that the password submitted in login request 237 is valid after the replay attempt. The password appears to match the password visible in replay request **236**. However, the selected successful initial `check-otp` request **235** has **not** been shown with its password value, so we cannot tell whether 235 and 236 used the **same** or **different** passwords. Therefore the login success is **not** evidence that replay caused a password update, and also **not** evidence that replay left the original password unchanged.

If 235 and 236 used the same password, a successful login at 237 is the expected result of the first valid reset. If they differed, a successful login using 236's password despite the replay's HTTP 500 would warrant careful investigation into side effects or improper state changes. The next step is to **locally compare** the password values used in History 235 vs 236 without sharing them; only report whether they were identical. If different, test which one currently authenticates (one controlled attempt per password). If identical, design a fresh paired-password experiment before drawing a firm conclusion.

**API2 assessment status:** In progress. Single replay returned HTTP 500 and `Invalid OTP` (History 236); password-state outcome unresolved. No authentication bypass or OTP replay vulnerability confirmed.

**Disclosure policy:** The source screenshot contains a plaintext lab password and an issued JWT. Never upload it unredacted to this public repository. This entry contains only sanitized metadata.

## API2 replay follow-up A9 — password values differed (researcher report, 2026-11-16)

The researcher explicitly confirmed that the password supplied in successful OTP validation request **235** (**Password P1**) was **different** from that supplied in replay request **236** (**Password P2**). A subsequent screenshot had already shown request **237**: login with P2 returned HTTP `200 OK` and a JWT.

**Important implication:** P2 was valid after the attempted replay despite entry 236 returning HTTP `500` with `Invalid OTP`. This is suspicious but **not yet conclusive proof of a replay-caused password change**, because there was no independent login verifying that request 235 had actually set P1 *before* 236 was sent. P2 also appeared in an earlier successful reset flow, so an unchanged earlier password remains a plausible alternative.

**Immediate control:** Sign out, submit exactly one login using P1 (the password from request 235), and record HTTP status and whether a JWT was issued. Do not share P1/P2 values. Compare this result to the already observed HTTP 200 for P2.

**Stronger follow-up if necessary:** Create a fresh OTP reset with two newly distinct lab passwords. First submit a valid OTP with P1 and **verify login with P1 before any replay**. Then replay that same consumed OTP with P2, and test both credentials (carefully one attempt each) to learn whether the second request altered the password despite a failure response. This sequencing removes the current baseline ambiguity; do not brute-force codes.

**Finding status:** Suspected OTP replay/state-change issue under investigation; **not confirmed**. Keep the distinct HTTP 500 error-handling observation separate.
