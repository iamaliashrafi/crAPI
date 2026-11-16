# API3:2023 — Broken Object Property Level Authorization (BOPLA) lab

**Target:** Researcher-owned, self-hosted OWASP crAPI at `http://localhost:8888`  
**Status:** In progress — scenario selected; no test evidence collected yet  
**Researcher accounts:** Research-owned TesterA and TesterB only

## OWASP concept

API3:2023 covers **Excessive Data Exposure** (readable properties that should be hidden) and **Mass Assignment** (writable properties that should be protected). Access to an object does not imply permission to inspect or modify all its properties.

Reference: https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/

## First scenario — crAPI video internal-property exposure

The official crAPI challenge set includes Challenge 5, **“Find an API endpoint that leaks an internal property of a video.”** This is the initial read-only API3 exploration. Reference: https://owasp.github.io/www-project-crapi/

### Baseline collection

1. Log in to the local lab as TesterB.
2. Navigate the **Community** / video area of the app.
3. In ZAP History, inspect the GET request(s) involving video resources (search for `video` in the URL). Do not assume a specific endpoint path before observing actual traffic.
4. Select a GET request and inspect **Response → Body**. Inventory JSON **property names** and compare with properties actually needed/displayed in the UI.
5. Consider whether any returned internal or sensitive field is unnecessary for the authenticated user. Do **not** classify any field as a vulnerability without confirming sensitivity, intended UI behavior and access requirements.

### Evidence to collect (sanitized)

- HTTP method and observed endpoint path.
- History ID, HTTP response status.
- JSON field names and data types; redact actual IDs, secrets, tokens, emails, location and personal values.
- User-visible screen properties compared with additional API response properties.
- Any established security impact; otherwise classify as *not confirmed*.

**Do not** upload raw ZAP screenshots or authorization headers to a public GitHub repository.

## Prior API2 transition note

The researcher reported having attempted JWT invalidation after a password reset and requested to move on. No pre-/post-reset JWT request/response pair or conclusive status was supplied. Therefore **JWT invalidation has not been verified** in the report; do not infer that the old JWT was revoked or remained active. API2's earlier OTP-attempt-limit observation remains separately documented in `docs/05-api2-broken-authentication-lab.md`.
