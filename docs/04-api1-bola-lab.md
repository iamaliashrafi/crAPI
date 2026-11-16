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
