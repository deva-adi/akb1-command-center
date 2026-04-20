# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 5.2.x   | ✅ Active  |
| < 5.2   | ❌ No      |

Only the latest release on the `main` branch receives security patches.

## Reporting a Vulnerability

**Do NOT open a public GitHub issue for security vulnerabilities.**

### Responsible Disclosure Process

1. **Email:** Send a detailed report to **security@akb1.dev** (or the repository owner's email listed in the README).
2. **Include:**
   - Description of the vulnerability and its potential impact
   - Steps to reproduce (proof of concept if possible)
   - Affected version(s) and component (backend, frontend, Docker config)
   - Suggested fix (optional but appreciated)
3. **Response SLA:**
   - **Acknowledgement:** Within 48 hours of receipt
   - **Triage & severity assessment:** Within 5 business days
   - **Fix timeline:** Critical/High within 14 days; Medium within 30 days; Low within 60 days
4. **Disclosure:** We follow coordinated disclosure — the reporter is credited (unless anonymity is requested) once a patch is released. We will not pursue legal action against researchers who follow this policy.

### Severity Classification (CVSS v3.1 Aligned)

| Severity | CVSS Score | Example |
|----------|-----------|---------|
| Critical | 9.0–10.0 | Remote code execution, auth bypass on exposed instance |
| High     | 7.0–8.9  | SQL injection, privilege escalation, data exfiltration |
| Medium   | 4.0–6.9  | Stored XSS, CSRF, information disclosure |
| Low      | 0.1–3.9  | Verbose error messages, minor info leak |

## Security Architecture Overview

AKB1 Command Center is designed as a **single-user, localhost-first** application. By default, the dashboard binds to `127.0.0.1:9000` and is not network-accessible.

For deployment scenarios requiring network access or multi-user authentication, see [`docs/SECURITY_GUIDE.md`](docs/SECURITY_GUIDE.md) which documents:

- **4-tier authentication strategy** (None → Basic Auth → OAuth2 Proxy → Built-in OIDC)
- **HTTPS termination** via Caddy or Nginx reverse proxy
- **API key authentication** for programmatic access
- **Container hardening** (non-root, read-only filesystem, dropped capabilities)
- **Rate limiting** (slowapi — 60 req/min read, 10 req/min write)
- **RBAC model** (Admin, Portfolio Lead, Viewer, API Service)

## Security Best Practices for Deployers

1. **Keep Docker and host OS updated** — apply security patches regularly
2. **Never expose port 9001 (API) directly** — route through nginx/Caddy
3. **Use HTTPS in production** — `docker-compose.proxy.yml` provides a Caddy overlay with automatic Let's Encrypt
4. **Rotate API keys** periodically via Tab 11 (Data Hub & Settings)
5. **Review container images** — run `docker scout cves` or `trivy image` before deployment
6. **Backup regularly** — automated daily backup is enabled by default; verify `./backups/` directory
7. **Monitor access logs** — structured JSON logs via structlog; forward to your SIEM if available

## Dependencies & Supply Chain

- All Python dependencies are pinned with minimum versions in `requirements.txt`
- Frontend dependencies managed via `package-lock.json` (exact versions)
- CI pipeline runs Trivy container scan — zero critical/high CVEs at release
- SBOM (Software Bill of Materials) generated in CycloneDX format at each release
- No telemetry, analytics, or phone-home behaviour — all data stays local

## Out of Scope

The following are **not** considered vulnerabilities:
- Attacks requiring physical access to the host machine
- Self-XSS (user attacking their own session)
- Denial of service against localhost-only deployments
- Social engineering attacks against the deployer
- Vulnerabilities in Docker itself or the host OS (report to respective vendors)

---

**Last updated:** 2026-04-16 | AKB1 Command Center v5.2
