# 03 — API Security Top 10 Assessment Tracker

This tracker describes **planned coverage**, not confirmed weaknesses.

| ID | Category | Discovery status | Test status | Verified result | Evidence |
|---|---|---|---|---|---|
| API1 | Broken Object Level Authorization | Completed: authorized B baseline + cross-account GET + researcher-verified repeat | **Confirmed in lab (researcher-verified)** | TesterA token requested TesterB location; HTTP 200 + TesterB private fields; first attempt screenshot, retest reported | [Lab journal](04-api1-bola-lab.md), [Confirmed finding](../findings/API01-BOLA.md) |
| API2 | Broken Authentication | Forgot-password, OTP delivery, invalid/valid OTP, new/old password login controls captured | Testing in progress | New password login 200; old password rejected 401 with null token; no auth bypass confirmed; OTP replay/expiry/throttling pending | [API2 lab journal](05-api2-broken-authentication-lab.md) |
| API3 | Broken Object Property Level Authorization | Pending | Not tested | — | — |
| API4 | Unrestricted Resource Consumption | Pending | Not tested | — | — |
| API5 | Broken Function Level Authorization | Pending | Not tested | — | — |
| API6 | Unrestricted Access to Sensitive Business Flows | Pending | Not tested | — | — |
| API7 | Server Side Request Forgery | Pending | Not tested | — | — |
| API8 | Security Misconfiguration | Pending | Not tested | — | — |
| API9 | Improper Inventory Management | Pending | Not tested | — | — |
| API10 | Unsafe Consumption of APIs | Pending | Not tested | — | — |

## Validation standards

- **Confirmed:** reproducible behavior with sanitized request/response evidence supporting the security impact.
- **Not reproduced:** completed attempted test with no evidence of the suspected issue; document test limitations.
- **Not applicable:** no applicable interface/flow found within the authorized scope and assessed version; justify.
- **Not tested:** research or testing incomplete.

## Next milestone
Session 0: verify proxy interception and capture the first authenticated API request. Then begin API1 with User A and User B.
