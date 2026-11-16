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

## Important current limitation

The dashboard currently shows **No Vehicles Found** for the newly created account. No vehicle object UUID or user-owned resource baseline has been captured yet. An HTTP `200` from a login or JWT verification endpoint does **not** constitute a BOLA finding.

## References

- [OWASP API1:2023 — BOLA](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/)
- [OWASP crAPI challenges](https://github.com/OWASP/crAPI/blob/develop/docs/challenges.md)
- [OWASP crAPI lab guide (vehicle setup)](https://github.com/OWASP/crAPI/blob/develop/docs/challengeSolutions.md)
