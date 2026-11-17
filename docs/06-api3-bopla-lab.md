# API3:2023 — Broken Object Property Level Authorization (BOPLA) lab

**Target:** Researcher-owned, self-hosted OWASP crAPI at `http://localhost:8888`  
**Status:** Cross-account excessive property exposure confirmed in local lab; severity and downstream impact remain provisional  
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

## API3 scope correction — Forum posts rather than profile videos (2026-11-16)

**Evidence received:** The researcher supplied a screenshot of the authenticated TesterB session at `http://localhost:8888/forum` under **Community → Forum**. It shows a feed of three user posts with titles, poster names, dates and brief text; **no video widget is visible in the Forum view**. Do not claim that the current crAPI build lacks video features entirely: video-upload flows are associated with **user profile / personal video**, not this Forum screen.

**Adjusted initial investigation:** Start with the read-only **crAPI Challenge 4** (Excessive Data Exposure in community posts), rather than requiring a video upload for Challenge 5.

**Candidate endpoint:** `GET /community/api/v2/community/posts/recent` is documented in third-party crAPI research; **not yet independently observed in this researcher's ZAP session**. First locate the actual GET for community posts in ZAP History (search for `posts` or `posts/recent`) and inspect Response Body.

**What to compare:** The visible feed displays post title, author display name, date and content. Enumerate the response's JSON property **names** and compare to those visible fields; assess whether extra fields contain potentially sensitive user/contact/internal data. A field being absent from the UI is **not by itself proof of an information disclosure**—sensitivity, access expectations, and impact must be established.

**Evidence status:** Only UI observation; no community-post JSON response examined yet and no API3 finding confirmed.

References:
- https://owasp.github.io/www-project-crapi/ (Challenges 4 and 5)
- https://cybersec-research.space/posts/crAPI_writeup/ (example community post endpoints)
- https://www.zaproxy.org/docs/desktop/start/features/history/

## API3 baseline B1 — community posts reveal additional author properties (2026-11-16)

**Evidence:** Researcher-provided OWASP ZAP screenshot, **History ID 352**, compared with their previously provided authenticated Forum UI screenshot. Researcher was signed in as their own TesterB test account.

| Property | Observed |
|---|---|
| Method | `GET` |
| Endpoint | `/community/api/v2/community/posts/recent?limit=30&offset=0` |
| Target | `http://localhost:8888` (researcher-owned OWASP crAPI lab) |
| HTTP response | `200 OK` |
| Response Content-Type | `application/json` |
| Response body size | 1007 bytes |
| Number of posts in response | 3 (`"total":3`) |

**Response structure / property names observed:**
- Top-level: `posts`, `next_offset`, `previous_offset`, `total`.
- Each observed post: `id`, `title`, `content`, `author`, `comments`, `authorid`, `CreatedAt`.
- Nested `author`: `nickname`, `email`, `vehicleid`, `profile_pic_url`, `created_at`.

**UI comparison:** The screenshot of `/forum` displays post title, author nickname, posting date, and content. The post-feed response **also includes each author's email address and vehicle identifier**, neither visibly shown in the provided Forum UI screenshot. Numeric author IDs and author-account creation timestamps are likewise returned and not shown as primary Forum labels. The screenshots show data for multiple post authors rather than merely the logged-in user.

**Potential security relevance:** `author.email` is contact information; `author.vehicleid` may enable correlation with vehicle-related API operations. Because a separate API1 BOLA issue was confirmed in this same lab, exposing vehicle IDs could increase exploitability **if** an exposed ID is usable in the vulnerable vehicle endpoints. Such an exploit chain has **not** been demonstrated with these specific Forum-derived identifiers; do not claim it. API returns additional properties; whether exposure violates the intended authorization/privacy policy and affects unrelated users requires a controlled second-account read-only check.

**Current assessment:** **Potential API3 excessive-data-exposure finding — under validation**. Presence of fields outside the UI is directly observed, but their intended disclosure and concrete impact are not yet independently verified. No further security-sensitive data was extracted.

