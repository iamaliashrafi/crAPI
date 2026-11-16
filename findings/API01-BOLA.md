# API1:2023 — Potential Broken Object Level Authorization in Vehicle Location API

**Finding ID:** API01-BOLA-001  
**Status:** Strong candidate — independent confirmation pending  
**Date tested:** 2026-11-16  
**Target:** OWASP crAPI running on a local, intentionally vulnerable lab at `http://localhost:8888`  
**OWASP category:** [API1:2023 Broken Object Level Authorization](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/)  
**Severity:** Not yet rated; dependent on confirmed authentication context and impact  
**Tool:** OWASP ZAP Requester

## Executive summary

A researcher-controlled API test against the lab vehicle location endpoint returned an HTTP `200 OK` response containing User B's private vehicle location and associated name and email. The researcher was attempting to send the request using User A's bearer token to User B's vehicle object. If the identity/context is confirmed as User A, this is an object-level authorization failure. At present we have one manually executed request and its response, but the screenshot alone does not cryptographically prove JWT ownership or absence of any User B cookies. Treat this as a **candidate**, not a validated production pentest finding.

## Prerequisites and intended access control

Two local research accounts (`TesterA`, `TesterB`) were registered and authenticated. `TesterB` has an assigned lab vehicle. A legitimate request from TesterB to that vehicle location returned data for TesterB (authorized baseline).

Expected secure behavior: a token from TesterA must not permit accessing nonpublic TesterB location and identity information, absent an explicit access-sharing arrangement.

## Evidence summary (sanitized)

**Authorized baseline:** ZAP History `188`, GET to User B's vehicle location, `200 OK`, response identifying `TesterB`.

**Cross-account attempt:** ZAP Requester Manual History `199`, GET to the same User B vehicle location, `200 OK`, response size `177` bytes, request time `30 ms`, data still identifying `TesterB`. Prior History `193`, `195` and `196` show login, token verification, and dashboard requests consistent with User A session.

Example target/request shape (not raw captured credentials):

```http
GET /identity/api/v2/vehicle/<USER_B_VEHICLE_UUID>/location HTTP/1.1
Host: localhost:8888
Authorization: Bearer <USER_A_JWT_REDACTED>
Accept: */*
```

Observed response shape (sensitive values omitted):

```json
{
  "carId": "<USER_B_VEHICLE_UUID>",
  "vehicleLocation": {
    "id": "<LOCATION_RECORD_ID>",
    "latitude": "<REDACTED>",
    "longitude": "<REDACTED>"
  },
  "fullName": "TesterB",
  "email": "<REDACTED>"
}
```

The shown request is an **illustrative intended test shape**. Its exact authentication context for entry `199` must still be independently rechecked before confirmation.

## Next validation steps

1. Confirm the URL still contains User B's own vehicle ID.
2. Confirm the Authorization header contains only TesterA's bearer token and no Cookie or other authentication material copied from TesterB's session.
3. Independently establish that the same token identifies TesterA, e.g. through User A's own authorized dashboard endpoint.
4. Repeat one non-destructive GET of User B's location using TesterA's token.
5. Compare status, body and account identity to User B's authorized baseline.
6. If cross-account disclosure is reproducible, mark **Confirmed**, assess security impact and severity, and provide a sanitized evidence screenshot.

## Impact if confirmed

An authenticated user could read another account's vehicle coordinates and associated identity details by addressing another vehicle object. This could expose private location information and user details. This is a lab-specific observation until verified and must not be portrayed as a production-customer incident.

## Proposed remediation (to verify against actual implementation)

Authorize access to every vehicle object server-side, using authenticated user identity and the object's permitted owner/association. For each location request, verify ownership or an explicit delegated permission *before* returning location or personally identifying fields. Respond with a consistent denial (e.g., `403` or `404`) when authorization fails. Add automated negative tests for cross-account access and avoid relying on identifier unguessability as an access control.

## Scope and evidence handling

Only the self-hosted OWASP crAPI lab is in scope. Do not publish JWTs, passwords, cookies, unredacted screenshots, real email addresses, vehicle VIN/PIN, vehicle UUID or precise location values. The screenshot used to make these observations is **not uploaded** to this repository.

## Cross-references

- [Lab notes and test sequence](../docs/04-api1-bola-lab.md)
- [Assessment methodology](../docs/01-scope-and-methodology.md)
