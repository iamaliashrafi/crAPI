# API4:2023 — Unrestricted Resource Consumption (crAPI lab)

**Scope:** Researcher's authorized local OWASP crAPI instance (`http://localhost:8888`)  
**Status:** Planned; no API4 requests or vulnerability observations yet  
**Method:** Manual ZAP only (researcher explicitly requested no scripts)  
**Safety:** Prefer small, sequential, read-only parameter-boundary checks. **Do not launch layer-7 DoS, high-volume fuzzing, parallel flood traffic, or expensive external API calls.**

## What API4 means

Excessive requests or costly inputs can consume server CPU, RAM, disk, bandwidth, database resources, third-party spend, or service availability. Relevant controls include rate limits, timeouts, maximum request/upload sizes, pagination bounds and third-party cost quotas.

Official reference: https://api-security.owasp.org/editions/2023/en/0xa4-unrestricted-resource-consumption/

**crAPI official challenge context:** Challenge 6 is titled "Perform a layer 7 DoS using 'contact mechanic' feature". It is deliberately disruptive by description, so our first API4 exercise is **not** that DoS attack. We begin with an innocuous, already-observed pagination endpoint. Source: https://github.com/OWASP/crAPI/blob/develop/docs/challenges.md

## Initial test A1 — bounded pagination input (read-only)

**Previously observed target:** `GET /community/api/v2/community/posts/recent?limit=30&offset=0`, captured during API3 with researcher-owned authorized sessions (ZAP History 352 / 360).

**Question:** Does the server reject, clamp or accept client-supplied `limit` values? This is a parameter-validation **discovery step**, not by itself proof of uncontrolled resource consumption.

### Manual baseline sequence

1. Open a previously captured authenticated GET to `/community/api/v2/community/posts/recent?limit=30&offset=0` in ZAP Requester.
2. Check the Bearer token is still valid; if not, refresh it via ordinary authorized login and new forum navigation. Never paste the token into public notes.
3. Make **one** read-only edit: change `limit=30` to `limit=100`. Keep `offset=0` and all other request details unchanged. Send **once**, not repeatedly.
4. Record HTTP status, response content-type, `posts` array length, `total`, response size and time (if shown), and any validation/error message. Redact response values in screenshots.
5. Stop and analyze. **The lab currently has only three Forum posts**, so seeing three posts even with `limit=100` will **not establish a maximum page-size bound or a vulnerability**.

### Interpretation guide

| Observation | What it does / does not show |
|---|---|
| HTTP 400 on 100 | Input validation may enforce a maximum; inspect explicit error |
| HTTP 200 returning 3 posts | The request was accepted, but available data limits effective resource use; no unbounded behavior proven |
| HTTP 200 with capped count (if more than 100 posts exist) | Potential server-side clamping; verify declared policy |
| Timeout / 500 | Could have many causes; check actual response and health before any inference |

**Safety:** Do not substitute very large or negative numerical values, run bulk iterations, trigger paid services, upload large files, or deliberately exhaust CPU/memory. This project is educational manual testing, not an availability attack.

## Prior category transition

API3 community post-feed disclosure was confirmed in the lab across TesterA and TesterB and remains documented in `findings/API03-EXCESSIVE-DATA-EXPOSURE.md`. The separate Mass Assignment phone-change experiment did not establish a vulnerability. Its most recent modified final-OTP request returned HTTP 500 / JSON status 403 with `Fail, invalid new number`; this **does not prove Mass Assignment is absent**.

## Evidence and reporting

Retain only sanitized endpoint details, test conditions, observed status, status messages, timing and size; never publicly commit request headers with JWTs, cookies, OTPs, user identities or phone numbers.

**No API4 finding confirmed.** The above is a planned procedure pending the researcher's manual ZAP response.

## API4 A1 — pagination limit 100, read-only manual control (2026-11-17)

**Evidence:** Researcher-supplied screenshot of an OWASP ZAP Requester test on their own localhost crAPI lab. The screenshot shows the request and response; no load generation or application changes were involved.

