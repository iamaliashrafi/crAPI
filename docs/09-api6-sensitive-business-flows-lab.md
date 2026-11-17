# API6:2023 — Unrestricted Access to Sensitive Business Flows (crAPI)

**Assessment target:** Authorized self-hosted OWASP crAPI at `http://localhost:8888`  
**Method:** OWASP ZAP + browser **manual only**, per researcher's request  
**Status:** Planned — no API6 requests executed or vulnerability confirmed yet  
**Started:** 2026-11-17

## Category definition

API6 addresses excessive **legitimate-looking use of business workflows** (rather than missing role authorization): examples include ticket scalping, reservation hoarding, spam comments/posts, fraudulent referral rewards, or abusive order flows. The risk is business-specific. The mere existence of an endpoint or acceptance of two requests is **not** sufficient proof of API6 vulnerability.

Official OWASP guidance: https://api-security.owasp.org/editions/2023/en/0xa6-unrestricted-access-to-sensitive-business-flows/

## Selected low-impact local scenario — community forum anti-spam safeguards

The crAPI Community → Forum feature can create user-generated posts. This is a business-flow abuse candidate because unrestricted high-frequency post creation can spam the forum and degrade legitimate usage. This exact API6 classification is a **test scenario**, not an official crAPI challenge solved or a confirmed implementation weakness.

**Anticipated endpoint (confirm with actual ZAP capture):** `POST /community/api/v2/community/posts`. The crAPI OpenAPI description defines `title` and `content`; confirm actual fields from the researcher's own browser traffic.

### Controlled manual procedure

1. Log in to the researcher-owned **TesterB** account, open **Community → Forum → New Post**.
2. Create **one benign identifiable disposable post**:
   - Title: `API6-LAB-POST-01`
   - Content: `Authorized local API6 anti-spam control test.`
3. In ZAP History, locate the corresponding **POST**. Record method, path, response status, response fields, and visible anti-automation/rate-limit headers, with secrets redacted.
4. **After reviewing that baseline**, send **at most one** identical replay from ZAP Requester to observe duplicate-post behavior; do not run a fuzzer, concurrent requests, or a large batch.
5. Check whether the second post actually exists and whether a human-verification, cooldown, or duplicate check was observed. If no protection is observed on two posts, only a **very limited signal** has been collected; real abuse resistance and business impact remain **unverified**.
6. Clean up test posts if a safe authorized deletion operation is available. Do not delete other users' posts.

### What counts as evidence

| Observation | Interpretation |
|---|---|
| First post succeeds | Normal business workflow baseline; not a vulnerability |
| Second identical manual post denied due to duplicate/cooldown | A local protection is observed; other abuse scenarios untested |
| Both posts succeed | A small number of posts is permitted; **not enough to confirm unlimited spam or API6 vulnerability** |
| Rate-limit headers absent | Not a finding by itself |
| 4xx/5xx | Inspect actual response and verify if temporary error, validation, or anti-abuse control |

### Safety boundaries

- **No flooding, high-volume fuzzing, account-registration loops, repeated orders, stock exhaustion, or real-world external service costs.**
- This local lab is intentionally vulnerable but resource-consumption/availability effects should be avoided.
- No scripting; the researcher explicitly deferred Python scripts until studying scripting separately.
- Keep all authorization tokens, session cookies, phone numbers, post IDs tied to personal data, and unredacted ZAP screenshots private.

## Previous category closure

API5 **BFLA** was confirmed in this local lab: a disposable video reported owned by TesterA was deleted through `DELETE /identity/api/v2/admin/videos/52` using the researcher's reported TesterB ordinary-user authentication, HTTP 200, and the researcher subsequently confirmed the video had disappeared from TesterA's profile. Report: [API05-BFLA-001](../findings/API05-BFLA-UNAUTHORIZED-VIDEO-DELETION.md).

## Sources

- https://api-security.owasp.org/editions/2023/en/0xa6-unrestricted-access-to-sensitive-business-flows/
- https://github.com/OWASP/crAPI/tree/develop/openapi-spec
- https://owasp.github.io/www-project-crapi/

## API6 A1/A2 — first Forum post and one manual duplicate submission (2026-11-17)

**Evidence:** Researcher-supplied OWASP ZAP Requester screenshot from the researcher's own local crAPI lab, with previously authorized test account TesterB.

| Check | Observation |
|---|---|
| Normal `POST /community/api/v2/community/posts` | ZAP History **476**, source Proxy, HTTP **200 OK**, response body **372 bytes** |
| Initial list GET | ZAP History **477**, HTTP **200 OK**; occurred **before** manual replay, so not proof of duplicate persistence |
| Manual `POST /community/api/v2/community/posts` | ZAP History **478**, source Manual, HTTP **200 OK**, response body **370 bytes** |
| Request properties in shown Requester | `title`, `content` |
| Title in both steps (per instructed workflow) | `API6-LAB-POST-01` |
| Manual 478 response | One post-shaped JSON object with a generated `id`, the submitted title/content, and `author.nickname` identifying TesterB; status HTTP 200 |
| Actual duplicate stored | **Not yet independently verified** by a fresh post-feed GET after History 478 |

**Interpretation:** Two low-volume, seemingly identical post-creation requests returned HTTP 200. The server's second response reports a newly created post, but the persisted existence of two distinct posts has **not yet been verified** after the manual replay. Even successful storage of two posts would not prove unrestricted automated posting, missing anti-spam controls or a business-impactful **API6** vulnerability. **Do not replay again or run a Fuzzer.**

**Next read-only check:** Refresh the researcher's own Community → Forum page, then inspect the newest `GET /community/api/v2/community/posts/recent` in ZAP Response Body. Count post objects titled `API6-LAB-POST-01` and check whether any have distinct IDs. Report only the count; do not upload bearer JWTs, session cookies, author emails, or vehicle IDs.

**Evidence hygiene:** The screenshot contains a Bearer token and nested author identity/contact/vehicle details. The public documentation records only sanitized properties and metadata.
