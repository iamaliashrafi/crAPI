# API1:2023 — Broken Object Level Authorization (BOLA)

**Stage:** preparation / baseline collection. **No vulnerability confirmed.**

## Learning objective

Authentication proves a subject's identity. Object-level authorization determines if that authenticated subject may access a particular resource. A BOLA assessment compares access to the **same object** under two different legitimate user identities, then checks whether unauthorized access is permitted.

## Authorized test data

- User A: researcher-owned `TesterA`
- User B: researcher-owned `TesterB`
- Target: self-hosted `http://localhost:8888` crAPI laboratory only
- Objects: separately assigned lab vehicles (once added)

## Read-only test design

1. Verify each account's registration and login; completed for TesterA and TesterB (see environment log).
2. Add a different lab vehicle under each account by following crAPI's normal Add Vehicle flow. Obtain the VIN and PIN only from the local MailHog test inbox, not from a real mailbox.
3. Under User B, capture a legitimate vehicle info/location request in ZAP and record only sanitized method, path and status.
4. Under User A, capture the corresponding authorized baseline to User A's own vehicle.
5. When both baselines are ready, make a controlled read-only cross-account request for **User B's vehicle** while authenticated as User A, keeping the authenticating session/token as User A; inspect result. Do not modify data.
6. If the response exposes B's nonpublic vehicle details, reproduce and document it as a confirmed candidate BOLA finding. If access is denied, record that response and any test limitations.

## Safe evidence policy

Store only redacted request/response examples. Do not commit raw JWTs, passwords, cookies, account email addresses, VINs, mailbox messages, or exact GPS coordinates to this repository. Use identifiers like `<USER_B_VEHICLE_UUID>` in public reports.

## Lab milestone — User B vehicle visible (2026-11-16)

**Observed in researcher-supplied screenshot:** the authenticated `TesterB` dashboard displays a lab vehicle, Mercedes-Benz **GLA Class**, model year **2026**, and a map/location marker. MailHog is also open in a separate tab. This supports the conclusion that User B's vehicle is linked and displayed; the exact VIN, owner-specific identifier, and coordinate values are deliberately not recorded here.

In ZAP, the selected request is `GET /identity/api/v2/vehicle/vehicles` with `HTTP 200` and response body `[]`. The timestamp/order of this request relative to vehicle linking is not proven, so this **does not yet establish** that it is the request providing the currently visible vehicle details. Reproduce a fresh authorized vehicle-related request first.

**Next controlled step (read-only baseline):** filter ZAP History to the local application using URL include regex `^http://localhost:8888/.*`; use the application's **Refresh Location** control if present, or refresh the dashboard, then identify the fresh vehicle-specific request. The upstream crAPI lab guide documents a location endpoint shaped like `/identity/api/v2/vehicle/<vehicleid>/location`, but the exact path and ID must be observed on this local deployment. Document only the endpoint pattern, response code and sanitized body; keep authorization tokens, full vehicle IDs and GPS coordinates private.

**Status:** User B vehicle shown; User A vehicle/authorized baseline still pending; **no unauthorized cross-account request or BOLA result yet**.

## References

