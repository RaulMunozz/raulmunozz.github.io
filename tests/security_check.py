#!/usr/bin/env python3
"""Dependency-free security checks for the static portfolio.

Run from the repository root with: python tests/security_check.py
Exit code 0 means every check passed.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
HTML_FILES = [ROOT / "index.html", ROOT / "portfolio" / "index.html"]
JS_FILE = ROOT / "script.js"
CSS_FILE = ROOT / "styles.css"
SVG_FILE = ROOT / "favicon.svg"

REQUIRED_CSP = [
    "default-src 'self'",
    "base-uri 'none'",
    "object-src 'none'",
    "script-src 'self'",
    "style-src 'self' https://fonts.googleapis.com",
    "font-src 'self' https://fonts.gstatic.com",
    "img-src 'self' data:",
    "connect-src 'self'",
    "form-action 'none'",
    "frame-src 'none'",
    "worker-src 'none'",
    "upgrade-insecure-requests",
]

DANGEROUS_PATTERNS = [
    r"\binnerHTML\b",
    r"\bouterHTML\b",
    r"\beval\s*\(",
    r"\bnew\s+Function\s*\(",
    r"\bdocument\.write\s*\(",
    r"javascript:",
    r"\son[a-z]+\s*=",
    r"<form\b",
    r"<input\b",
]

SECRET_PATTERNS = [
    r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----",
    r"\bghp_[A-Za-z0-9]{20,}\b",
    r"\bAKIA[0-9A-Z]{16}\b",
    r"\bAIza[0-9A-Za-z_-]{35}\b",
    r"(?i)\b(api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]{8,}['\"]",
]

failures = []


def check(condition, message):
    status = "PASS" if condition else "FAIL"
    print(f"{status}: {message}")
    if not condition:
        failures.append(message)


for path in HTML_FILES:
    text = path.read_text(encoding="utf-8")
    label = path.relative_to(ROOT).as_posix()

    match = re.search(
        r'<meta\s+http-equiv=["\']Content-Security-Policy["\']\s+content="([^"]+)"',
        text,
        re.I,
    )
    csp = match.group(1) if match else ""
    for directive in REQUIRED_CSP:
        check(directive in csp, f"{label}: CSP contains {directive}")

    check(
        'name="referrer" content="no-referrer"' in text,
        f"{label}: referrer policy is no-referrer",
    )

    external_ok = True
    for attrs in re.findall(r"<a\b([^>]*href=[\"']https://[^\"']+[\"'][^>]*)>", text, re.I):
        if "noopener" not in attrs or "noreferrer" not in attrs:
            external_ok = False
    check(external_ok, f"{label}: external links use noopener noreferrer")

    check(
        text.count('class="card-link"') == 6,
        f"{label}: six project cards preserved",
    )
    check(
        len(re.findall(r'<a class="card-link"[^>]+href="https://github.com/RaulMunozz/', text)) == 6,
        f"{label}: six GitHub code links preserved",
    )

    cv_href = "../CV.pdf" if label == "portfolio/index.html" else "CV.pdf"
    check(f'href="{cv_href}"' in text, f"{label}: CV download link present")
    check('id="about"' in text, f"{label}: about section present")

    for pattern in DANGEROUS_PATTERNS:
        check(not re.search(pattern, text, re.I), f"{label}: no {pattern}")

check((ROOT / "CV.pdf").is_file(), "CV.pdf: downloadable CV is present")

js = JS_FILE.read_text(encoding="utf-8")
check("textContent" in js, "script.js: writes the year with textContent")
for pattern in DANGEROUS_PATTERNS:
    check(not re.search(pattern, js, re.I), f"script.js: no {pattern}")

for path in HTML_FILES + [JS_FILE, CSS_FILE, SVG_FILE]:
    text = path.read_text(encoding="utf-8")
    label = path.relative_to(ROOT).as_posix()
    for pattern in SECRET_PATTERNS:
        check(not re.search(pattern, text, re.I), f"{label}: no {pattern}")

print(f"\n{len(failures)} failure(s).")
sys.exit(1 if failures else 0)
