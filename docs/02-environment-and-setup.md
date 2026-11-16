# 02 — Environment Baseline and ZAP Setup

## Screenshot-based baseline (2026-11-16)
The researcher supplied a screenshot of OWASP ZAP beside a browser displaying crAPI at `http://localhost:8888/login`.

- ZAP is running in Standard Mode and Quick Start → Manual Explore is visible.
- The ZAP footer shows `Main Proxy: localhost:8081`.
- The History panel includes `GET http://localhost:8888/login`, status `200 OK`.
- Other origins appear under Sites. They are **not in scope**.
- Authenticated API interception, test-account creation and context filtering have **not yet been verified**.

## Session 0 — setup checklist
- [ ] Set Manual Explore URL to `http://localhost:8888`.
- [ ] Launch a browser from ZAP and confirm new crAPI traffic in History.
- [ ] Create an isolated Context called `crAPI-Lab` for the local crAPI origin.
- [ ] Use only two researcher-owned test accounts: User A and User B.
- [ ] Capture a login API request and identify its method, URL path, headers and status, **without saving secrets**.
- [ ] Record versions and relevant deployment information.

## Step 1 — browser interception
1. In ZAP Quick Start open **Manual Explore**.
2. Enter `http://localhost:8888` into **URL to explore**.
3. Keep the HUD disabled for the initial exercise (optional; it may be enabled later).
4. Choose the browser and click **Launch Browser**.
5. Navigate inside crAPI and confirm new requests in ZAP's **History**.
6. Select a relevant request. Inspect **Request** and **Response** tabs and identify the HTTP method, URL, response code, and content type.
7. Avoid copying any bearer token, cookie, password or session ID into this repository or a chat message.

## Expected evidence for this step
- A sanitized screenshot of ZAP History with a recent crAPI request.
- A short text note listing only: endpoint path, method, response status, and whether the request is an API request or page/navigation request.
- Mark this step complete only after confirming visibility of relevant API traffic.

## Troubleshooting
If a browser launched outside ZAP does not show new requests, use **Launch Browser** from Manual Explore first. If the local service is not accessible, verify the crAPI containers and `http://localhost:8888/login` before changing proxy settings. Do not modify certificates or proxy configuration unless needed.

## Configuration inventory (to fill)
| Item | Current value |
|---|---|
| Operating system | To verify |
| crAPI version/commit | To verify |
| ZAP version | To verify |
| Web application URL | http://localhost:8888 |
| ZAP main proxy | localhost:8081 (visible in screenshot; confirm) |
| Browser | Firefox (shown in screenshot; confirm) |
| Authentication model | To verify from actual traffic |

## Session 0 — follow-up screenshot review (2026-11-16)

The second user-provided screenshot shows crAPI's `/login` page next to ZAP. ZAP History includes:
- ID 48: `GET http://localhost:8888/%F0%9F%A4%96` — HTTP `404`; no vulnerability conclusion can be drawn from this alone.
- ID 49: `GET http://localhost:8888/chatbot/genai/state` — HTTP `200`, tagged as a JSON response.
- ZAP shows `Main Proxy: localhost:8081` in the footer.
- **Assessment:** local HTTP requests are being captured in History; API authentication traffic and launch via Manual Explore are not independently verified.
- Manual Explore's input field still displays `http://`, so do not claim it was populated or that Launch Browser was used.
- **Next actionable step:** create the `crAPI-Lab` Context from the `http://localhost:8888` node in Sites and verify that only this local origin is included. Then proceed with test-account setup and an authenticated API request.
- This screenshot has **not** been uploaded to the repository; the verified observations are recorded in this text.


## Session 0 — Context creation confirmed (2026-11-16)

A subsequent user-provided screenshot shows a Context named `crAPI-Lab` in the ZAP Contexts panel. The `http://localhost:8888` site remains visible in Sites and the History panel still contains locally captured traffic.

