# API9:2023 — Improper Inventory Management (OWASP crAPI)

**Assessment target:** Self-hosted, authorized local OWASP crAPI at `http://localhost:8888`  
**Status:** Planned — old v2 endpoint's activity not yet verified in this researcher's lab  
**Date:** 2026-11-17  
**Method:** Manual OWASP ZAP only; no Python scripts, brute force, or rate-limit flooding

## Goal: compare password-reset OTP API versions

The application's normal password reset flow was already observed in ZAP at:

`POST /identity/api/auth/v3/check-otp`

The **official OWASP crAPI OpenAPI specification** also documents a prior version:

`POST /identity/api/auth/v2/check-otp`

**Official source:** https://github.com/OWASP/crAPI/blob/develop/openapi-spec/crapi-openapi-spec.json

**OWASP definition:** API9 concerns unretired/poorly tracked API versions, outdated documentation and inconsistent controls. See https://api-security.owasp.org/editions/2023/en/0xa9-improper-inventory-management/

The presence of multiple *documented* versions alone is not an API9 security finding. To establish a meaningful weakness, we must determine whether the older version is still active and provides materially weaker security controls / exposes functionality that should have been retired.

## Single, non-disruptive negative control

1. In ZAP History, select the earlier test-owned account request `POST /identity/api/auth/v3/check-otp` with an **invalid or already-consumed OTP**. Open it in Requester.
2. Change **only the route version** from `/identity/api/auth/v3/check-otp` to `/identity/api/auth/v2/check-otp`.
3. Keep this to a researcher-owned **TesterB** account and an already-consumed or definitely invalid OTP; the new-password field, if present, must be throwaway and no valid OTP entered. Ensure no other user is targeted. Send **once**.
4. Compare the observed HTTP status and response body to the earlier v3 invalid-OTP response. If v2 returns a meaningful OTP validation response (rather than route 404), this supports the old endpoint being **present/active**, not proof that it is unprotected against abuse.
5. Stop. The official crAPI codebase may use different rate-limit enforcement between versions, but a single rejected request **does not validate or refute rate-limit behavior**. Do not brute force 4-digit OTPs, use ZAP Fuzzer, or send repeated concurrent traffic.

## Assessment rubric

| Observation | Supported interpretation |
|---|---|
| v2 returns an application-level invalid OTP message | Older version exists and handles input in this deployed lab; business/security impact unverified |
| v2 returns 404 | No evidence this specific legacy endpoint is deployed on this instance; does not rule out other inventory weaknesses |
| v2 returns 429/503 for throttling | A protection may be present; requires careful interpretation with already-existing account state |
| v2 returns 200 without expected OTP confirmation | Requires immediate independent review of state; do **not** assume password changed solely because of a 200 |
| Network/JSON error | Inconclusive; inspect actual error and stop rather than guessing |

**Important scope:** Password reset endpoints can change account credentials. Use only researcher-owned accounts with an invalid/consumed OTP and do not make repeated attempts. No password reset or account takeover is sought in this API9 inventory check.

## Context

API8 A1 was confirmed as a low-severity verbose Java/Spring validation error disclosure in ZAP History 375; formal report: [API08-MISCONFIG-001](../findings/API08-VERBOSE-VALIDATION-ERRORS.md).

## Evidence handling

Keep JWTs, cookies, test emails, OTP values, test passwords and raw ZAP request screenshots out of the public repository. Record sanitized endpoint, HTTP status, response message category and exact differences observed.