**Next step:** Sign in to the local crAPI Forum using research-owned **TesterA** and capture its normal `GET /community/api/v2/community/posts/recent?limit=30&offset=0` in ZAP. Compare the set of author-property names and confirm whether other authors' `email` and `vehicleid` properties are returned to that different account as well. No request tampering, password guessing, or write operations are needed.

**Evidence hygiene:** Original ZAP screenshot contains a complete Bearer JWT, session cookie, email addresses and vehicle IDs. **Do not upload the screenshot as-is** to this public GitHub repository; all values are omitted in this sanitized text record.

## API3 follow-up B2 — second-account confirmation (2026-11-16)

**Evidence:** Researcher-supplied OWASP ZAP screenshot from the second research-owned account (**TesterA**, per test instructions). History records a new login at **354** and successful dashboard API traffic at **355**, followed by GET request **360**.

| Observation | TesterB baseline | TesterA follow-up |
|---|---|---|
| History ID | 352 | **360** |
| Endpoint | `GET /community/api/v2/community/posts/recent?limit=30&offset=0` | Same endpoint |
| HTTP status | `200 OK` | `200 OK` |
| JSON body size | 1007 bytes | 1007 bytes |
| Returned posts | 3 | 3 |
| `posts[].author.email` | Visible in JSON | **Visible in JSON** |
| `posts[].author.vehicleid` | Visible in JSON | **Visible in JSON** |
| UI comparison | Email/vehicle ID not displayed in Forum | Normal authenticated view of same Forum |

**Conclusion:** The same sensitive author property categories are returned to **two independently authenticated research-owned sessions**, including other post authors. This is a **confirmed local-lab cross-account exposure of surplus author properties**, matching the excess-data-exposure side of OWASP API3:2023. The application's explicit privacy policy, intended public disclosure, and exploitability of these particular vehicle IDs in the separate BOLA endpoint are **not** independently established; severity is provisional. The researcher did not exploit the IDs from this response.

**Formal sanitized report:** [API03 — Community Forum Discloses Author Email and Vehicle Identifier](../findings/API03-EXCESSIVE-DATA-EXPOSURE.md).

**Safe next test:** If continuing API3, pursue another property-level scenario (e.g. Mass Assignment) with the researcher's own disposable account and reversible field updates only. Avoid publishing full JWTs, emails, cookies or vehicle IDs.

**Evidence hygiene:** The raw screenshot contains an active-looking Bearer token, session cookie, addresses and vehicle identifiers. Keep unredacted images out of public GitHub, LinkedIn, and Upwork.

## API3 profile surface B3 — editable profile capabilities identified (2026-11-16)

**Evidence:** Researcher-provided screenshot of their own TesterA profile at `http://localhost:8888/my-profile`.

**Visible UI:** name (displayed), email with **Change email** button, phone number with **Change phone number** button, avatar change control, and **My Personal Video → Upload Video** (maximum upload size shown as 10 MB). No API endpoint or profile-update request is visible in this screenshot.

**Interpretation:** The profile page exposes potential update surfaces for an authorized, carefully controlled **Mass Assignment** test (API3 writable properties). The video-upload feature is located under profile, not the Community Forum view previously tested. Do not assume the existence or name of a profile-update endpoint until an actual ZAP request is observed.

**Next step:** Click **Change phone number** and inspect the form without submitting changes. After observing its normal flow, locate the actual request in ZAP History, identify expected writable fields, and only then design a low-impact test using the researcher's own disposable TesterA data. No mass-assignment flaw has been tested or confirmed.

## API3 profile workflow B4 — change-phone-number form observed (2026-11-16)

**Evidence:** Researcher-provided screenshot of TesterA's own browser at `http://localhost:8888/change-phone-number`.

**Visible behavior:** A two-step account phone-change UI: (1) **New Phone Number** text field and **Send OTP for verification** button; (2) **OTP Verification** stage not yet reached. No ZAP write request or server response for this flow has yet been captured.

