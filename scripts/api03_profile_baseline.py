#!/usr/bin/env python3
"""Read-only API3 profile baseline for the research-owned local OWASP crAPI lab.

Login goes directly to local crAPI. Only the authenticated Dashboard GET goes
through OWASP ZAP, so the password is not sent through the intercepting proxy.
No tokens, passwords, phone numbers or response data are saved or printed.
"""
from __future__ import annotations

import getpass
import re
import sys
from typing import Any, Iterator

import requests

BASE_URL = "http://localhost:8888"
ZAP_PROXY = "http://127.0.0.1:8081"
TIMEOUT = (3, 10)  # connect and read timeout, in seconds


def shape_paths(value: Any, path: str = "$", depth: int = 0) -> Iterator[str]:
    """Return structural property paths without printing any field values."""
    if depth > 5:
        return
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            yield f"{child_path}: {type(child).__name__}"
            if isinstance(child, (dict, list)):
                yield from shape_paths(child, child_path, depth + 1)
    elif isinstance(value, list) and value:
        yield from shape_paths(value[0], f"{path}[0]", depth + 1)


def phone_like_values(value: Any) -> Iterator[str]:
    """Find values of phone-like fields for local equality testing only."""
    if isinstance(value, dict):
        for key, child in value.items():
            key_l = key.lower()
            if (re.search(r"phone|mobile|telephone", key_l) or key_l in {"tel", "number"}) and isinstance(child, (str, int)):
                yield str(child)
            if isinstance(child, (dict, list)):
                yield from phone_like_values(child)
    elif isinstance(value, list):
        for item in value:
            yield from phone_like_values(item)


def main() -> int:
    print("crAPI API3 — read-only profile baseline (local lab only)")
    print(f"Target: {BASE_URL} | ZAP proxy: {ZAP_PROXY}")
    email = input("TesterA test email: ").strip()
    if not email:
        print("Email is required.", file=sys.stderr)
        return 2
    password = getpass.getpass("TesterA password (hidden): ")
    expected_phone = getpass.getpass(
        "Expected new test phone (hidden; press Enter to skip comparison): "
    ).strip()

    # Authenticate DIRECTLY to crAPI. Do not put the password in ZAP history.
    with requests.Session() as direct:
        direct.trust_env = False
        try:
            login = direct.post(
                f"{BASE_URL}/identity/api/auth/login",
                json={"email": email, "password": password},
                timeout=TIMEOUT,
            )
        except requests.RequestException:
            print("Could not reach the local crAPI login endpoint.", file=sys.stderr)
            return 1
        if login.status_code != 200:
            print(f"Login failed (HTTP {login.status_code}). No data saved.")
            return 1
        try:
            token = login.json()["token"]
        except (ValueError, KeyError, TypeError):
            print("Login returned no readable JWT; check local crAPI auth.", file=sys.stderr)
            return 1

    print("Login succeeded (JWT held in memory only).")

    # Send only one authenticated read-only GET through the locally running ZAP.
    with requests.Session() as via_zap:
        via_zap.trust_env = False
        via_zap.proxies.update({"http": ZAP_PROXY, "https": ZAP_PROXY})
        try:
            response = via_zap.get(
                f"{BASE_URL}/identity/api/v2/user/dashboard",
                headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
                timeout=TIMEOUT,
            )
        except requests.RequestException:
            print("Dashboard GET failed. Check ZAP is listening on 127.0.0.1:8081.", file=sys.stderr)
            return 1

    print(f"Dashboard GET: HTTP {response.status_code}")
    if response.status_code != 200:
        print("No response body printed. Check the ZAP History entry and reauthenticate if necessary.")
        return 1
    try:
        data = response.json()
    except ValueError:
        print("Dashboard returned non-JSON data; no content printed.")
        return 1

    print("\nJSON field paths / types (VALUES REDACTED):")
    for line in shape_paths(data):
        print("  " + line)

    if expected_phone:
        candidates = list(phone_like_values(data))
        if not candidates:
            print("\nPhone comparison: NOT AVAILABLE — no phone-like JSON field found.")
            print("Verify the new phone in /my-profile instead.")
        elif expected_phone in candidates:
            print("\nPhone comparison: MATCH — requested test number appears in dashboard JSON.")
        else:
            print("\nPhone comparison: NO MATCH — review a fresh /my-profile page before concluding.")
    else:
        print("\nPhone comparison: skipped (no number entered).")

    print("\nDone. Exactly one read-only dashboard request was sent through ZAP.")
    print("Keep the ZAP session private: its History can include a bearer JWT.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
