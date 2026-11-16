# 01 — Scope and Methodology

## Authorization and scope

**Authorized target:** the researcher's own locally hosted instance of OWASP crAPI at `http://localhost:8888`. Browser traffic to this host is in scope. External websites, unrelated local services, third-party systems, and other users' accounts are out of scope.

This work is an **educational lab assessment**, not a customer pentest. Do not target public production applications using the steps documented here without written authorization.

## Objectives
- Study all ten OWASP API Security Top 10 (2023) categories.
- Discover and document relevant API endpoints and authentication mechanisms.
- Apply repeatable, controlled manual tests with OWASP ZAP.
- Classify each category by verified outcome, not presumptions.
- Explain impact and remediations from a defender's perspective.

## Repeatable workflow
1. **Learn:** Explain the risk, prerequisites, and expected safe behavior.
2. **Map:** Identify API endpoints from normal application use; record method, path, parameters, authentication and response shape without secrets.
3. **Baseline:** Capture a legitimate request/response.
4. **Test:** Make the smallest authorized change necessary to probe the control.
5. **Validate:** Reproduce, compare intended vs observed behavior, rule out false positives.
6. **Rate:** Explain impact, conditions, and confidence; use CVSS only with explicit rationale if used.
7. **Remediate:** Recommend server-side authorization, input validation, safe defaults, observability, etc., as relevant.
8. **Document:** Save redacted evidence and a report using the template.

## Rules of engagement
- Create and use two test accounts owned by the researcher, e.g., User A and User B.
- Use controlled test data only.
- Never perform destructive operations on external assets.
- Avoid aggressive fuzzing, denial-of-service or resource-exhaustion tests; model/API4 checks should use conservative thresholds and limited samples.
- Avoid scanning third-party origins present in ZAP Sites.
- Record ZAP version, crAPI deployment/commit (if available), dates and configuration before asserting reproducibility.
- Treat scanner alerts as hypotheses pending manual verification.

## Findings status
Use `Confirmed`, `Not reproduced`, `Not applicable`, or `Not tested`. If a test fails to confirm a risk, document the negative result and limitations.

## Publishing disclosure
All work is performed on intentionally vulnerable crAPI. Do not present this as an actual client engagement. Never publish tokens, passwords, cookies, session IDs, personal identifiers, or raw unredacted traffic.
