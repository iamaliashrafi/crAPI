# API5:2023 — Broken Function Level Authorization (crAPI)

**Authorized target:** Researcher-owned local OWASP crAPI instance at `http://localhost:8888`  
**Method:** Manual ZAP only — researcher explicitly opted out of scripting  
**Status:** Planned; no API5 evidence collected yet

## OWASP category

**API5 Broken Function Level Authorization (BFLA)** occurs if a principal can invoke a function that should be restricted to another role, permission, or ownership context. The distinction from **API1 BOLA** is that here the question is access to a **privileged operation**, not simply the reading of a target object.

OWASP category: https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/

## Selected crAPI Challenge 7

The official crAPI challenge documentation explicitly lists **“Delete a video of another user”** under **BFLA**: https://github.com/OWASP/crAPI/blob/develop/docs/challengeSolutions.md

**Proposed controlled scenario:** Researcher owns **both TesterA and TesterB**. The target is an intentionally disposable test video that belongs to one of those accounts. The comparison is between the owner's permission to delete their own video and a different ordinary test user's authorization to invoke the same delete function.

**Safety:** Deletion is a destructive write. Do not delete either account's personal/valuable files. If the user chooses to proceed, test only on a new disposable video intentionally created for this exercise. Never touch third-party accounts or resources. Avoid assuming a particular DELETE endpoint path until it is observed from the local application's behavior.

## Stage 1 — identify the ordinary delete workflow (not yet performed)

1. In the local crAPI UI, sign in as **TesterB** and visit `/my-profile`.
2. Observe whether **My Personal Video** already has a disposable test video and a visible delete/remove control.
3. If there is no video, create a tiny disposable, nonpersonal test video only if needed for this challenge. Avoid larger upload resource tests.
4. **Before clicking Delete**, capture the UI and inspect ZAP History for safe existing video metadata/listing traffic. Determine the actual API path and identifier based on observed requests, not guesses.
5. If a disposable resource and deletion control are established, plan a single intentional cross-account permission check with the researcher's other test account, making the risk of deletion explicit and confirming the expected 403/404 denial. Verify actual resource state after the test.

**Current evidence:** Only previous upload history entries and the profile UI have been seen during API4; these do **not** yet establish whether either test account currently owns a video, or whether a DELETE function is accessible.

## Reporting rubric

- **403/404 to unauthorized TesterA plus video intact:** indicates this one cross-account delete attempt was denied, no BFLA demonstrated.
- **2xx and independently confirmed video deletion by TesterA:** potential BFLA, must confirm that the action was actually unauthorized for the session and that the video was TesterB-owned.
- **2xx without deletion / unrelated errors:** inconclusive until object state verified.
- **No suitable test video or delete operation:** not tested, do not invent a result.

## Evidence policy

Keep JWTs, cookies, emails, video content, IDs and raw unredacted ZAP screenshots out of public GitHub. Document only sanitized API request/response shapes, status codes and observed state transitions.

## Prior API4 case

The 10 MB video upload limit was challenged once with a researcher-reported ~11 MB MP4. The video endpoint `POST /identity/api/v2/user/videos` returned **HTTP 413** with `title: Payload Too Large` and `detail: Maximum upload size exceeded`. This showed an active upstream or application upload-size control, not an API4 bypass. Disruptive Contact Mechanic layer-7 DoS testing was not conducted.

## API5 scenario revision — TesterA owns uploaded video; TesterB tests restricted deletion (2026-11-17)

**Researcher-reported setup:** A disposable test video has now been uploaded by **TesterA (User 1)**. The researcher wants to test whether the other ordinary account, **TesterB**, can delete TesterA's video. The video ID and actual upload response have **not yet been provided**, nor has a DELETE request been executed.

**Authorization design:** Record a fresh authenticated TesterA `GET /identity/api/v2/user/dashboard` and obtain the `video_id` locally (avoid sharing secrets or actual IDs publicly). Then authenticate as TesterB, make sure a B-issued Bearer JWT is in use, and perform at most one deliberate authorization check on the known admin delete operation `DELETE /identity/api/v2/admin/videos/{video_id}` **against only this researcher-owned disposable A video**. The official crAPI OpenAPI specification advertises this as an admin video deletion endpoint; whether it lacks authorization in the researcher's deployed version is **untested**. Verify the result from a fresh TesterA dashboard; 2xx response alone does not prove deletion.

**Consent/safety:** This test intentionally may permanently delete the disposable video. Do not operate on any third-party user content, or upload raw JWTs, cookies, videos, or personal identifiers to a public repository. No scripting; manual ZAP-only.

**Evidence status:** Setup confirmed by researcher's statement; **no API5 finding yet**. Do not classify based on third-party writeups.

**Sources:**
- https://github.com/OWASP/crAPI/blob/develop/docs/challenges.md (Challenge 7)
- https://github.com/OWASP/crAPI/blob/develop/openapi-spec/crapi-openapi-spec.json (declared admin delete operation)

## API5 controlled-delete setup — owner video identified (2026-11-17)

**Researcher statement:** The video uploaded by **TesterA** has `video_id` **52** in TesterA's dashboard. This is **researcher-reported**, rather than independently verified by an uploaded dashboard response. The exact ID may be retained in private test notes; public reports should use a placeholder where practical.

**Next manual action:** Log out of TesterA and log into **TesterB**, then load a fresh authenticated `GET /identity/api/v2/user/dashboard` in ZAP Requester. Confirm the Bearer token belongs to TesterB and do not send the delete yet. The intended one-time authorization check will be `DELETE /identity/api/v2/admin/videos/52` with TesterB's *ordinary-user* token, only against the intentionally disposable TesterA video. Test may permanently delete the video. Confirm deletion (or non-deletion) from a fresh TesterA dashboard response after the request. No API5 vulnerability has been observed so far.

**Authoritative endpoint source:** https://github.com/OWASP/crAPI/blob/develop/openapi-spec/crapi-openapi-spec.json (admin video DELETE operation).

**Secret hygiene:** JWT, cookies, account identity and raw screenshots must not be published in the public repository.