**Verified:** Context name is created and visible. **Not yet independently verified from this screenshot:** the Context's `In Scope` checkbox and complete include/exclude rules. Verify before any active scanning; other internet origins present in Sites are out of scope.

**Next action assigned:** create first researcher-controlled test account (User A) through the crAPI Signup form; inspect the resulting POST request in ZAP History without exposing credentials or tokens. User B will follow after the first signup is verified.

## Session 0 — first signup API validation (2026-11-16)

**Evidence:** a researcher-supplied screenshot of crAPI Signup alongside ZAP Request & Response. **Do not upload the raw screenshot:** it contains a plaintext test-account password, so retain only this sanitized account-free summary.

- **HTTP method:** `POST`
- **Request path:** `/identity/api/auth/signup`
- **Target:** `http://localhost:8888` (authorized local crAPI lab)
- **Observed response:** `HTTP/1.1 400`, `Content-Type: application/json`
- **Sanitized error summary:** `Validation failed` for `signUpForm.number`; validation message `must not be blank`.
- **Diagnosis:** the phone-number input was left blank and the `number` property was submitted as an empty string. Server-side request validation rejected the incomplete form.
- **Security finding?** **No.** This is expected form input validation, not evidence of an API vulnerability.
- **Follow-up:** use a fictitious test number, change the exposed test password and retry registration. Confirm success via a new request and response; do not assume the outcome.
- **Disclosure practice:** Never commit credentials, cookies, bearer tokens, or raw screenshots containing passwords; redact before sharing.

## Session 0 — test account A status (2026-11-16)

The researcher reported successfully accessing the crAPI application after retrying signup. This supports an **operator-reported successful account creation/access**, but no new ZAP screenshot has independently confirmed the successful HTTP response or token format yet. The password is for the isolated lab only; avoid sharing or reusing it.

**Next learning milestone:** inspect the corresponding login HTTP request and response in ZAP History. Record method, path, content type and status only. Do not upload plaintext passwords, bearer tokens, cookies, session identifiers or unsanitized login messages. After login interception is verified, create researcher-controlled User B for subsequent BOLA authorization testing.

## Session 0 — successful signup verified in ZAP (2026-11-16)

A user-provided screenshot independently confirms a successful **signup** (not yet login). In ZAP History, entry **56** is selected:

- HTTP method: `POST`
- Endpoint: `/identity/api/auth/signup`
- Request content type: `application/json`
- Response: `HTTP/1.1 200`, JSON
- Sanitized JSON response: `{"message":"User registered successfully! Please login.","status":200}`
- The browser shows the **Login** form, but no authenticated login request/response is shown.

**Interpretation:** The application accepted the test-account registration; authentication and token/session handling are **not yet verified**. The request pane visibly contains test-account credentials; **do not publish the raw screenshot or request body**. It is sufficient to document the method, endpoint, status and sanitized response text.

**Next step:** Submit the login form, then select the resulting POST login request in ZAP History. Inspect response status and authentication mechanism while redacting all passwords, bearer tokens, cookies and session values.

## Session 0 — authenticated dashboard and JWT verification (2026-11-16)

A new researcher-provided screenshot shows the crAPI **Dashboard** for researcher-owned account `TesterA` after login. ZAP History includes:
- Entries **57** and **58**: `POST /identity/api/auth/l...`, HTTP `401` (URL truncated in the visible History column; not yet independently inspected).
- Entry **59**: `POST /identity/api/auth/l...`, HTTP `200`; likely the successful login request, pending inspection of its full URL and response.
- Entry **64** (selected): `POST /identity/api/auth/verify`, HTTP `200`. A JWT was sent in a JSON request body. The response reports `{"message":"The token is a valid JWT token","status":200}`.
- Entries **65–66**: subsequent `GET` requests under `/identity/api/v2/...`, HTTP `200` (paths truncated in the screenshot).

