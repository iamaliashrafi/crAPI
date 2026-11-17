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