**Interpretation:** This is a candidate writable-property API3 surface, but neither a Mass Assignment weakness nor a bypass of OTP has been shown. The first form probably initiates verification, not necessarily the final property update; do not infer endpoint names, request field names, or server validation behavior from this UI.

**Next minimal action:** Enter a dedicated, non-routable lab test phone value in TesterA's own session, click **Send OTP for verification** once, and capture the resulting actual network request and response via ZAP. Do not complete the verification or modify request properties until the request's purpose and fields are understood. If the app or environment could send real SMS, use a controlled test number only and avoid third-party recipients.

**Evidence policy:** Redact phone, authorization headers, OTPs and session cookies from any shared screenshot and all public commits.

## API3 phone-change baseline B5 — OTP initiation request captured (2026-11-16)

**Evidence:** Researcher-provided ZAP Request/Response screenshot from the researcher-owned TesterA profile flow on their local crAPI lab.

| Property | Observed |
|---|---|
| Method | `POST` |
| Path | `/identity/api/v2/user/change-phone-number` |
| Target | `http://localhost:8888` |
| Authorization | Bearer JWT header present (full token not retained) |
| Request Content-Type | `application/json` |
| JSON request keys | `old_number`, `new_number` (actual values omitted) |
| HTTP response | `200 OK` |
| Response summary | Server says OTP was sent to the test account's email and can be read through local MailHog; it echoes the requested new number in the message (actual value omitted) |

**Interpretation:** The observed `200` is **OTP initiation**, not evidence of an actual phone update. The user interface shows a separate second-stage OTP verification step. This request alone does not indicate a mass-assignment vulnerability, and guessing an additional writable property before observing the final verification request could mischaracterize the flow.

**Next minimum action:** In the researcher's local MailHog, find the newly generated phone-change OTP for TesterA (do not share or commit its value), enter it in the ordinary crAPI verification form, then inspect the next POST request in ZAP for actual confirmation endpoint and request keys. This baseline may update the researcher's disposable test phone number after successful verification; ensure the value is owned/reversible and note the account's resulting state. Do not modify request bodies or include unapproved properties until this baseline is understood.

**Sensitive evidence:** The screenshot exposes a bearer JWT, session cookie, and test phone numbers. Never upload this raw screenshot to a public GitHub or portfolio page. Preserve only redacted field names, endpoint, response status and sanitized interpretation.

## API3 phone-change positive baseline B6 — phone OTP verification succeeded (2026-11-16)

**Evidence:** Researcher-supplied ZAP Request/Response screenshot for the researcher-owned TesterA account on local `http://localhost:8888`.

| Item | Observation |
|---|---|
| Request | `POST /identity/api/v2/user/verify-phone-otp` |
| Request header | `Authorization: Bearer` present; token not retained |
| Request content type | `application/json` |
| Request JSON keys | `old_number`, `new_number`, `otp` (all values redacted) |
| HTTP response | `200 OK` |
| Response body | `{"message":"Phone number change is successful","status":200}` |

**Interpretation:** The application reports that the normally authorized OTP-confirmed phone change succeeded. This is a **positive baseline** for an allowed property update, **not evidence of Mass Assignment**. The account's persisted phone number has not yet been independently verified from a fresh profile read or authenticated user-dashboard response.

**Next single action:** Revisit `/my-profile` as TesterA or inspect a fresh `GET /identity/api/v2/user/dashboard` in ZAP. Verify that `phone` now shows the new test number and examine which other profile properties are returned, without recording their values. This gives a reliable persisted-state baseline and reveals candidate property names for a later controlled extra-field test. Do not add arbitrary attributes or replay this already consumed OTP in the baseline phase.

**Security / disclosure:** The raw screenshot contains a complete JWT, session cookie, lab OTP and test phone numbers. Do not publish the screenshot or its secret values in GitHub/Upwork/LinkedIn. This report retains only field names and sanitized response metadata.

