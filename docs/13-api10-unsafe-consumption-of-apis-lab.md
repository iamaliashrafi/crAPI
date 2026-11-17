# API10:2023 — Unsafe Consumption of APIs (crAPI)

**Scope:** Authorized self-hosted OWASP crAPI at `http://localhost:8888`  
**Mode:** Manual OWASP ZAP only, no scripts  
**Status:** Planned — independent API10 behavior not yet verified  
**Date:** 2026-11-17

## Security question

OWASP API10 addresses **unsafe trust in responses, redirects, transport and resource costs** of upstream / third-party APIs. A successful outgoing HTTP request is **not by itself** an API10 vulnerability; the issue is what the application does with the resulting untrusted data and whether it safely validates destinations, redirects, content, errors and size.

Official reference: https://api-security.owasp.org/editions/2023/en/0xaa-unsafe-consumption-of-apis/

## Existing evidence (API7, not separately sufficient for API10)

A previous manual Contact Mechanic request (`POST /workshop/api/merchant/contact_mechanic`, ZAP History #508) supplied `mechanic_api=http://google.com`. The server returned HTTP 200 and a JSON field `response_from_mechanic_api` containing external website HTML (about 89,825 response-body bytes). This demonstrates **SSRF** through a client-controlled URL but does **not** on its own prove unsafe parsing, injection execution, unsafe redirects, or vulnerable processing of an upstream response. Do not double-count a confirmed API7 issue as an independently confirmed API10 vulnerability without new evidence.

## Single safe manual redirect-handling check (planned)

**Hypothesis:** Does the Contact Mechanic HTTP client follow a public upstream `302` redirect and return the **final destination's** response, instead of handling / validating the redirect explicitly? This tests a concrete API10-style trust-boundary behavior without internal network probes.

**Preparation:** Use a test-owned account and vehicle, with an existing valid captured `POST /workshop/api/merchant/contact_mechanic` opened in ZAP Requester. Do not use any real personal information.

**One change only:** Replace the `mechanic_api` URL with:

```text
https://httpbin.org/redirect-to?url=https%3A%2F%2Fexample.com%2F
```

Keep all other legitimate request fields unchanged. Ensure `repeat_request_if_failed=false`, `number_of_repeats=1`. Send **one** manual request.

This is a benign redirect from the public HTTP testing service `httpbin.org` to the public reserved example website `https://example.com/`. No internal IPs, cloud metadata destinations, custom servers, uncontrolled URLs or repeat storms.

**Read response:** Inspect `response_from_mechanic_api`.
- If content of example.com is returned, it supports a public cross-domain redirect being **followed**, but not necessarily a separate exploitable API10 issue given that the same field already allows arbitrary destinations.
- If a 302 error / metadata / rejection is returned, record exactly what the service does.
- If HTTP 4xx/5xx/network error, record as inconclusive; **do not retry repeatedly**.

A standalone API10 vulnerability requires demonstrable unsafe treatment of untrusted upstream data, insecure transport, leaking information through redirects, or a policy bypass with security impact. Following a harmless public redirect is a behavior observation, **not proof of compromise**.

## Stopping rule and reporting

After this one bounded request, close API10 with either **confirmed only if independent security impact is actually evidenced**, or **limited review / no confirmed independent vulnerability**. This provides honest coverage of all ten categories without fabricating results.

## Evidence hygiene

Never publish JWTs, cookies, VINs, OTPs, full Contact Mechanic reports, or raw ZAP screenshots. Record the URL, non-sensitive response shape, status and whether the final public destination was reached.

## References

- https://api-security.owasp.org/editions/2023/en/0xaa-unsafe-consumption-of-apis/
- https://httpbin.org/legacy (redirect-to endpoint)
- https://github.com/postmanlabs/httpbin/blob/master/httpbin/core.py
- [Prior API7 SSRF finding](../findings/API07-SSRF-ARBITRARY-PUBLIC-URL-FETCH.md)

## API10 A1 — public redirect test returned connection error (2026-11-17)

**Evidence:** Researcher-provided screenshot of **OWASP ZAP Requester** and History **#514** from the authorized local crAPI instance, after one test with the previously captured `POST /workshop/api/merchant/contact_mechanic` request. No scripting, flooding or internal IP destinations were used.

| Field | Observed value |
|---|---|
| Method/path | `POST /workshop/api/merchant/contact_mechanic` |
| `mechanic_api` | `https://httpbin.org/redirect-to?url=https%3A%2F%2Fexample.com%2F` |
| Retry behavior | `repeat_request_if_failed=false`, `number_of_repeats=1` |
| HTTP status | **400 Bad Request** |
| JSON error | `{"message":"Could not connect to mechanic api."}` |
| ZAP elapsed time | **5,706 ms** |
| ZAP response body size | **48 bytes** |
| Followed redirect / fetched `example.com`? | **Not demonstrated** |

**Interpretation:** The application did not complete the requested external redirect workflow. The screenshot does **not** establish whether the cause was outbound connectivity, TLS, a remote service condition, timeout, redirect policy or application-level processing. It **does not** prove that redirects are correctly blocked or that upstream input is safely consumed. The separately confirmed API7 SSRF test reflected Google's HTML from a user-controlled `mechanic_api`, but that same proof is **not double-counted** as an independent API10 vulnerability.

**Conclusion / stopping rule:** **Limited API10 check complete — inconclusive; no independently confirmed API10 vulnerability.** This is a coverage exercise, not a full security assurance or clean bill of health. Further upstream response trust checks can be included in a later explicitly scoped assessment. No additional requests are needed for the present ten-category educational lab.

**Evidence hygiene:** Raw ZAP screenshot contains test JWT and VIN. Only sanitized metadata and response text recorded publicly.