- [OWASP API1:2023 — BOLA](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/)
- [OWASP crAPI challenges](https://github.com/OWASP/crAPI/blob/develop/docs/challenges.md)
- [OWASP crAPI lab guide (vehicle setup)](https://github.com/OWASP/crAPI/blob/develop/docs/challengeSolutions.md)

## Baseline evidence B1 — authenticated vehicle list (2026-11-16)

**Source:** screenshot of the researcher's own local ZAP session. ZAP History entry **181** is selected.

- Request: `GET /identity/api/v2/vehicle/vehicles HTTP/1.1` on `http://localhost:8888`.
- Authentication: an `Authorization: Bearer <REDACTED>` header is visible. The surrounding session indicates User B (`TesterB`), but the exact JWT identity was not independently decoded or validated.
- Response: `HTTP/1.1 200 OK` with `application/json`.
- Response body: JSON array containing **one** vehicle object with keys resembling `id`, `uuid`, `pincode`, `vin`, `year`, `status`, `previousOwners`, `model`, `vehiclecompany`, `vehicle_img`, `vehiclelocation`, and `owner`. The displayed record has `status: "INACTIVE"` and `owner: null`.
- One lab Mercedes-Benz GLA Class (2026) is visible in prior screenshots.
- **Sanitized interpretation:** User B's session can fetch a populated vehicle list; this does **not** demonstrate unauthorized access.
- **Important:** the raw screenshot reveals an active-looking bearer token, session material, VIN, PIN, UUID and exact vehicle coordinates. It must NOT be uploaded as-is, embedded in README files, or copied into public reports. None of those values have been saved here.
- **Limitations:** this endpoint lists vehicles, but does not alone prove access to a specific object by its ID. No `GET /identity/api/v2/vehicle/<ID>/location` response has yet been observed. The earlier `[]` response has been superseded by a newly observed single-record response, without claiming when the vehicle was attached.

**Next action:** find a vehicle-specific GET request on the lab origin in ZAP History; if not present, refresh the vehicle dashboard and inspect new traffic. Capture the legitimate User B endpoint and response as a sanitized *object-level* baseline. Afterwards obtain User A's baseline and perform a controlled, read-only comparison.

**Current finding status:** API1 BOLA — **Not tested (object-level cross-account access)**.

## Baseline exploration B2 — ZAP Sites tree inspection (2026-11-16)

**Source:** researcher-provided ZAP screenshot showing the expanded Sites tree for the authorized `http://localhost:8888` application.

Under `identity → api → v2 → vehicle`, only two endpoint entries are currently visible:
- `POST add_vehicle({vin,pincode})`
- `GET vehicles`

The latter is selected and its response contains a single User B lab vehicle, consistent with baseline B1. **No per-vehicle `GET /identity/api/v2/vehicle/<vehicleid>/location` endpoint is shown in the visited tree yet.** Absence from the Sites tree does not prove that this endpoint does not exist: the tree reflects requests ZAP has observed. This screenshot also shows `Filter: OFF` in the History tab and unrelated Google Maps/Fonts origins; these are out of assessment scope.

**Official crAPI guide:** clicking **Refresh Location** on the Dashboard is documented to initiate `/identity/api/v2/vehicle/<vehicleid>/location`. Guide: https://github.com/OWASP/crAPI/blob/develop/docs/challengeSolutions.md . This is a documented expected behavior, **not yet locally observed**.

**Next step:** while logged in as User B, use the application's Refresh Location function (scroll around the vehicle location UI if needed), then locate the new GET in ZAP History. If the control is missing in this deployment, use ZAP Requester to construct an authorized read-only baseline against **User B's own vehicle**, retaining User B's existing authenticated session and avoiding all third-party domains. Do not yet test cross-user access. Redact JWTs, UUIDs, PINs, VINs and precise location data from any published evidence.

**Finding status:** no cross-account request or BOLA finding confirmed.

## Baseline evidence B3 — vehicle-specific location (2026-11-16)

**Researcher-provided ZAP screenshot:** History item **188** selected. This is the first locally verified vehicle-specific read-only request.

- **Method/path:** `GET /identity/api/v2/vehicle/<USER_B_VEHICLE_UUID>/location`.
- **Host:** `localhost:8888` (authorized local crAPI lab).
- **Authentication:** `Authorization: Bearer <USER_B_JWT_REDACTED>` is visible; the surrounding test context is TesterB.
- **Response:** `HTTP/1.1 200 OK`, `Content-Type: application/json`.
- **Sanitized shape:** `{"carId":"<USER_B_VEHICLE_UUID>","vehicleLocation":{"id":<LOCATION_RECORD_ID>,"latitude":"<REDACTED>","longitude":"<REDACTED>"},"fullName":"TesterB","email":"<REDACTED>"}`.
- **Interpretation:** an authenticated User B request returns its lab vehicle location and related account details. This is a valid authorized baseline, not evidence of unauthorized cross-account access.
- **Sensitive-data handling:** the screenshot includes a full JWT, the vehicle UUID, latitude/longitude, an email, and a session cookie. The original screenshot must **not** be posted to this public repository. We store only substituted placeholder fields above.
- **Next test:** keep this User B target URL unaltered, authenticate as TesterA, then resend a **GET** in ZAP Requester using **only TesterA's valid Authorization header**, not TesterB's. Compare the observed result with the expected access denial or other explicitly permitted behavior. Preserve read-only method and local target; no mass scanning. Do not report BOLA until unauthorized data disclosure is confirmed and reproduced.
- **Note:** User A does not strictly require a car to test whether its authenticated identity can access B's car, though separate vehicles can enrich later bidirectional testing.

**Finding status:** User B location baseline confirmed; cross-account authorization test pending.

## BOLA test preparation B4 — copied User B location request into ZAP Requester (2026-11-16)

The researcher supplied a new screenshot of ZAP's Requester tab showing a copied `GET /identity/api/v2/vehicle/<USER_B_VEHICLE_UUID>/location` request. The request currently carries User B's `Authorization: Bearer <REDACTED>` header and, in the response panel, the previously captured HTTP `200 OK` with User B location/account fields. The Requester footer indicates `Time: 0 ms` and `Body Length: 0` for the current editor operation, so there is **no evidence yet of a newly submitted modified request**.

**Next step:** Keep the Requester tab with the User B vehicle URL. Authenticate as User A in the browser; in ZAP History locate a recent User A authenticated dashboard or vehicle request, copy only its Bearer token locally and substitute it for User B's Bearer token in Requester. To isolate bearer-based authorization, remove the copied `chat_session` Cookie header if present. Keep method, host and User B vehicle path unchanged. Submit only one read-only GET to the local lab. Record response code and redacted response fields; an HTTP 200 is not sufficient on its own to claim BOLA unless User B's protected data is actually disclosed. No secrets or raw screenshots are published.

## Cross-account experiment B5 — potential BOLA reproduced once (2026-11-16)

**Researcher-supplied screenshot:** ZAP Requester now shows an executed manual request, History **199**:
- Source: `Manual`
- Method: `GET`
- URL: `http://localhost:8888/identity/api/v2/vehicle/<USER_B_VEHICLE_UUID>/location`
- Response: `HTTP/1.1 200 OK`; JSON response body **177 bytes**; Requester reports **30 ms** elapsed
- Sanitized response contains `"carId":"<USER_B_VEHICLE_UUID>"`, `"vehicleLocation": {"latitude":"<REDACTED>","longitude":"<REDACTED>"}`, `"fullName":"TesterB"`, and `"email":"<REDACTED>"`.
- The same screenshot also shows prior successful authentication sequence, History entries 193 (login), 195 (JWT verify), 196 (user dashboard), and 197 (vehicle list with a 2-byte empty response), consistent with a session switch from TesterB to TesterA.
- In the preceding interaction, the researcher was instructed to replace User B's bearer token in the Requester with User A's bearer token, remove the copied `chat_session` cookie, and keep User B's vehicle URL unchanged.

**Security interpretation:** If History 199 was sent exclusively with User A's authentication context and without User B's remaining credentials, returning User B's private location, name and email represents **API1:2023 BOLA**. It is presently a **strong candidate / confirmation pending**, since a static screenshot cannot independently establish token ownership, absence of all B session material, or a second independent reproduction. Do **not** label this finding definitively confirmed, assign a CVSS score, or claim remediation has occurred.

**Next decisive verification:** In Requester, verify that the target path still belongs to B, and that the only authentication credential being sent is a valid token from TesterA. Remove the `Cookie:` header if it is present. Reissue one read-only GET against the same local lab endpoint. Compare response body and document outcome with all sensitive values replaced. Optional stronger control: verify User A token on `GET /identity/api/v2/user/dashboard` before the B request, without disclosing token values.

**Evidence disclosure warning:** the screenshot shows a JWT and precise location information in plaintext. Do not upload this raw screenshot or copy secrets into this public repository.
