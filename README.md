# OWASP API Security Top 10 (2023) — crAPI Assessment

A structured, hands-on API security assessment of the intentionally vulnerable [OWASP crAPI](https://github.com/OWASP/crAPI) application using **OWASP ZAP**.

**Project status:** In progress — API1 BOLA and API3 Excessive Data Exposure confirmed in the authorized local lab; API2 controls tested (no confirmed bypass); API4–API10 pending.  
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
| API1 | Broken Object Level Authorization (BOLA) | **Confirmed in local lab (researcher-verified)** — [finding](findings/API01-BOLA.md) |
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

The `findings/` folder contains only evidence-based assessments. API1 includes an initial screenshot-observed response and researcher-reported verification of a second request; no redacted repeat screenshot has been uploaded. Remaining API categories are not yet tested.

## Methodology

**Understand intended functionality → Capture normal API traffic → Define expected authorization/security behavior → Test a controlled deviation → Reproduce and validate → Assess impact → Recommend fixes → Publish sanitized evidence.**

Manual evidence takes precedence over unverified scanner alerts. Use test accounts owned by the researcher and stay within the local lab and controlled dependencies. Avoid production targets and disruptive load testing.

## Progress update (2026-11-16)

ZAP intercepts local crAPI API traffic. Two researcher-owned test accounts (`TesterA`, `TesterB`) were created and authenticated, and a lab vehicle was attached to TesterB. A legitimate vehicle-location request was recorded, followed by a cross-account request using TesterA's token for TesterB's vehicle. The initial HTTP `200 OK` and TesterB data were observed in a ZAP screenshot; the researcher reports independently confirming the token/cookie isolation and reproducing the disclosure. This is documented as an API1 BOLA finding in the **intentionally vulnerable lab**. See [detailed evidence](findings/API01-BOLA.md) and [lab journal](docs/04-api1-bola-lab.md).


## API3 discovery update (2026-11-16)

An authorized read-only check of the Community Forum post-feed endpoint returned other authors' `email` and `vehicleid` properties to both TesterB and TesterA sessions, although those values are not displayed in the Forum UI. This local lab result is documented in the [API3 finding](findings/API03-EXCESSIVE-DATA-EXPOSURE.md) and [API3 journal](docs/06-api3-bopla-lab.md). Severity remains provisional; no downstream vehicle exploit chain was performed using the identifiers from these responses.

**API2 note:** Controlled invalid/valid OTP recovery and an attempt-limit response were observed, but JWT invalidation remains unverified. See the [API2 journal](docs/05-api2-broken-authentication-lab.md).

## Python + ZAP automation (from 2026-11-17)

Subsequent lab exercises use small, reviewable Python scripts for reproducible authenticated requests and OWASP ZAP as an intercepting evidence/inspection proxy. The first read-only script, [API3 Profile Baseline](scripts/api03_profile_baseline.py), logs in to the **research-owned local lab**, makes one authenticated Dashboard GET through ZAP, and prints **only JSON field names/types and an optional local phone-number match result**. It does not itself establish Mass Assignment or modify the account. See [scripts/README.md](scripts/README.md) for macOS setup, execution and safeguards.

## References

- [OWASP API Security Top 10 (2023)](https://api-security.owasp.org/editions/2023/en/0x11-t10/)
- [OWASP crAPI project](https://owasp.org/projects/crapi)
- [ZAP Getting Started](https://www.zaproxy.org/getting-started/)
- [ZAP Quick Start / Manual Explore](https://www.zaproxy.org/docs/desktop/addons/quick-start/)

## Sensitive-data policy

Never commit real passwords, active tokens, cookies, personal information, database dumps, ZAP session files, or unsanitized HTTP captures. Redact all session material and personal identifiers from screenshots, requests, and exported reports before publication.
