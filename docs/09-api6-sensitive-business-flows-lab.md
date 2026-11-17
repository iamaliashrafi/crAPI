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
