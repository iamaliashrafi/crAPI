# API8:2023 — Security Misconfiguration (crAPI)

**Target:** Researcher-owned local crAPI `http://localhost:8888`  
**Mode:** Manual OWASP ZAP, no scripts  
**Status:** In progress — previously captured verbose validation error selected for review; severity pending  
**Date:** 2026-11-17

## Scope and risk model

API8 covers insecure configuration, unnecessary methods/services, security header issues, permissive cross-origin rules, and **overly detailed error messages**. A local intentionally vulnerable training application's HTTP URLs or headers are not automatically production vulnerabilities; the assessment must anchor to actual effects and deployment context.

**OWASP category:** https://api-security.owasp.org/editions/2023/en/0xa8-security-misconfiguration/

## API8 check A1 — verbose server-side validation output already captured

During earlier API3 manual testing, ZAP **History #375** displayed an unsuccessful `POST /identity/api/v2/user/change-phone-number` with placeholder phone fields, HTTP **400 Bad Request** and a JSON response beginning with `Validation failed`. The **details** visibly included Java/Spring internal validation class names and structures such as `org.springframework.validation.BeanPropertyBindingResult`, field objects and size rules.

**What is supported:** Internal framework implementation names and validation internals were exposed in the error response in this local lab. This is a potential **verbose error information disclosure / error-handling hardening** issue. The visible screenshot did **not** demonstrate secrets, stack frames with file paths, database credentials, or another system compromise. Do not claim any of those.

**Single next action (no new request):**

1. In OWASP ZAP **History**, locate manual request **375** (`POST /identity/api/v2/user/change-phone-number`, HTTP 400).
2. Select **Response → Body**, and inspect the visible `details` field.
3. Record only whether it exposes internal Java packages/classes or only user-friendly validation reasons. Redact user account values, phone numbers, JWTs and cookies.
4. If internal framework details persist in the stored history, classify a **limited verbose error disclosure** finding at Informational/Low provisional severity, according to the concrete exposed data. More severe API8 consequences have not been tested.

**Do not run flood tests, malicious payloads or public scans.** This assessment is manual and local.

## Prior category

API7 SSRF was confirmed on `POST /workshop/api/merchant/contact_mechanic` using a single benign public URL (`http://google.com`), which returned HTML in `response_from_mechanic_api`. Formal report: [API07-SSRF-001](../findings/API07-SSRF-ARBITRARY-PUBLIC-URL-FETCH.md). No internal resources accessed.

## Evidence policy

The source ZAP capture contains sensitive request data. Never commit unredacted screenshots or complete authorization headers to public GitHub.

## API8 A1 — internal Java/Spring validation details confirmed (2026-11-17)

**Evidence:** Researcher-provided ZAP Request & Response screenshot re-inspecting existing manual **History #375**, `POST /identity/api/v2/user/change-phone-number` in their authorized local crAPI lab. No new request was sent for this check.

| Attribute | Directly observed |
|---|---|
| HTTP status | **400 Bad Request** |
| JSON `message` | `Validation failed` |
| JSON `details` | Starts with `org.springframework.validation.BeanPropertyBindingResult: 2 errors` |
| Application structure disclosed | `changePhoneForm`, fields `new_number` and `old_number`, Java/Spring binding/validation class names |
| Input constraints | `Size` validation with range 0 to 15 |
| Secrets / filesystem paths | **None evidenced in the error response screenshot** |

**Assessment:** **Confirmed low-severity / informational-style API8 verbose error disclosure**. Invalid user-supplied field values were correctly rejected with HTTP 400, but client-visible `details` unnecessarily exposed framework internals and internal form/validator structures. No server compromise, credential disclosure, stack-trace path leak, or critical misconfiguration demonstrated.

**Standalone sanitized finding:** [API08-MISCONFIG-001 — Verbose Spring Validation Errors](../findings/API08-VERBOSE-VALIDATION-ERRORS.md). Provisional severity **Low**. No remediation or retest performed.

**Next:** Manual API9 audit of API version inventory: contrast the documented `/identity/api/auth/v3/check-otp` route (observed earlier) with the older `/identity/api/auth/v2/check-otp` route in the official crAPI OpenAPI spec; do at most one negative-control request to the older version, with test-owned account and a known-invalid or already-used OTP, without brute forcing.
