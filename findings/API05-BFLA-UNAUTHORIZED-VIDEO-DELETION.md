# API05 — Unauthorized Deletion of Another User's Video through an Admin Endpoint

**Finding ID:** API05-BFLA-001  
**Category:** OWASP API5:2023 — Broken Function Level Authorization (BFLA)  
**Target:** Authorized, local, intentionally vulnerable OWASP crAPI (`http://localhost:8888`)  
**Status:** **Confirmed in local lab — researcher-verified deletion**, based on the observed API response and the researcher's post-test owner-account check  
**Severity:** **High (provisional qualitative assessment, not a finalized CVSS score)**  
**Assessment date:** 2026-11-17  
**Method:** Single manual OWASP ZAP Requester request, without automated fuzzing  
**Remediation:** Not implemented; not retested

## Executive summary

The researcher's ordinary test user **TesterB** sent an authenticated `DELETE` request to an **admin video deletion** endpoint for a disposable video belonging to independent test user **TesterA**. The server returned **HTTP 200** with `User video deleted successfully.` The researcher then switched back to TesterA and confirmed that the video was no longer present. This demonstrates a failure to enforce the expected privileged function access restrictions and/or owner constraints in the local lab.

**Evidence provenance:** The request method/path, Bearer header, and HTTP response are visible in the researcher's ZAP screenshot. Video ownership, ordinary-user identity of the Bearer session, and the post-delete state were explicitly confirmed by the researcher during the guided two-account test; these particular facts were not independently verified by a sanitized screenshot of token claims or a final GET response. Keep that distinction in the portfolio.

## Authorized scope and accounts

- **Application:** Self-hosted OWASP crAPI at `localhost:8888`.
- **Owner account:** `TesterA`, research-owned ordinary account; uploaded a disposable test video for this one scenario.
- **Requester account:** `TesterB`, research-owned ordinary account; no administrator role was intended.
- **Target video:** Lab video ID **52**; this ID is a disposable test resource, not real-world personal content.
- **Permission being checked:** Whether a standard user can invoke an administrative video deletion operation on a different user's resource.

## Reproduction summary

1. Researcher logs in as TesterA, uploads a disposable test video, and reports `video_id=52` from TesterA's dashboard.
2. Researcher signs out, logs in as TesterB, and captures a fresh authenticated request with TesterB's Bearer JWT in OWASP ZAP.
3. In **ZAP Requester**, one request is made with that standard-user token to the administrative deletion endpoint:

   ```http
   DELETE /identity/api/v2/admin/videos/52 HTTP/1.1
   Host: localhost:8888
   Authorization: Bearer <REDACTED_TESTER_B_TOKEN>
   ```

4. The server's observed response is:

   ```http
   HTTP/1.1 200 OK
   Content-Type: application/json

   {"message":"User video deleted successfully.","status":200}
   ```

5. Without repeating the DELETE, the researcher logs back into TesterA and confirms the previously uploaded video **is gone**.

## Observed result vs intended result

| Measure | Observation |
|---|---|
| Requesting principal | TesterB standard user (researcher-confirmed test context) |
| Resource owner | TesterA (researcher-confirmed test context) |
| Privileged operation | `DELETE /identity/api/v2/admin/videos/52` |
| Response status | **HTTP 200 OK** (ZAP screenshot) |
| Response text | **`User video deleted successfully.`** (ZAP screenshot) |
| Actual video state | **Deleted / absent from owner profile** (researcher-reported fresh owner check) |
| Expected secure behavior | **403 Forbidden** or another appropriate denial for non-admin, non-owner principal; target video should remain intact |

## Security impact

This local-lab behavior allows a normal authenticated account to invoke an administrative function that changes another account's resources. For a real service, unauthorized media deletion could lead to data loss, sabotage, and availability/integrity impact. It does not establish that every administrative endpoint is similarly vulnerable.

## Root cause hypothesis (not source-code verified)

The admin video-deletion handler likely has insufficient **function-level role enforcement** and/or missing ownership checks. The endpoint path containing `/admin/` is not an authorization mechanism. Only server-side authorization checks can enforce privilege restrictions.

## Recommended remediation

1. Require a server-side **administrator role** for the admin video-deletion handler, denying ordinary authenticated users.
2. Where user self-service deletion is intended, expose a separate correctly authorized endpoint that verifies video ownership.
3. Centralize function-level authorization with deny-by-default rules and explicit role/permission mapping.
4. Add integration tests: ordinary TesterB denied on admin DELETE of TesterA's video; actual owner/admin behaviors tested separately as applicable.
5. Log unauthorized attempts without leaking access tokens or private user/video data.

## Retest acceptance criteria

An ordinary account with a valid Bearer token must receive a denial when requesting this admin video DELETE for another account's disposable video, and a fresh owner-side check must show the target video is still intact. Privileged functionality should continue to work only for authorized roles.

## Caveats and evidence hygiene

- This is one confirmed **local lab** test, deliberately against an intentionally vulnerable training app; no production deployment or unrelated account was tested.
- Evidence of deletion is a researcher follow-up report; the screenshot independently shows only the successful DELETE response and the request shape.
- The ZAP screenshot displayed a full Bearer JWT and other session data. **Do not publish it raw**. No credentials or unredacted captures are included in this report.
- CVSS is not calculated; High is a **provisional qualitative severity** pending formal scoring and risk context.

## References

- [OWASP API5:2023 — Broken Function Level Authorization](https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/)
- [OWASP crAPI Challenge 7 — Delete a video of another user](https://owasp.github.io/www-project-crapi/)
- [API5 chronological lab journal](../docs/08-api5-broken-function-level-authorization-lab.md)