| Attribute | Observation |
|---|---|
| Method | `GET` |
| Path | `/community/api/v2/community/posts/recent?limit=100&offset=0` |
| HTTP status | **`200 OK`** |
| Response type | `application/json` |
| Response body length | **1,007 bytes** |
| ZAP reported elapsed time | **53 ms** |
| Posts present | **3** (the same three as in the earlier `limit=30` authenticated baseline) |

**Interpretation:** The server accepted the client-supplied `limit=100` and returned only the three available records. This does **not** establish that the backend enforces or lacks a pagination cap: the dataset is smaller than either tested limit. No resource exhaustion, abnormal latency or API4 vulnerability was demonstrated by this one request. A response size around 1007 bytes is unsurprising for three posts and is not evidence of unbounded allocation.

**Next bounded, manual-only check:** Change only `limit=100` to `limit=0` in the same GET request and send once, keeping `offset=0`. Inspect the status and body. This is a safe input-boundary/validation probe, **not** a load test. If the endpoint rejects zero (4xx), note the validation rule; if it accepts zero, record whether it returns an empty list, a default page size, or an error. No repeated or very large requests.

**Safety and evidence:** The screenshot includes a Bearer JWT, session material, author emails and vehicle IDs. Do not publish the raw screenshot or any values in GitHub; preserve only the redacted request metadata and measurements here.

## API4 A2 — zero-page-size boundary check (2026-11-17)

**Evidence:** Researcher-supplied OWASP ZAP Requester screenshot from their authorized local crAPI lab.

| Attribute | Observation |
|---|---|
| Method | `GET` |
| Path | `/community/api/v2/community/posts/recent?limit=0&offset=0` |
| HTTP status | **`200 OK`** |
| Content type | `application/json` |
| ZAP-reported response body length | **1,001 bytes** |
| ZAP-reported elapsed time | **39 ms** |
| Posts in visible JSON | Three existing post objects |

**Comparison:** The earlier `limit=100` single-request check returned HTTP 200 with three posts, body length 1,007 bytes, and 53 ms; the same known dataset consists of only three posts. The six-byte body-size difference might reflect pagination metadata or other JSON response differences, but the exact source has **not** been verified. Avoid claiming the response bodies are identical.

**Interpretation:** The endpoint did not reject a zero `limit` and returned existing posts, rather than an empty list. The reason is not established; possible interpretations include default-value fallback or special handling of zero. This is a **pagination-input semantics observation**, not evidence of unrestricted resource consumption, missing server-side upper bounds, or resource exhaustion. No API4 finding confirmed.

**Next low-impact manual control:** Change only `limit=0` to `limit=1`, leave `offset=0`, and send one read-only GET through ZAP Requester. Inspect whether the API returns **one post** or ignores the requested count. This checks whether the parameter is effective without introducing load. Do not conduct a flood or very-large-limit probe.

**Evidence hygiene:** The screenshot visibly contains a Bearer JWT, and the response includes author email addresses and vehicle identifiers; don't upload it unredacted to public GitHub.

## API4 A3 — positive pagination limit one (2026-11-17)

**Evidence:** Researcher-supplied ZAP Requester screenshot from their own localhost crAPI lab.

| Property | Observation |
|---|---|
| Request | `GET /community/api/v2/community/posts/recent?limit=1&offset=0` |
| Response | HTTP **200 OK**, `application/json` |
| Returned post objects | **1** |
| JSON `next_offset` | **1** |
| JSON `previous_offset` | `null` |
| JSON `total` | **1** (reported by the API for this response; do not confuse with independently established global post count) |
| Response body length | **376 bytes** |
| ZAP reported time | **38 ms** |

**Comparison across A1–A3:**
- `limit=100`: HTTP 200, **3** posts, 1007-byte body, 53 ms.
- `limit=0`: HTTP 200, **3** posts, 1001-byte body, 39 ms.
- `limit=1`: HTTP 200, **1** post, 376-byte body, 38 ms.

**Interpretation:** A positive limit of 1 demonstrably controls the number of returned posts; a zero value did not yield an empty page in this dataset and may trigger default semantics. Since there are only three known posts, this experiment **cannot establish whether a maximum page-size limit exists**. No significant resource use or service disruption was observed; **no API4 vulnerability confirmed**. Do not continue escalating `limit` into very large values just to probe availability.

