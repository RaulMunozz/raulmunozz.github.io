# Security Policy

**Last reviewed:** 2026-11-24  
**Scope:** the public static portfolio hosted with GitHub Pages at `https://raulmunozz.github.io/` and `https://raulmunozz.github.io/portfolio/`.

## Architecture

This project is a static website. It has:

- HTML, CSS and a single small JavaScript file.
- No backend, application server or server-side runtime.
- No database or data storage.
- No user accounts, authentication, sessions or cookies.
- No forms, file uploads, APIs, endpoints or user-controlled input.
- No environment variables, API keys or private credentials in the client code.
- No package manager, build step or third-party JavaScript dependencies.

External resources are limited to Google Fonts CSS/font files and links to GitHub and `mailto:`.

## Implemented protections

| Protection | Implementation |
|---|---|
| Content-Security-Policy | `<meta http-equiv="Content-Security-Policy">` in both HTML entry points. Allows only same-origin scripts, styles and images, plus the two Google Fonts origins. Blocks plugins, frames, workers, form submissions, `base` tag hijacking and unknown script sources. |
| Referrer privacy | `<meta name="referrer" content="no-referrer">` prevents the site URL from being sent as a referrer to external links. |
| Reverse tabnabbing | All external links use `rel="noopener noreferrer"`. |
| XSS-safe DOM usage | The only script writes the footer year with `textContent`; there is no `innerHTML`, `eval` or dynamic HTML insertion. |
| No inline code | JavaScript and CSS are loaded from local files, so the CSP does not require `unsafe-inline` or `unsafe-eval`. |
| HTTPS | GitHub Pages redirects HTTP to HTTPS and sends HSTS for the `github.io` domain. |
| Secrets | No credentials, tokens or private keys are present in the repository or client code. |
| Clickjacking | The page contains no sensitive actions. Full frame-ancestor enforcement requires an HTTP response header, which GitHub Pages does not allow; see Limitations. |
| Supply chain | No npm/Composer/pip dependencies are used by the deployed site. |

## Security configuration

The deployed CSP is:

```text
default-src 'self';
base-uri 'none';
object-src 'none';
script-src 'self';
style-src 'self' https://fonts.googleapis.com;
font-src 'self' https://fonts.gstatic.com;
img-src 'self' data:;
connect-src 'self';
form-action 'none';
frame-src 'none';
worker-src 'none';
upgrade-insecure-requests
```

Notes:

- `frame-ancestors` is intentionally not placed in the meta CSP because browsers ignore that directive in `<meta>` elements.
- `upgrade-insecure-requests` is safe here because the site has no HTTP-only resources.
- The Google Fonts domains are the only allowed third-party origins.

## Environment variables

None. The site does not require environment variables, secrets or API keys.

## Secure deployment

1. Keep only the published files in the GitHub Pages branch: `index.html`, `styles.css`, `script.js`, `favicon.svg`, `portfolio/index.html`, `README.md`, `SECURITY.md` and `tests/security_check.py`.
2. Keep GitHub Pages set to **Deploy from a branch → main / root**.
3. Protect the `main` branch and require reviewed changes before merging.
4. Enable two-factor authentication on the GitHub account.
5. Never commit tokens, passwords, `.env` files or private keys.
6. After each deployment, verify both URLs with `curl -I` and confirm the page loads without CSP violations in the browser console.
7. Keep the CSP in sync in both `index.html` files if the site later adds scripts, styles, images or APIs.

## Known limitations

These items cannot be fully configured on GitHub Pages hosted at `github.io` without moving to a custom domain behind a CDN/proxy:

- Custom HTTP response headers cannot be set by the repository. This includes `X-Content-Type-Options`, `X-Frame-Options` / `frame-ancestors`, `Permissions-Policy`, a header-delivered CSP and a custom HSTS value.
- `Access-Control-Allow-Origin: *` is added by GitHub Pages for public static assets. This is acceptable because the site serves only public files, but it is not configurable here.
- `Strict-Transport-Security` is sent by GitHub Pages with `max-age=31556952`; `includeSubDomains` and `preload` are not controlled by this project.
- There are no application request logs, WAF, rate limiting or intrusion detection because there is no application layer.
- Google Fonts is a third-party dependency. Removing it would require self-hosting font files, which would change the deployment but not the visible design.
- If a future contact form, API, login, database or user input is added, this security model must be revisited and server-side controls implemented.

## Maintenance

- Review this file after any change to HTML, CSS, JavaScript, hosting or external resources.
- Run `python tests/security_check.py` after each change; it must exit with code 0.
- Periodically confirm HTTP → HTTPS redirection and HSTS with `curl -I`.
- Check the browser console for CSP violations after deployments.
- Review GitHub security features: Dependabot alerts, secret scanning and branch protection.
- Report security issues privately to the email address published on the site.

## Automated verification

A dependency-free check is included at `tests/security_check.py`. Run it from the repository root:

```powershell
python tests/security_check.py
```

It checks both HTML entry points for the required CSP directives, the `no-referrer` policy, `noopener noreferrer` on every external link, the six preserved project cards and code links, and the absence of dangerous DOM patterns and common secret patterns in the deployed source files. Exit code 0 means every check passed.

## Classification

Low residual risk overall due to the static, read-only nature of the site. The main remaining risks are platform-level header limitations and third-party font delivery.
