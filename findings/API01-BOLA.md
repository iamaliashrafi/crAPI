# API1:2023 — Broken Object Level Authorization in Vehicle Location API

**Finding ID:** API01-BOLA-001  
**Status:** **Confirmed in the local lab — researcher-verified repeat**  
**Assessment date:** 2026-11-16  
**Target:** Self-hosted OWASP crAPI (`http://localhost:8888`)  
**OWASP classification:** [API1:2023 — Broken Object Level Authorization](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/)  
**Risk level:** **High (preliminary qualitative assessment; not a finalized CVSS score)**  
**Tool:** OWASP ZAP (History and Requester)  
**Remediation status:** Not implemented or retested.

## Executive summary

A read-only authenticated cross-account request to the vehicle-location API returned a different research user's vehicle coordinates and associated identity information. The researcher used a valid token from User A (`TesterA`) while keeping the vehicle identifier belonging to User B (`TesterB`). The researcher subsequently confirmed that the request contained User A's token, had no User B authentication cookie, and reproduced the disclosure.

**Evidence provenance:** The initial cross-account HTTP `200 OK` and User B JSON body are visible in a screenshot of ZAP Requester. The final verification of token equality, absence of User B cookies, and successful second request are **researcher-reported**, not supported by a separately uploaded screenshot. Both kinds of evidence are disclosed transparently. This is a controlled, intentionally vulnerable lab and **not** a client engagement.

## Scope and preconditions

- Two independent accounts owned by the researcher: `TesterA` and `TesterB`.
- User B owns the target lab vehicle.
- Local authorization target: `localhost:8888` only.
- No production service, third-party host, or real user account was tested.
- The test used a read-only `GET`, without data modification.

## Affected endpoint

```http
GET /identity/api/v2/vehicle/<USER_B_VEHICLE_UUID>/location HTTP/1.1
Host: localhost:8888
Authorization: Bearer <USER_A_JWT_REDACTED>
Accept: */*
```

Only the *authentication context* was changed from B to A; the resource path continued to identify B's vehicle. A copied `chat_session` Cookie header was removed before the verification, as reported by the researcher.

## Evidence and reproduction

| Step | Actor and operation | Observation | Provenance |
|---|---|---|---|
| 1. Authorized baseline | `TesterB` GETs its own vehicle location | HTTP `200 OK`; JSON identifies `TesterB` | ZAP History `188` screenshot |
| 2. Identity preparation | `TesterA` logs in and accesses own dashboard | Login, verify, dashboard show HTTP `200` | ZAP History `193`, `195`, `196` screenshot |
| 3. Cross-account read | Tester's Requester GETs B's vehicle location | HTTP `200 OK`, 177-byte JSON identifying `TesterB`, including private coordinates | ZAP Manual History `199` screenshot |
| 4. Isolation check | Compare User A's bearer token to the cross-account Requester token; ensure no User B cookie remains | Authentication context confirmed as `TesterA` | **Researcher-reported** |
| 5. Independent repeat | Repeat the same read-only GET against B's vehicle under User A credentials | HTTP `200 OK` and B's data returned again | **Researcher-reported; additional redacted screenshot not yet supplied** |

### Sanitized response shape

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

The values above are placeholders, **not** raw evidence. Do not publish raw JWTs, vehicle identifiers, coordinates, VINs, PINs, passwords, cookies, or unredacted request/response screenshots.

## Expected vs actual behavior

**Expected:** The backend denies a request by `TesterA` for nonpublic `TesterB` vehicle location data unless an explicit access grant exists. A suitable `403 Forbidden` or masked `404 Not Found` response may be used.

**Actual (researcher-verified):** The backend accepted User A's authenticated request to B's vehicle and returned User B's location and identity fields.

## Security impact

**Confidentiality loss:** An authenticated account may retrieve another account's private vehicle location and identifying information when it knows or obtains the relevant vehicle identifier. Such exposure can facilitate unauthorized monitoring or user profiling. This test demonstrates **read** access only; it does not demonstrate vehicle modification or privilege escalation.

**Preliminary risk:** High due to cross-account private location and identity disclosure. A final CVSS vector requires full evaluation of deployment exposure, attacker prerequisites, impact, and scope. Do not extrapolate lab exploitation to production systems.

## Likely root cause and recommended remediation

The observed behavior is consistent with a missing or ineffective **object-level authorization check**, although source code has **not** been reviewed; exact root cause is not proven.

1. Derive the requesting user from validated authentication server-side.
2. Resolve the vehicle by ID and verify the user owns the vehicle or has a valid delegated permission **before** returning location or identity data.
3. Deny access consistently without revealing private fields, even when the UUID is valid.
4. Apply equivalent checks to every vehicle-related object endpoint; do not rely on unguessable identifiers.
5. Add automated negative authorization regression tests using two independent test accounts, including `A → vehicle B` and `B → vehicle A`.
6. Retest after a code change and record the response and status.

## Final verification still useful for the portfolio

A **sanitized screenshot of the repeated Requester test** with the Authorization value covered, URL UUID redacted and precise location/email hidden would strengthen independent auditability. This is an evidence-publication task, **not** a prerequisite to record the researcher's confirmed lab finding.

## Ethical / publication statement

This is a security training exercise against an intentionally vulnerable local OWASP crAPI deployment, not a real customer or production target. No live credentials or unsanitized screenshots are committed.

## Related material

- [Step-by-step lab journal](../docs/04-api1-bola-lab.md)
- [Top 10 assessment tracker](../docs/03-assessment-tracker.md)
- [Scope and methodology](../docs/01-scope-and-methodology.md)
