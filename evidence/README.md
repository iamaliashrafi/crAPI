# Evidence Handling

This directory is reserved for **sanitized** screenshots, request/response examples and diagrams generated during hands-on assessment.

Before uploading:
- Redact bearer/JWT tokens, authorization headers, cookies, API keys, passwords, account emails, addresses, phone numbers, identifiers linked to personal data and other secrets.
- Remove unnecessary user data and raw payloads.
- Capture only your own deliberately created lab accounts and in-scope local crAPI traffic.
- Include date, target path (not secret query parameters), test ID and a short caption.
- Ensure that redaction is permanent (not just a visual layer over underlying readable text).

Never commit complete ZAP sessions, browser profiles, unredacted HAR files, database dumps, or .env files.
