# OWASP API Security Top 10 (2023) — Final Educational Lab Assessment Summary

**Project:** OWASP crAPI (intentionally vulnerable training application)  
**Environment:** Self-hosted, researcher-authorized `http://localhost:8888`  
**Tooling:** OWASP ZAP, browser, manual Requester tests; an earlier read-only Python baseline was used during API3 before the researcher chose **manual-only testing** for remaining checks.  
**Assessment period:** 2026-11-16 to 2026-11-17  
**Coverage:** All **ten categories** received a documented lab investigation; depth varies substantially. **This is not a full penetration test or a certification of security.**  
**Evidence:** Researcher-supplied sanitized observations; direct ZAP screenshots for key HTTP requests/responses; some ownership or post-action state checks explicitly researcher-reported.

## Executive summary

The limited manual crAPI assessment yielded **five documented local findings** in API1, API3, API5, API7 and API8. The remaining five categories contain bounded, inconclusive or control-observed tests, **not** proof of security. All findings concern an intentionally vulnerable local training application, not a real-world production target.

| Category | Result | Key evidence | Finding / journal |
|---|---|---|---|
| **API1** Broken Object Level Authorization | **Confirmed in local lab** — provisional High | TesterA token used for TesterB vehicle location; HTTP 200 with another user's location/contact data; researcher verified repeat | [API01 BOLA](../findings/API01-BOLA.md) |
| **API2** Broken Authentication | Limited checks; **no confirmed bypass** | Invalid OTP denied; 12 controlled OTP candidates led to attempt-limit message; JWT invalidation outcome **not independently verified** | [API2 journal](05-api2-broken-authentication-lab.md) |
| **API3** Broken Object Property Level Authorization | **Confirmed exposure** — provisional Medium; Mass Assignment **inconclusive** | Forum API returned other authors' `email` and `vehicleid` not shown in UI; phone-change property probes did not demonstrate unauthorized mutation | [API03 Exposure](../findings/API03-EXCESSIVE-DATA-EXPOSURE.md) |
| **API4** Unrestricted Resource Consumption | Control observed; **no bypass demonstrated** | ~11 MB video upload (researcher-reported size) rejected HTTP 413 `Maximum upload size exceeded` against 10 MB UI limit; read-only pagination checks | [API4 journal](07-api4-unrestricted-resource-consumption-lab.md) |
| **API5** Broken Function Level Authorization | **Confirmed in local lab** — provisional High | Reportedly normal TesterB token invoked `DELETE /identity/api/v2/admin/videos/52`; HTTP 200 `User video deleted successfully.`; owner TesterA later confirmed video absent | [API05 BFLA](../findings/API05-BFLA-UNAUTHORIZED-VIDEO-DELETION.md) |
| **API6** Unrestricted Access to Sensitive Business Flows | Limited check; **no confirmed business-flow abuse** | Two matching Forum posts accepted and later visible; no high-volume traffic or proven business impact | [API6 journal](09-api6-sensitive-business-flows-lab.md) |
| **API7** Server-Side Request Forgery | **Confirmed benign external SSRF in local lab** — provisional Medium | `mechanic_api=http://google.com` resulted in HTTP 200 with Google-related HTML returned inside `response_from_mechanic_api`; no internal access tested | [API07 SSRF](../findings/API07-SSRF-ARBITRARY-PUBLIC-URL-FETCH.md) |
| **API8** Security Misconfiguration | **Confirmed verbose error disclosure** — provisional Low | HTTP 400 validation error exposed Spring `BeanPropertyBindingResult`, internal `changePhoneForm` and constraints | [API08 verbose errors](../findings/API08-VERBOSE-VALIDATION-ERRORS.md) |
| **API9** Improper Inventory Management | Legacy route present; **security impact unverified** | `POST /identity/api/auth/v2/check-otp` answered invalid OTP with HTTP 500 rather than 404; this does not establish weaker security than v3 | [API9 journal](12-api9-improper-inventory-management-lab.md) |
| **API10** Unsafe Consumption of APIs | **Inconclusive** — no independent finding | A single benign `httpbin.org` public redirect test returned HTTP 400 `Could not connect to mechanic api.` after ~5.7 seconds; redirect policy not established | [API10 journal](13-api10-unsafe-consumption-of-apis-lab.md) |

## Findings count and limits

- **5 documented local findings:** API01 BOLA, API03 excessive author-property exposure, API05 admin video deletion BFLA, API07 benign external SSRF, API08 verbose framework error disclosure.
- **Provisional qualitative risk levels:** High (API1, API5), Medium (API3, API7), Low (API8). **No official CVSS scores** or real-world business impact assessment were completed.
- **5 categories without a confirmed independent finding:** API2, API4, API6, API9, API10. These statuses mean *not demonstrated within the limited test*, **not “secure.”**
- Some observations such as TesterA/TesterB ownership and post-delete state were checked by the researcher but are not always independently visible in an attached response screenshot. Findings distinguish researcher confirmation from screenshot-observed HTTP responses.

## Most important remediation themes

1. **Per-object access control:** enforce authorization for vehicle-location data reads (API1).
2. **Response DTO allowlisting:** expose only necessary public author properties in Forum responses (API3).
3. **Function-level authorization:** restrict `/admin/videos/{id}` to true privileged roles, and separately verify resource ownership for any user video-delete path (API5).
4. **Outbound URL control:** map mechanic identifiers to server-side allowlisted callback destinations; validate DNS, IPs, redirects, schemes and response size (API7).
5. **Sanitized error handling:** return safe, minimal validation errors without Java framework internals (API8).

All proposed remediations remain **recommendations only**; no fixes were implemented or retested.

## Methodology and disclosure

The researcher used two **self-controlled test accounts**, TesterA and TesterB, and intentionally disposable lab resources. Tests were manual and deliberately constrained: no live third-party production targets, cloud metadata enumeration, private network scanning, brute-force credential attacks, sustained denial of service, or mass spam tests.

**Do not publish** the original ZAP screenshots without redacting bearer JWTs, cookies, emails, phone numbers, VINs, GPS locations, OTPs or credentials. The GitHub repository includes sanitized text findings, not raw secrets.

## Completion note

The **ten-category educational walkthrough is complete** as of 2026-11-17. A future professional portfolio refinement can add sanitized evidence captures, finalized CVSS scoring, source-code-independent retest proof, and remediation verification. No future tests are implied by completion of the educational coverage.

## Primary references

- https://api-security.owasp.org/editions/2023/en/0x11-t10/
- https://github.com/OWASP/crAPI
- https://www.zaproxy.org/
