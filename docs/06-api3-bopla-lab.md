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
