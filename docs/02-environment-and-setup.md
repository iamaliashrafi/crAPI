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
