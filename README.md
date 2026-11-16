# OWASP API Security Top 10 (2023) — crAPI Assessment

A structured, hands-on API security assessment of the intentionally vulnerable [OWASP crAPI](https://github.com/OWASP/crAPI) application using **OWASP ZAP**.

**Project status:** In progress — laboratory setup / baseline exploration.  
**Assessment environment:** Local self-hosted crAPI instance (`http://localhost:8888`).  
**Assessment date started:** 2026-11-16.  
**Tooling:** OWASP ZAP, browser, and manual HTTP request/response review.

> **Portfolio disclosure:** This is an educational security-assessment project against a deliberately vulnerable local lab, **not** a real client engagement or a production penetration test. Findings are not confirmed until independently reproduced and documented. This repository is not an official OWASP or ZAP project.

## Goals

1. Learn the OWASP API Security Top 10 (2023) using practical, authorized tests.
2. Practice ZAP interception, API discovery, authentication, manual testing, and reporting.
3. Produce reproducible technical findings with evidence, impact analysis, and remediation guidance.
4. Publish a transparent portfolio case study suitable for GitHub, Upwork, and LinkedIn.

## Assessment coverage

| ID | OWASP API Security risk (2023) | Status |
|---|---|---|
| API1 | Broken Object Level Authorization (BOLA) | Not started |
| API2 | Broken Authentication | Not started |
| API3 | Broken Object Property Level Authorization | Not started |
| API4 | Unrestricted Resource Consumption | Not started |
| API5 | Broken Function Level Authorization | Not started |
| API6 | Unrestricted Access to Sensitive Business Flows | Not started |
| API7 | Server Side Request Forgery (SSRF) | Not started |
| API8 | Security Misconfiguration | Not started |
| API9 | Improper Inventory Management | Not started |
| API10 | Unsafe Consumption of APIs | Not started |

These are **assessment categories**, not a claim that ten exploitable vulnerabilities have been found in this exact deployment. Record each outcome as *Confirmed / Not reproduced / Not applicable / Not tested*, with evidence and test limitations.

## Repository map

- [Scope, ethics, and methodology](docs/01-scope-and-methodology.md)
- [Environment baseline and ZAP setup](docs/02-environment-and-setup.md)
- [Top 10 assessment tracker](docs/03-assessment-tracker.md)
- [Finding report template](templates/finding-template.md)
- [Evidence handling policy](evidence/README.md)
- [Reports and publication notes](reports/README.md)

The `findings/` folder will be populated **only as each category is tested and documented**, rather than pre-writing hypothetical results.

## Methodology

**Understand intended functionality → Capture normal API traffic → Define expected authorization/security behavior → Test a controlled deviation → Reproduce and validate → Assess impact → Recommend fixes → Publish sanitized evidence.**

Manual evidence takes precedence over unverified scanner alerts. Use test accounts owned by the researcher and stay within the local lab and controlled dependencies. Avoid production targets and disruptive load testing.

## Baseline observation (2026-11-16)

A user-provided screenshot shows crAPI displaying `http://localhost:8888/login` and ZAP History recording `GET http://localhost:8888/login` with an HTTP `200 OK` response. ZAP's status bar appears to show a proxy on `localhost:8081`. This **does not yet prove** that authenticated API requests are being captured. Next action: use **Quick Start → Manual Explore → Launch Browser**, and inspect the login API request and response.

## References

- [OWASP API Security Top 10 (2023)](https://api-security.owasp.org/editions/2023/en/0x11-t10/)
- [OWASP crAPI project](https://owasp.org/projects/crapi)
- [ZAP Getting Started](https://www.zaproxy.org/getting-started/)
- [ZAP Quick Start / Manual Explore](https://www.zaproxy.org/docs/desktop/addons/quick-start/)

## Sensitive-data policy

Never commit real passwords, active tokens, cookies, personal information, database dumps, ZAP session files, or unsanitized HTTP captures. Redact all session material and personal identifiers from screenshots, requests, and exported reports before publication.
