# API03 — Community Forum Discloses Author Email and Vehicle Identifier

**Category:** OWASP API3:2023 — Broken Object Property Level Authorization (Excessive Data Exposure)  
**Target:** Authorized, local OWASP crAPI lab (`http://localhost:8888`)  
**Status:** **Confirmed in local lab — cross-account field exposure**; policy-specific severity and downstream exploit chain not independently verified  
**Provisional severity:** Medium (qualitative, pending data-classification/impact review; no CVSS score assigned)  
**Test date:** 2026-11-16  
**Authentication:** Normal authenticated research-owned accounts TesterB and TesterA; no forged token and no write request required

## Executive summary

The application's Community Forum shows post title, content, author display name and posting date. The API providing those posts returns additional nested author properties, including each post author's **email address** (`author.email`) and **vehicle identifier** (`author.vehicleid`). These properties appear in successful responses associated with two separate authenticated test accounts, although neither was shown in the Forum UI.

The data are sent to the client regardless of whether the interface displays them. The exposure of email/contact information and vehicle identifiers increases the amount of third-party user information available through the standard post-feed call.

## Endpoint

```http
GET /community/api/v2/community/posts/recent?limit=30&offset=0 HTTP/1.1
Host: localhost:8888
Authorization: Bearer <REDACTED>
```

### Response shape (sanitized example; not a verbatim response)

```json
{
  "posts": [
    {
      "id": "<REDACTED>",
      "title": "<REDACTED>",
      "content": "<REDACTED>",
      "author": {
        "nickname": "<REDACTED>",
        "email": "<REDACTED>",
        "vehicleid": "<REDACTED>",
        "profile_pic_url": "<REDACTED>",
        "created_at": "<REDACTED>"
      },
      "comments": [],
      "authorid": "<REDACTED>",
      "CreatedAt": "<REDACTED>"
    }
  ],
  "next_offset": null,
  "previous_offset": null,
  "total": 3
}
```

## Researcher evidence

| Observation | Authenticated session | ZAP History | Result |
|---|---|---|---|
| Normal Community → Forum page | TesterB (researcher-provided UI screenshot) | n/a | Post authors, titles, dates and text visible; no email or vehicle-ID fields displayed |
| Forum post-feed GET | TesterB | **352** | **200 OK**, JSON response **1007 bytes** with `author.email` and `author.vehicleid` in each post |
| New authentication and dashboard activity | Researcher switched to TesterA per instructed workflow | **354**, **355** and related | Login/dashboard succeeded (HTTP 200 in History) |
| Forum post-feed GET | TesterA (per researcher workflow; fresh login seen preceding request) | **360** | **200 OK**, JSON response **1007 bytes**; nested author emails and vehicle IDs again visible |

Response structure contains other metadata such as `authorid` and `author.created_at`, but their presence alone does not establish sensitivity. Values are omitted.

## Reproduction steps (local, authorized lab)

1. Sign in with research-owned **TesterB**, visit **Community → Forum**, note what fields the page displays.
2. Capture the normal `GET /community/api/v2/community/posts/recent?limit=30&offset=0` in OWASP ZAP.
3. Inspect `Response → Body` and observe `author.email` and `author.vehicleid` for forum post authors.
4. Sign out and sign in with independent, research-owned **TesterA**; revisit the same Forum.
5. Capture the new ordinary GET request and inspect its JSON. The same categories of additional author properties are returned.

## Security impact and limitations

- **Verified:** Two authenticated test-account views can retrieve author emails and vehicle identifiers through a feed whose displayed UI does not require those properties.
- **Potential impact:** The email values are identifiable contact data. A vehicle identifier may help locate corresponding vehicle resources in an application with insecure object-level authorization. A distinct **API1 BOLA** weakness was already documented in this local lab, but **no exploit chain from these particular forum-derived vehicle IDs into location/contact data has been executed as part of this finding**.
- **Not independently established:** The product's intended privacy policy, whether email/vehicle identifiers are explicitly intended to be shared, unauthenticated accessibility of the feed, or the scope of other affected accounts. Do not claim broader exposure or a CVSS score without further evidence.
- **Classification:** The observed excess exposure is directly supported by the two-account screenshots and matches OWASP API3 guidance about property-level authorization; the ultimate severity is provisional.

## Recommended remediation

1. Use a **server-side response allowlist** for forum summaries, returning only fields required by the client: e.g. title, content, author nickname, creation date and genuinely necessary public avatar metadata.
2. Remove `author.email`, `author.vehicleid` and other nonessential internal properties from the public/community post DTO by default.
3. If a property must be exposed for a privileged workflow, require explicit property-level authorization in the relevant dedicated endpoint.
4. Add automated tests asserting neither unrelated author email nor vehicle IDs are present in standard community-feed responses across multiple account roles.
5. Reassess endpoints accepting leaked identifiers, especially any remaining BOLA paths.

## Evidence handling

The raw researcher screenshots contain account emails, bearer JWTs, session cookies and vehicle IDs. **Do not upload unredacted screenshots to this public GitHub repository or portfolio.** This report contains only redacted illustrative response data and nonsecret request metadata.

## References

- https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/
- https://owasp.github.io/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/12-API_Testing/03-Excessive_Data_Exposure
- https://github.com/OWASP/crAPI/blob/develop/docs/challenges.md (Challenge 4)
- Related local lab result: [API1 BOLA](API01-BOLA.md)