**Next candidate resource control (manual, staged, low-risk):** The researcher's previously observed `/my-profile` interface exposes a **My Personal Video → Upload Video** function and displays a **10 MB** maximum file size. Inspect that upload UI first (no upload yet) and, only after mapping the normal request and server response, design a minimal test of whether server-side file size limits are enforced. Upload controls are within API4 resource consumption scope. No concurrent uploads, flooding, or large files should be used.

**Evidence hygiene:** The raw ZAP screenshot displays a Bearer JWT and author contact / vehicle properties. This public text record intentionally omits secrets and actual post data.

## API4 A4 — oversized video upload rejected with HTTP 413 (2026-11-17)

**Evidence:** Researcher-supplied OWASP ZAP screenshot of the History panel for the researcher's self-hosted local crAPI. The Profile UI previously advertised a **10 MB** maximum for **My Personal Video**. The researcher reports testing an approximately **11 MB** video upload and says it failed.

| Property | Observed / qualified |
|---|---|
| Upload endpoint | `POST /identity/api/v2/user/videos` |
| Key ZAP History entry | **416** (proxy-captured) |
| HTTP status of entry 416 | **413 Payload Too Large** (History Code column) |
| Response-body size for 416 | **145 bytes** |
| Other nearby entries | **414** and **415** are `POST` to the same endpoint with **200**; their visible **response** body sizes are each ~3.29 MB, **not known request/upload sizes** |
| Test file size | About **11 MB**, **researcher reported**; the ZAP screenshot does not independently establish request Content-Length |
| Exact 413 response body | **Not inspected yet** |
| Rejecting component | Not yet identified (could be reverse proxy / gateway or application code) |

**Interpretation:** The observed 413 response is **evidence of a server-side or gateway-side payload size limit** for the attempted larger upload, rather than a solely client-side UI guard. This particular oversized-upload attempt **did not demonstrate bypass of the advertised 10 MB limit**. The precise configured threshold, handling of different file types, and source of 413 have not been verified; it would be inaccurate to declare the entire API4 category secure. Do not confuse response-body size with upload request size.

**Next manual-only action — no new traffic:** Select ZAP History **416** and inspect its **Response → Body** and **Response → Header**. Record whether the message names the limit or the rejecting component; inspect **Request → Header** for Content-Length without disclosing credentials or multipart contents. Do not retry the upload or perform high-volume resource testing. This is a low-impact request limit check, not a DoS attempt.

**Evidence handling:** Do not publish unredacted JWTs, cookies, emails, file content or raw ZAP captures to public GitHub.

## API4 A5 — exact oversized-upload rejection body confirmed (2026-11-17)

**Evidence:** Researcher-supplied close-up ZAP screenshot of **Response → Body** for the earlier video upload request **416**, `POST /identity/api/v2/user/videos`.

```json
{
  "type": "about:blank",
  "title": "Payload Too Large",
  "status": 413,
  "detail": "Maximum upload size exceeded",
  "instance": "/identity/api/v2/user/videos"
}
```

The associated History response status was **HTTP 413**. The researcher reports a test MP4 of approximately **11 MB** against the UI-advertised **10 MB** maximum. The close-up independently confirms the explicit server/gateway-side size-limit response, but not the exact uploaded byte count or which infrastructure component enforced the limit.

**Assessment for this case:** **Size-limit control observed — oversized upload rejected. No bypass demonstrated.** This is a defensive behavior, not a vulnerability finding. No more uploads are necessary to close this scenario. The overall API4 category is not declared secure; rate limits, concurrency, expensive business flows, and external-service quotas have not been exhaustively assessed.

**Safe continuation:** The crAPI Contact Mechanic resource-consumption challenge is related to layer-7 DoS and should **not** be performed as high-volume/disruptive traffic. If proceeding, limit work to non-disruptive review of the normal authenticated flow, or record disruptive availability testing as out of scope for this manual exercise. Alternatively move to API5 Broken Function Level Authorization.
