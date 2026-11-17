# API7:2023 — Server-Side Request Forgery (SSRF), manual OWASP crAPI lab

**Target:** Self-hosted OWASP crAPI at `http://localhost:8888` (researcher-controlled)  
**Assessment mode:** Manual OWASP ZAP and browser only; no scripts  
**Status:** Planned — no API7 request/response observed in this particular lab yet  
**Date:** 2026-11-17

## Scenario: crAPI Challenge 11

The [official crAPI challenge list](https://owasp.github.io/www-project-crapi/) identifies **Challenge 11** as making crAPI send a server-side HTTP request to `www.google.com` and return the response. OWASP [API7:2023](https://api-security.owasp.org/editions/2023/en/0xa7-server-side-request-forgery/) concerns APIs that fetch attacker-controlled URIs without sufficient destination restrictions.

**Candidate entry point (from public crAPI documentation, not yet observed in this researcher's session):**
`POST /workshop/api/merchant/contact_mechanic`, with JSON field `mechanic_api`. The normal flow submits a service report from the vehicle owner's account to the selected mechanic. Other fields may include `mechanic_code`, `vin`, `problem_details`, `repeat_request_if_failed` and `number_of_repeats`; actual request shape must be captured, not guessed.

## Safe one-shot procedure

1. Use research-owned **TesterB** (or another test account that owns a vehicle), open that vehicle's **Contact Mechanic** flow. Send only **one harmless legitimate report** with a short, disposable message. Inspect the actual ZAP History `POST /workshop/api/merchant/contact_mechanic`; note JSON *field names*, response status and nonsecret response fields.
2. Open that real captured request in **ZAP Requester**. Confirm the request uses only the research-owned account's Bearer JWT and vehicle; do not expose the JWT or VIN in screenshots.
3. In a single follow-up request, change only `mechanic_api` from its ordinary mechanic callback URL to the harmless public endpoint `https://www.google.com`. Keep valid mechanic identifiers and other fields as in the captured baseline. If `repeat_request_if_failed` and `number_of_repeats` exist, ensure retry behavior remains disabled / single-attempt (e.g., false and 1); do not turn on repeated requests.
4. **Send once**, observe HTTP status and whether the response includes the external site's data in a field such as `response_from_mechanic_api`. No internal network probing, metadata IPs, port scans or repeated traffic.
5. Confirm whether the fetched response content could only have been obtained by the application server, and whether the endpoint permitted user control of an otherwise sensitive destination. A server-side fetch of a user-supplied arbitrary public URL coupled with response reflection is strong SSRF evidence in this intentionally vulnerable lab, though deeper internal access is not required to prove the unsafe destination policy.

## What not to claim prematurely

- A 2xx response alone, without evidence of the server fetching the chosen destination, is **not** confirmed SSRF.
- Sending the baseline legitimate mechanic request is normal application behavior and is **not** an exploit.
- Do **not** claim access to cloud metadata, internal services, other users' data, or data exfiltration unless separately authorized, tested, and observed. This lab intentionally stops at benign public URL evidence.

## Evidence handling

Do not commit real bearer JWTs, session cookies, VINs, report identifiers tied to accounts, or unredacted screenshots. Save only sanitized request/response property names, status and non-sensitive response excerpts.

## References

- https://owasp.github.io/www-project-crapi/ (official Challenge 11)
- https://api-security.owasp.org/editions/2023/en/0xa7-server-side-request-forgery/
- https://github.com/OWASP/crAPI/blob/develop/docs/challenges.md
