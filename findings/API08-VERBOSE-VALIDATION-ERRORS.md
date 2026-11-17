# API08 — Verbose Java/Spring Validation Internals Exposed to API Clients

**Finding ID:** API08-MISCONFIG-001  
**Category:** OWASP API8:2023 — Security Misconfiguration  
**Target:** Researcher-owned local OWASP crAPI instance, `http://localhost:8888`  
**Status:** **Observed and confirmed in local lab** from a ZAP History request/response screenshot  
**Provisional severity:** **Low** (qualitative; may be informational under some reporting schemes)  
**Assessment date:** 2026-11-17  
**Tool:** OWASP ZAP History / Request & Response  
**Remediation:** Not performed or retested

## Summary

When a client supplies invalid-length telephone fields to the identity service, the application returns an HTTP 400 JSON error containing more than a user-oriented validation explanation. Its `details` field exposes the **Java/Spring framework class names, binding-result structure, form object name, field-validation descriptors, and field size rules**. This is avoidable internal implementation disclosure, not by itself a high-impact exploit.

## Reproduction — sanitized

One researcher-owned authenticated test account made the following manual request in ZAP, History **375**:

```http
POST /identity/api/v2/user/change-phone-number HTTP/1.1
Host: localhost:8888
Authorization: Bearer <REDACTED>
Content-Type: application/json

{
  "old_number": "<INVALID_TEST_VALUE>",
  "new_number": "<INVALID_TEST_VALUE>",
  "name": "MassAssignProbeA"
}
```

The request failed as expected with **HTTP 400 Bad Request**. The returned JSON included:

```json
{
  "message": "Validation failed",
  "details": "org.springframework.validation.BeanPropertyBindingResult: 2 errors; Field error in object 'changePhoneForm' on field 'new_number': ...; Field error in object 'changePhoneForm' on field 'old_number': ..."
}
```

The displayed error details also included validation codes and the size requirement **between 0 and 15** for both phone-related fields. The example above intentionally omits rejected values, JWTs, cookies and verbose raw backend text.

## Impact and limits

A caller can learn the application framework (Spring validation) and form/field implementation details. This may help reconnaissance and target later attacks. The screenshot **does not establish any leaked passwords, access tokens in the response, filesystem paths, database credentials, stack-trace file names, or direct exploitation**.

This finding should not be conflated with the separate, inconclusive API3 Mass Assignment probe that originally triggered the 400 validation error.

## Remediation

1. Return a small, predictable, client-facing validation error (e.g. `HTTP 400` with field names and simple constraints).
2. Keep `BeanPropertyBindingResult`, package/class names, rejected object values and exception details in access-controlled server logs only.
3. Ensure production exception handlers consistently sanitize framework error details.
4. Add regression tests that malformed client inputs never expose internal class/package names or sensitive submitted values.

## Retest

Send one invalid-length value from an authorized test account. A correct implementation can return `HTTP 400` with a short field-level reason while suppressing internal framework details.

## Evidence provenance and privacy

The supplied screenshot clearly displays ZAP History ID **375**, `HTTP/1.1 400` and the `details` string with `org.springframework.validation.BeanPropertyBindingResult` and `changePhoneForm`. The request header contains a Bearer JWT and cookie and thus **must not be published unredacted**. The report contains sanitized paraphrase only.

## References

- [OWASP API8:2023 — Security Misconfiguration](https://api-security.owasp.org/editions/2023/en/0xa8-security-misconfiguration/)
- [API8 lab journal](../docs/11-api8-security-misconfiguration-lab.md)
