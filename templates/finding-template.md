# Finding [ID] — [Concise title]

**OWASP API category:** APIx:2023 — [Name]  
**Status:** Not tested / Confirmed / Not reproduced / Not applicable  
**Severity:** Pending (assign only with supporting evidence)  
**Environment and date:** [crAPI build, date, browser, ZAP version]  
**Endpoints:** [Methods and paths only; do not expose credentials]

## Executive summary
[One paragraph explaining what was tested and the verified result.]

## Background and expected security behavior
[Describe legitimate flow and server-side rule.]

## Preconditions
[Owned test accounts, necessary data, roles and any special lab setup.]

## Reproduction procedure
1. [Establish authorized baseline.]
2. [Perform a narrowly scoped controlled test.]
3. [Compare request and server response.]
4. [Repeat to validate.]

## Evidence
| Artifact | Purpose | Redacted? |
|---|---|---|
| [link] | [What it shows] | Yes |

Use sanitized HTTP samples with `<REDACTED>` placeholders only; do not commit raw session exports.

## Actual vs expected outcome
**Expected:** [Secure result]  
**Observed:** [Verified result, including response status and relevant non-sensitive fields]

## Security impact
[Explain affected asset, attacker prerequisites, and plausible consequence. Distinguish observed facts from hypotheses.]

## Root cause and remediation
[Explain likely root cause cautiously, then recommend specific server-side controls and regression tests.]

## Retest / validation status
[What was retested and when, and whether remediation was deployed.]

## References
- [OWASP API Security Top 10 — 2023](https://api-security.owasp.org/editions/2023/en/0x11-t10/)