## Python-assisted workflow B7 — read-only dashboard baseline (2026-11-17)

**Status:** Script created in public GitHub repository; **not yet run by the researcher on their Mac**. Therefore no new local crAPI response or property status has been observed.

**Artifacts:**
- [Python script](../scripts/api03_profile_baseline.py)
- [Setup and safety instructions](../scripts/README.md)
- [Dependency declaration](../scripts/requirements.txt)

**Workflow:** Authenticate TesterA by a direct localhost POST (hidden input, password not sent via ZAP), make exactly one authenticated `GET /identity/api/v2/user/dashboard` via ZAP's locally configured port 8081, print sanitized JSON field names and types, and optionally compare the requested test phone value against a phone-like field without showing raw values. If no phone property is returned, the script states the comparison is unavailable and asks the researcher to verify in the refreshed profile instead.

**Why:** Establish a precise, reproducible post-change profile baseline before designing a single controlled property mutation test for Mass Assignment. Keep all credentials, OTPs, JWTs, cookies and phone values out of public GitHub artifacts.

**Next step:** The researcher runs the script locally and shares only HTTP status, field names and phone-comparison state. Do not claim the phone is persisted or Mass Assignment is confirmed before reading the actual results.

## Python baseline B8 — successful local run (2026-11-17)

**Evidence source:** Researcher-provided terminal output from their own Mac, not an independently executed remote test.

**Execution environment:** Local Python virtual environment `.venv`, `requests` installed from `scripts/requirements.txt`, OWASP crAPI at `http://localhost:8888`, OWASP ZAP configured as `http://127.0.0.1:8081`.

**Command:** `python scripts/api03_profile_baseline.py`  
**Result:** TesterA login succeeded; authenticated `GET /identity/api/v2/user/dashboard` returned **HTTP 200**, using the ZAP proxy for the read-only GET. No credentials or response values were printed. The user skipped the optional phone-number comparison, so the newly set phone value **has not been independently verified** by this run.

**Structural output (no personal values):**

| JSON property | Python type |
|---|---|
| `id` | `int` |
| `name` | `str` |
| `email` | `str` |
| `number` | `str` |
| `picture_url` | `NoneType` |
| `video_url` | `NoneType` |
| `video_name` | `NoneType` |
| `available_credit` | `float` |
| `video_id` | `int` |
| `role` | `str` |

**Interpretation:** The script now has a verified successful *execution baseline* for this researcher's local lab. Field existence is not itself a mass-assignment vulnerability: write operations and persisted-property authorization still require separate controlled verification.

**Next step:** Run the same script again, this time entering the expected new test phone at the hidden comparison prompt. Confirm `Phone comparison: MATCH` before proceeding to a low-impact write-property test. A mismatch or unavailable result must not be labeled a vulnerability without further checks.

**Evidence hygiene:** No JWT, password, OTP, phone value, email address, or ZAP session is copied into this repository.

## API3 manual Mass Assignment probe B9 — prepared in ZAP Requester (2026-11-17)

**Evidence:** Researcher-provided screenshot shows the researcher-owned TesterA account's previously captured `POST /identity/api/v2/user/change-phone-number` loaded in ZAP Requester Tab 4. This is an **old** successful OTP initiation request; no new mutation test result has yet been provided.

**Baseline:** The current test phone number was subsequently confirmed persisted via `scripts/api03_profile_baseline.py` (`Phone comparison: MATCH`).

**Planned controlled manual test — not yet executed or verified:**

1. Update `old_number` to the currently saved TesterA test phone (do not reuse the stale value from the previously captured request).
2. Set `new_number` to another disposable, researcher-controlled test phone value, different from the current number.
3. Add exactly one extra **benign** JSON property `"name":"MassAssignProbeA"` to the initiation request. Avoid attempting changes to `role`, `available_credit` or third-party properties.
4. Send once in ZAP Requester. Do **not** submit the new OTP yet.
5. Obtain a fresh authorized read-only dashboard GET and compare its `name` property against the expected original TesterA name **without publishing personal values**. If the extra field unexpectedly changes the name on OTP initiation alone, reproduce and analyze; if unchanged, this single endpoint-stage test does **not** rule out mass assignment at the final verification endpoint or elsewhere.