**Validated:** dashboard access under TesterA and a server response affirming that the submitted JWT is valid. **Not established:** the exact shape and issuance of the login response, token expiry, or whether any access controls can be bypassed. Authentication success must not be confused with object-level authorization.

**Information handling:** the screenshot exposes an active-looking JWT in the ZAP request body. Never commit the screenshot, JWT, cookies or unredacted request captures to this public repo. Store these text-only, sanitized findings instead. Avoid copying or decoding the actual token using third-party sites.

**Next exercise:** select History row 59, inspect the full login request path and status in ZAP, and provide only a redacted screenshot if further review is needed. Then create User B and prepare baseline User A vs. User B object access for API1 (BOLA).

## Session 0 — successful login request confirmed (2026-11-16)

A researcher-provided screenshot displays ZAP History **ID 59** selected, with the full login HTTP transaction:

- Method: `POST`
- URL path: `/identity/api/auth/login` on the authorized `http://localhost:8888` crAPI lab
- Request content type: `application/json`
- Observed server response: `HTTP/1.1 200` and `Content-Type: application/json`
- The response JSON includes a field named `token` containing a JWT (the actual token value **is not recorded**).
- The user's browser displays the authenticated crAPI dashboard for researcher-owned User A / TesterA.

**Conclusion:** a valid test-account login was observed, and the API issued a JWT. This does **not** demonstrate object-level authorization, and no vulnerability is confirmed.

**Evidence handling:** the original screenshot reveals a test-only password and a potentially live JWT; it must not be added unredacted to this public repository or to portfolio posts. Do not store raw login payloads, cookies or JWTs in GitHub.

**Next milestone:** create a second researcher-owned account (User B) using a separate session or by logging out; capture a sanitized success summary, then identify a resource owned by User B and establish authorized baseline requests for API1:2023 BOLA.

## Session 0 — second test account registration confirmed (2026-11-16)

The screenshot supplied by the researcher shows ZAP History item **72** capturing User B / `TesterB` registration.

- `POST /identity/api/auth/signup`
- HTTP response: `200 OK`; `Content-Type: application/json`
- Sanitized response: `{"message":"User registered successfully! Please login.","status":200}`
- Browser displays the login screen following registration; **successful login by User B has not yet been observed**.
- Two distinct researcher-owned lab accounts (TesterA and TesterB) are now reported as registered. Test account A's login was independently observed in an earlier screenshot.

**Status:** registration setup achieved. This is not a confirmed vulnerability finding.

**Evidence security:** Screenshot contains lab credentials and test-user details; do **not** commit the original screenshot or a raw request to the public repo. The relevant HTTP metadata and sanitized response are sufficient.

**Next step:** Log in to User B, verify a `POST /identity/api/auth/login` HTTP `200` response and dashboard identity, then identify one user-owned resource per account for an API1 BOLA baseline test.

## Session 0 — second account authenticated (2026-11-16)

**Source:** researcher-provided screenshot of ZAP + crAPI dashboard.

- The browser shows authenticated dashboard for `TesterB`.
- ZAP History entry 73: `POST` request to an `/identity/api/auth/l...` path, HTTP `200`. Given earlier verification, this is consistent with successful User B login, though the full path is truncated in the screenshot.
- ZAP History entry 75 (selected): `POST /identity/api/auth/verify`, HTTP `200`. The JSON response reports the JWT is valid.
- Other authenticated user/vehicle GET requests are visible in ZAP history.
- Both TesterA and TesterB have now been independently observed accessing their own dashboards.
- The selected request body contains a JWT. Do not publish the raw screenshot or token.

**Assessment status:** preparation for API1:2023 BOLA is in progress; no BOLA result has been tested or confirmed yet.

**Next step:** connect a lab vehicle to TesterB using its own VIN and PIN from the local MailHog inbox, then capture a legitimate vehicle-related API request as the baseline. Repeat for TesterA before comparing object-level access.
