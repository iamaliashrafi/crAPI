# Python-assisted crAPI testing (local authorized lab)

## Scope

All scripts here target only the researcher's own self-hosted OWASP crAPI instance at `http://localhost:8888`. OWASP ZAP's local intercepting proxy is expected on `http://127.0.0.1:8081`. Never use these exercises against unauthorized environments.

## Script 01 — API3 profile baseline

`scripts/api03_profile_baseline.py` performs the following low-risk workflow:

1. Prompts interactively for research-owned TesterA account email and password (password input is hidden).
2. Signs in **directly** to the local crAPI login endpoint. The login password does not traverse ZAP.
3. Keeps the returned JWT in Python memory only; does not print, commit or save the token.
4. Sends **one authenticated read-only GET** to `/identity/api/v2/user/dashboard` **through ZAP**, so the request appears in ZAP History.
5. Prints JSON **property names and types only**; no response values.
6. Optionally compares the just-changed test phone number, entered through a hidden prompt, against any phone-like JSON field without displaying the number.
7. If no phone property is in Dashboard JSON, reports **NOT AVAILABLE** rather than guessing. Verify the change on the refreshed `/my-profile` page instead.

**The script does not test Mass Assignment yet.** This is an automated baseline to support later property-level testing; do not claim a vulnerability merely because a field is printed.

## Setup and run on macOS

Clone the repository once if it is not on your machine:

```bash
git clone https://github.com/iamaliashrafi/crAPI.git
cd crAPI
```

If it already exists locally, enter the repository and run `git pull`.

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r scripts/requirements.txt
python scripts/api03_profile_baseline.py
```

Before running, make sure crAPI is available in the browser at `http://localhost:8888` and that ZAP is running with its **Main Proxy on port 8081**. If your ZAP proxy port changed, update `ZAP_PROXY` in the script.

At the prompts: enter the **TesterA** email, its current password, and optionally the **new test phone number** from the completed OTP verification. Do not share these inputs. Inspect the terminal result and the newly captured GET in ZAP History. Share only the HTTP status, JSON field **names**, and comparison result.

## Security and repository hygiene

- Never commit or paste real passwords, OTPs, JWTs, session cookies, email addresses, phone numbers, unsanitized ZAP captures, or screenshots containing these values.
- ZAP still captures the Dashboard GET **Bearer token** in its History: keep ZAP Session files private.
- Python virtual environment `.venv/` is local working data and must not be committed.
- Never hard-code credentials or expand the host scope without explicit authorization.
- A failed login or unavailable Docker/ZAP instance is an environment/configuration error, not a discovered vulnerability.

## Next development step

After observing the fresh dashboard field names and confirming TesterA's test phone was saved, design a **single controlled Mass Assignment field-allowlisting test** against the researcher's own disposable account. First capture the expected request body and define an independent, reversible state check.
