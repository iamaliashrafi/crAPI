# API07 — User-Controlled Mechanic Callback URL Triggers Server-Side HTTP Request

**Finding ID:** API07-SSRF-001  
**Category:** OWASP API7:2023 — Server-Side Request Forgery (SSRF)  
**Status:** **Confirmed in the authorized local crAPI lab — benign external HTTP fetch and response reflection**  
**Provisional severity:** Medium (qualitative; internal network reachability and real deployment impact not tested; no CVSS assigned)  
**Date:** 2026-11-17  
**Target:** Researcher's self-hosted OWASP crAPI at `http://localhost:8888`  
**Tool:** OWASP ZAP Requester (one manually modified request)  
**Remediation:** Not attempted or retested

## Executive summary

The authenticated Contact Mechanic endpoint accepts a client-controlled `mechanic_api` URL. In a manual test, the researcher supplied `http://google.com` as that URL while retaining ordinary test-vehicle details and disabling request retries. The application returned **HTTP 200** and a JSON property `response_from_mechanic_api` containing an HTML document corresponding to the chosen external website. This is evidence that a client-chosen, non-mechanic public destination can be fetched through the application's server-side workflow.

This result matches **OWASP crAPI Challenge 11**: “Make crAPI send an HTTP call to www.google.com and return the HTTP response.”

The exercise deliberately used a harmless public destination, **not internal addresses, cloud metadata or data-exfiltration infrastructure**.

## Reproduction — sanitized

1. Authenticate as a research-owned normal account with a test vehicle.
2. Capture the ordinary Contact Mechanic request in ZAP:
   `POST /workshop/api/merchant/contact_mechanic`.
3. Open the request in ZAP Requester. Preserve the normal required test-vehicle and mechanic fields, but change only the user-controlled callback destination to `http://google.com`. Disable retries and limit to a single send.
4. Send **once** and inspect response.

Sanitized illustrative request body — values other than the benign URL are placeholders:

```http
POST /workshop/api/merchant/contact_mechanic HTTP/1.1
Host: localhost:8888
Authorization: Bearer <REDACTED_TEST_USER_JWT>
Content-Type: application/json

{
  "mechanic_code": "<TEST_MECHANIC_CODE>",
  "problem_details": "<BENIGN_TEST_TEXT>",
  "vin": "<REDACTED_TEST_VIN>",
  "mechanic_api": "http://google.com",
  "repeat_request_if_failed": false,
  "number_of_repeats": 1
}
```

## Evidence and observations

| Element | Observed |
|---|---|
| ZAP History | **508**, source **Manual** |
| Method/path | `POST /workshop/api/merchant/contact_mechanic` |
| Input sink | `mechanic_api` |
| Supplied external destination | `http://google.com` |
| Retry parameters | `repeat_request_if_failed: false`, `number_of_repeats: 1` |
| HTTP response | **200 OK** |
| Response JSON | Includes `response_from_mechanic_api` with an HTML document beginning with `<!doctype html><html ...` and recognizably related to Google |
| ZAP recorded elapsed time | **750 ms** |
| ZAP recorded response body length | **89,825 bytes** |

**Evidence provenance:** These method/path, input keys, external URL, response JSON field, status, timing and length are visible in a researcher-uploaded ZAP screenshot. Actual externally resolved destination/redirect chain and network packet traces were not independently captured. The expected HTML being returned in `response_from_mechanic_api` is strong lab evidence of the application's external fetch capability, and closely matches the intentionally vulnerable challenge.

## Security impact

A normal API client appears able to influence the destination contacted by the server, rather than being restricted to an approved mechanic service host. In real deployments, improperly restricted server-side URL fetching can create a pivot for sending requests from the server's network position and may enable access to untrusted destinations, depending on the actual network architecture.

**Do not overstate:** This lab did **not** test internal hosts, localhost/loopback destinations, private IP ranges, cloud metadata, ports, credentials, sensitive information or exploitation beyond a benign public web response. Such consequences remain hypothetical and are **not** reported as observed.

## Likely root cause (hypothesis, source code not examined)

The API likely trusts the client-supplied `mechanic_api` as an outbound HTTP target without a strict allowlist of legitimate mechanic callback endpoints.

## Recommended remediation

1. Do **not** let clients select arbitrary outbound destinations. Accept a stable mechanic identifier and map it server-side to an approved endpoint.
2. Apply a strict allowlist of hostnames and HTTPS schemes, with explicit port rules and URL normalization.
3. Resolve and validate DNS/IP destinations, rejecting private, loopback, link-local, reserved and otherwise disallowed address ranges, including after redirects and on every connection to mitigate DNS rebinding.
4. Disable redirects or revalidate every hop; reject embedded credentials and malformed or alternative IP representations.
5. Enforce egress firewall/service-mesh policies and short connection/read timeouts, bounded response size, and no automatic retries to arbitrary destinations.
6. Avoid returning untrusted external responses verbatim to callers; log sanitized destinations and blocked attempts.

## Suggested retest

With a controlled, harmless public domain not on the approved mechanic allowlist, a normal user should receive a clear **4xx rejection** and should not receive remotely fetched content. Approved mechanic lookups should continue functioning.

## Evidence confidentiality

The source screenshot contains a full Bearer JWT, test VIN and callback response data. It is **not** uploaded raw to this public repository. This report contains only safe descriptions and sanitized examples.

## References

- [OWASP API7:2023 — Server-Side Request Forgery](https://api-security.owasp.org/editions/2023/en/0xa7-server-side-request-forgery/)
- [OWASP crAPI official challenges — Challenge 11](https://github.com/OWASP/crAPI/blob/develop/docs/challenges.md)
- [API7 chronological lab journal](../docs/10-api7-ssrf-lab.md)