**Interpretation:** A `200` OTP-sent response means only OTP initiation succeeded, not that `name` was modified, not that phone change was finalized, and not that Mass Assignment was found.

**Disclosure:** The source ZAP Requester screenshot contains a JWT, session cookie and test phone numbers. Do not upload it unredacted to public GitHub or portfolio.

## API3 manual mass-assignment probe B10 — request rejected by input validation (2026-11-17)

**Evidence:** Researcher-provided ZAP Requester screenshot of a manual `POST /identity/api/v2/user/change-phone-number` in the authorized local crAPI lab; ZAP History **375**, Source `Manual`.

**Request structure:** `old_number`, `new_number`, and an extra proposed property `name` with a benign lab marker. The researcher sent the *illustrative placeholders* `CURRENT_TEST_PHONE` and `ANOTHER_TEST_PHONE` instead of actual valid lab phone values.

**HTTP result:** `400 Bad Request`, JSON error `Validation failed`. The response names rejected input values and Spring/Java validation detail for `old_number` and `new_number`, including length/size rules.

**Interpretation:** The request failed **input validation** for phone-number values. It does not demonstrate that the additional `name` property was accepted, persisted, or rejected by any property-authorization logic. **No Mass Assignment finding is confirmed.** The verbose framework validation output may be considered in a separate error-handling review, but is not on its own proof of a serious information leak.

**Next manual-only action:** In ZAP Requester, replace placeholder values with the researcher's own current valid test phone and another controlled valid-format test number; preserve the single benign `name` probe field. Send once, do **not** complete OTP. Next obtain a fresh read-only Dashboard response in ZAP and check whether `name` actually changed. If `200` merely initiates an OTP, that alone cannot establish a mass-assignment issue.

**Workflow preference:** The researcher requested **manual-only testing with OWASP ZAP** until they complete separate Python training. Do not propose or require scripting for subsequent lab steps unless the researcher explicitly asks to resume.

**Sensitive evidence:** Screenshot shows a Bearer JWT and test-account details. No raw screenshot, token, cookie, or user values are included in public GitHub documentation.

## API3 manual probe B11 — duplicate phone prevented field-assignment assessment (2026-11-17)

**Evidence:** Researcher-provided ZAP Requester screenshot, manual **History ID 376**.

| Attribute | Observed |
|---|---|
| HTTP method | `POST` |
| Path | `/identity/api/v2/user/change-phone-number` |
| JSON keys | `old_number`, `new_number`, extra benign `name` marker |
| Response status | **`403 Forbidden`** |
| Response message (sanitized) | `Number already registered!` |

**Interpretation:** The researcher reused the previously registered new test phone in the `new_number` field, while retaining the pre-change number in `old_number`. The endpoint rejected the duplicate-number condition. This is **not** evidence that the extra `name` field was accepted, rejected, or persisted; no Mass Assignment flaw has been confirmed. The earlier tester-owned phone update was independently verified by the researcher's read-only Python baseline (`Phone comparison: MATCH`).

**Next manual-only step:** In the same private ZAP Requester tab, use the currently persisted phone in `old_number` and an entirely new, unregistered, controlled test phone in `new_number`; keep the benign `name` marker unchanged and send once. Do not complete OTP at this stage. Inspect the response, then verify account `name` by a fresh authorized GET. An OTP-initiation HTTP 200 does not by itself mean the extra property was saved.

**Evidence hygiene:** The screenshot contains a live-looking bearer JWT, cookie and test phone numbers. Omit values and raw screenshots from public documentation. The researcher requests **manual-only** ZAP testing, without scripting.
