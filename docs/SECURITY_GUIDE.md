# AKB1 Command Center v5.2 — Security Guide

**Version:** 1.0 | **Date:** 2026-04-16
**Author:** Adi Kompalli | AKB1 Framework
**Audience:** Deployers, DevOps Engineers, IT Security Teams, CTOs evaluating the platform
**Benchmark:** OWASP Top 10 (2021), NIST SP 800-53, CIS Docker Benchmark v1.6, OWASP ASVS L1/L2

---

## Executive Summary

AKB1 Command Center ships as a **localhost-first, single-user application** by default — no authentication required for local use. This guide documents four progressive security tiers for deployers who need network exposure, team access, or enterprise compliance. Each tier adds defense layers without requiring application code changes until Tier 3 (built-in OIDC, planned for v5.4).

**Industry Benchmark:** This 4-tier progressive security model follows the same pattern used by Grafana (anonymous → org viewer → LDAP/OIDC), Metabase (no auth → basic → SSO), and GitLab (open → LDAP → SAML). The principle: don't force auth complexity on single-user localhost deployments, but provide a clear upgrade path to enterprise-grade security.

---

## Table of Contents

1. [Threat Model](#1-threat-model)
2. [4-Tier Authentication Strategy](#2-4-tier-authentication-strategy)
3. [Tier 0: Localhost (Default)](#3-tier-0-localhost-default)
4. [Tier 1: Reverse Proxy Basic Auth](#4-tier-1-reverse-proxy-basic-auth)
5. [Tier 2: OAuth2 Proxy Sidecar (SSO)](#5-tier-2-oauth2-proxy-sidecar-sso)
6. [Tier 3: Built-in OIDC (v5.4 Roadmap)](#6-tier-3-built-in-oidc-v54-roadmap)
7. [HTTPS Configuration](#7-https-configuration)
8. [API Key Authentication](#8-api-key-authentication)
9. [Rate Limiting](#9-rate-limiting)
10. [Container Hardening](#10-container-hardening)
11. [RBAC Model](#11-rbac-model)
12. [Input Validation & Injection Prevention](#12-input-validation--injection-prevention)
13. [CORS & Header Security](#13-cors--header-security)
14. [Data Protection](#14-data-protection)
15. [Logging & Audit Trail](#15-logging--audit-trail)
16. [Dependency & Supply Chain Security](#16-dependency--supply-chain-security)
17. [OWASP Top 10 Mapping](#17-owasp-top-10-mapping)
18. [Deployment Patterns](#18-deployment-patterns)
19. [Security Checklist for Deployers](#19-security-checklist-for-deployers)
20. [Incident Response](#20-incident-response)

---

## 1. Threat Model

### Deployment Scenarios & Attack Surface

| Scenario | Network Exposure | Primary Threats | Recommended Tier |
|----------|-----------------|-----------------|-----------------|
| **Personal laptop** — single user, localhost | None (127.0.0.1 only) | Physical access, malware on host | Tier 0 |
| **Team LAN** — shared within office network | LAN (192.168.x.x) | Unauthorized LAN access, session hijacking | Tier 1 |
| **VPN/cloud** — accessible over corporate VPN or cloud VM | Private network | Credential theft, MITM, brute force | Tier 2 |
| **Public internet** — demo or SaaS deployment | Internet | Full OWASP Top 10, DDoS, credential stuffing | Tier 2 + WAF |

### Assets to Protect

| Asset | Sensitivity | Impact if Compromised |
|-------|-----------|----------------------|
| Delivery KPIs (CPI, margin, utilization) | Confidential | Competitive intelligence leak |
| Financial data (revenue, cost, EVM) | Highly Confidential | Commercial damage, client trust |
| Customer satisfaction scores | Confidential | Relationship damage |
| Resource names and utilization | PII-adjacent | Privacy breach |
| AI governance audit trail | Internal | Compliance audit failure |
| SQLite database file | All of the above | Full data breach |
| API keys | Secret | Unauthorized data access/modification |

### Trust Boundaries

```
┌─────────────────────────────────────────────────────────────────┐
│ HOST MACHINE (Trust Boundary 1)                                 │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ DOCKER NETWORK (Trust Boundary 2)                         │  │
│  │                                                           │  │
│  │  ┌─────────────┐    ┌───────────────┐    ┌──────────┐   │  │
│  │  │  Caddy/Nginx │───►│   Frontend    │───►│ Backend  │   │  │
│  │  │  (TLS term)  │    │   (nginx)     │    │ (FastAPI)│   │  │
│  │  └─────────────┘    └───────────────┘    └────┬─────┘   │  │
│  │        ▲                                       │         │  │
│  │        │                                  ┌────▼─────┐   │  │
│  │     HTTPS                                 │  SQLite  │   │  │
│  │        │                                  │  /data/  │   │  │
│  │        │                                  └──────────┘   │  │
│  └────────┼──────────────────────────────────────────────────┘  │
│           │                                                     │
└───────────┼─────────────────────────────────────────────────────┘
            │
       User Browser
```

---

## 2. 4-Tier Authentication Strategy

| Tier | Mechanism | Effort | When to Use | Industry Precedent |
|------|-----------|--------|-------------|-------------------|
| **0 — None** | Bind `127.0.0.1` only | Zero config | Personal laptop, demo | Grafana default, Metabase default |
| **1 — Reverse Proxy Basic Auth** | Nginx/Caddy `basicauth` | 10 min | Team LAN, small office | Prometheus + Nginx pattern |
| **2 — OAuth2 Proxy Sidecar** | oauth2-proxy container + Google/Azure AD/Okta/Keycloak/GitHub | 30 min | Corporate VPN, cloud VM, multi-user | Grafana + oauth2-proxy, Kubernetes dashboard |
| **3 — Built-in OIDC** | python-jose + authlib in FastAPI | v5.4 roadmap | SaaS, enterprise, fine-grained RBAC | GitLab, Redmine, Mattermost |

**Principle:** Each tier is additive. Tier 2 includes all Tier 1 hardening. Tier 3 includes all Tier 2 capabilities.

---

## 3. Tier 0: Localhost (Default)

### What Ships Out of the Box

- **Port binding:** `127.0.0.1:9000` — dashboard accessible only from the host machine
- **API binding:** `127.0.0.1:9001` — Swagger docs and API endpoints localhost-only
- **No authentication** — the deployer is the sole user
- **CORS:** Locked to `http://localhost:9000` (configurable via `CORS_ORIGINS` env var)
- **Rate limiting:** `slowapi` middleware — 60 GET/min, 10 POST/min per IP
- **Input validation:** All API inputs validated via Pydantic v2 schemas
- **SQL injection protection:** Parameterised queries via SQLAlchemy/aiosqlite
- **File upload limits:** 50 MB max (configurable)
- **Structured logging:** JSON logs via structlog — no sensitive data in logs

### Security Controls Active at Tier 0

| Control | Implementation | OWASP Mapping |
|---------|---------------|---------------|
| Localhost binding | `127.0.0.1:9000` in docker-compose.yml | A01:2021 (Broken Access Control) |
| Input validation | Pydantic v2 request models | A03:2021 (Injection) |
| Parameterised SQL | SQLAlchemy + aiosqlite | A03:2021 (Injection) |
| Rate limiting | slowapi (leaky bucket) | A04:2021 (Insecure Design) |
| CORS restriction | FastAPI CORSMiddleware | A05:2021 (Security Misconfiguration) |
| Dependency scanning | Trivy in CI, SBOM at release | A06:2021 (Vulnerable Components) |
| Structured logging | structlog JSON, no PII in logs | A09:2021 (Logging Failures) |
| Non-root container | `USER 1001` in Dockerfile | CIS Docker 4.1 |
| Read-only filesystem | `read_only: true` in docker-compose | CIS Docker 5.12 |
| No-new-privileges | `security_opt: no-new-privileges` | CIS Docker 5.25 |
| Health check | `/health` endpoint, no sensitive data | Operational security |

### What Tier 0 Does NOT Protect Against

- Someone on the same machine with a different user account (they can access localhost)
- Malware on the host machine that can make HTTP requests
- Physical access to the machine (can copy the SQLite file directly)

**Mitigation:** Full-disk encryption (FileVault on macOS, BitLocker on Windows, LUKS on Linux).

---

## 4. Tier 1: Reverse Proxy Basic Auth

### When to Use

- Small team (2–10 users) on the same LAN
- No SSO/IdP infrastructure available
- Quick protection for a demo or staging environment

### Caddy Setup (Recommended — Automatic HTTPS)

Use the provided `docker-compose.proxy.yml` overlay:

```bash
# macOS / Linux
docker compose -f docker-compose.yml -f docker-compose.proxy.yml up -d

# Windows PowerShell
docker compose -f docker-compose.yml -f docker-compose.proxy.yml up -d
```

The Caddy reverse proxy provides:
- Automatic HTTPS via Let's Encrypt (for public domains) or self-signed certs (for LAN)
- HTTP/2 by default
- Basic Auth with bcrypt-hashed passwords
- Security headers (HSTS, X-Frame-Options, CSP, etc.)

### Password Management

```bash
# Generate a bcrypt hash for Caddy basicauth
docker run --rm caddy:2-alpine caddy hash-password --plaintext 'YourSecurePassword'
```

Update the hash in `Caddyfile`:
```
basicauth /* {
    admin $2a$14$HASH_HERE
    viewer $2a$14$HASH_HERE
}
```

### Nginx Alternative

For deployers who prefer Nginx:

```nginx
server {
    listen 443 ssl;
    server_name akb1.yourcompany.com;

    ssl_certificate     /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;

    # Security headers
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    auth_basic "AKB1 Command Center";
    auth_basic_user_file /etc/nginx/.htpasswd;

    location / {
        proxy_pass http://akb1-frontend:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ {
        proxy_pass http://akb1-backend:9001/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Generate `.htpasswd`:
```bash
# Install apache2-utils (Debian/Ubuntu) or httpd-tools (RHEL/Fedora)
htpasswd -nbBC 10 admin YourSecurePassword >> .htpasswd
```

---

## 5. Tier 2: OAuth2 Proxy Sidecar (SSO)

### When to Use

- Corporate deployment with existing IdP (Google Workspace, Azure AD, Okta, Keycloak, GitHub)
- Multi-user access with SSO
- Compliance requirement for centralized authentication
- No application code changes needed

### Architecture

```
User Browser ──HTTPS──► Caddy (TLS) ──► oauth2-proxy ──► AKB1 Frontend
                                              │
                                              ▼
                                        Identity Provider
                                    (Google/Azure AD/Okta/
                                     Keycloak/GitHub)
```

### docker-compose.sso.yml (Overlay)

```yaml
version: '3.8'

services:
  oauth2-proxy:
    image: quay.io/oauth2-proxy/oauth2-proxy:v7.6.0
    container_name: akb1-oauth2-proxy
    environment:
      OAUTH2_PROXY_PROVIDER: ${OAUTH2_PROVIDER:-google}
      OAUTH2_PROXY_CLIENT_ID: ${OAUTH2_CLIENT_ID}
      OAUTH2_PROXY_CLIENT_SECRET: ${OAUTH2_CLIENT_SECRET}
      OAUTH2_PROXY_COOKIE_SECRET: ${OAUTH2_COOKIE_SECRET}
      OAUTH2_PROXY_EMAIL_DOMAINS: ${OAUTH2_EMAIL_DOMAINS:-*}
      OAUTH2_PROXY_UPSTREAMS: http://akb1-frontend:80
      OAUTH2_PROXY_HTTP_ADDRESS: 0.0.0.0:4180
      OAUTH2_PROXY_REDIRECT_URL: ${OAUTH2_REDIRECT_URL:-https://akb1.yourcompany.com/oauth2/callback}
      OAUTH2_PROXY_COOKIE_SECURE: "true"
      OAUTH2_PROXY_COOKIE_HTTPONLY: "true"
      OAUTH2_PROXY_COOKIE_SAMESITE: lax
      OAUTH2_PROXY_SET_XAUTHREQUEST: "true"
      OAUTH2_PROXY_PASS_ACCESS_TOKEN: "false"
      OAUTH2_PROXY_SKIP_PROVIDER_BUTTON: "true"
      OAUTH2_PROXY_SESSION_STORE_TYPE: cookie
      OAUTH2_PROXY_COOKIE_EXPIRE: 8h
      OAUTH2_PROXY_COOKIE_REFRESH: 1h
    ports:
      - "127.0.0.1:4180:4180"
    depends_on:
      frontend:
        condition: service_started
    restart: unless-stopped
    networks:
      - default

  caddy:
    image: caddy:2-alpine
    container_name: akb1-caddy
    volumes:
      - ./Caddyfile.sso:/etc/caddy/Caddyfile
      - caddy-data:/data
      - caddy-config:/config
    ports:
      - "${HTTPS_PORT:-443}:443"
      - "${HTTP_PORT:-80}:80"
    depends_on:
      - oauth2-proxy
    restart: unless-stopped
    networks:
      - default

volumes:
  caddy-data:
  caddy-config:
```

### IdP Setup Guides

#### Google Workspace

1. Go to [Google Cloud Console](https://console.cloud.google.com/) → APIs & Services → Credentials
2. Create OAuth 2.0 Client ID (Web application)
3. Set authorized redirect URI: `https://akb1.yourcompany.com/oauth2/callback`
4. Copy Client ID and Client Secret to `.env`
5. Set `OAUTH2_EMAIL_DOMAINS=yourcompany.com` to restrict access

#### Azure AD (Entra ID)

1. Azure Portal → App registrations → New registration
2. Redirect URI: `https://akb1.yourcompany.com/oauth2/callback` (Web)
3. Certificates & secrets → New client secret
4. Set `OAUTH2_PROVIDER=azure`, add `OAUTH2_PROXY_AZURE_TENANT` to `.env`

#### Okta

1. Okta Admin → Applications → Create App Integration → OIDC → Web Application
2. Sign-in redirect URI: `https://akb1.yourcompany.com/oauth2/callback`
3. Set `OAUTH2_PROVIDER=oidc`, `OAUTH2_PROXY_OIDC_ISSUER_URL=https://yourorg.okta.com`

#### Keycloak (Self-Hosted)

1. Create realm and client in Keycloak admin
2. Set `OAUTH2_PROVIDER=keycloak-oidc`
3. Set `OAUTH2_PROXY_OIDC_ISSUER_URL=https://keycloak.yourcompany.com/realms/akb1`

#### GitHub

1. GitHub → Settings → Developer settings → OAuth Apps → New
2. Authorization callback URL: `https://akb1.yourcompany.com/oauth2/callback`
3. Set `OAUTH2_PROVIDER=github`, `OAUTH2_PROXY_GITHUB_ORG=your-org` (optional)

### Session Management

| Setting | Default | Production Recommendation |
|---------|---------|--------------------------|
| Session store | Cookie | Cookie (stateless) or Redis (scalable) |
| Cookie expiry | 8 hours | 8 hours (workday session) |
| Cookie refresh | 1 hour | 1 hour (re-validate with IdP) |
| Cookie secure | true | true (HTTPS required) |
| Cookie httponly | true | true (prevent XSS access) |
| Cookie samesite | lax | lax (CSRF protection) |
| Pass access token | false | false (minimise token exposure) |

### Launching with SSO

```bash
# Generate a cookie secret (32-byte random)
dd if=/dev/urandom bs=32 count=1 2>/dev/null | base64 | tr -d '\n' > cookie_secret.txt

# Set environment variables
export OAUTH2_CLIENT_ID="your-client-id"
export OAUTH2_CLIENT_SECRET="your-client-secret"
export OAUTH2_COOKIE_SECRET=$(cat cookie_secret.txt)
export OAUTH2_REDIRECT_URL="https://akb1.yourcompany.com/oauth2/callback"
export OAUTH2_EMAIL_DOMAINS="yourcompany.com"

# Launch with SSO overlay
docker compose -f docker-compose.yml -f docker-compose.sso.yml up -d
```

---

## 6. Tier 3: Built-in OIDC (v5.4 Roadmap)

### Planned for v5.4 — Architecture Documented Now

Tier 3 embeds authentication directly in the FastAPI backend, enabling:
- Fine-grained RBAC enforcement at the API level (not just perimeter auth)
- Per-user audit trails ("who changed what, when")
- Row-level access control (user sees only their programmes)
- Native login page with AKB1 branding

### Technical Approach

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| JWT verification | python-jose + cryptography | Verify IdP-issued tokens server-side |
| OIDC client | authlib | Standards-compliant OIDC flow |
| Session management | itsdangerous (signed cookies) | Stateless, no Redis dependency |
| Password hashing | passlib[bcrypt] | For local-account fallback |
| RBAC middleware | FastAPI Depends() chain | Per-endpoint role checks |

### Database Schema (Stub Tables — Created in v5.2, Populated in v5.4)

```sql
-- Users table (stub — populated when Tier 3 auth is enabled)
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    display_name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'viewer',      -- admin, portfolio_lead, viewer, api_service
    is_active BOOLEAN DEFAULT 1,
    auth_provider TEXT DEFAULT 'local',        -- local, google, azure_ad, okta, keycloak, github
    external_id TEXT,                          -- IdP subject identifier
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User-role assignments for fine-grained access
CREATE TABLE user_roles (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    role TEXT NOT NULL,                        -- admin, portfolio_lead, viewer, api_service
    scope_type TEXT,                           -- NULL (global), 'programme', 'project'
    scope_id INTEGER,                          -- programme or project ID (NULL = all)
    granted_by INTEGER REFERENCES users(id),
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, role, scope_type, scope_id)
);

CREATE INDEX idx_user_roles_user ON user_roles(user_id);
CREATE INDEX idx_users_email ON users(email);
```

### Login Page Design

```
┌─────────────────────────────────────────────────┐
│                                                 │
│      ┌─────────────────────────────────┐       │
│      │     AKB1 COMMAND CENTER         │       │
│      │     ─────────────────           │       │
│      │                                 │       │
│      │  ┌─── Sign in with ──────────┐  │       │
│      │  │  [Google]  [Azure AD]     │  │       │
│      │  │  [Okta]    [Keycloak]     │  │       │
│      │  │  [GitHub]                 │  │       │
│      │  └───────────────────────────┘  │       │
│      │                                 │       │
│      │  ──────── or ─────────          │       │
│      │                                 │       │
│      │  Email:    [________________]   │       │
│      │  Password: [________________]   │       │
│      │                                 │       │
│      │  [        Sign In          ]    │       │
│      │                                 │       │
│      │  Navy #1B2A4A background        │       │
│      │  Ice Blue #D5E8F0 card          │       │
│      │  Amber #F59E0B CTA button       │       │
│      └─────────────────────────────────┘       │
│                                                 │
│  AKB1 v5.4 | Delivery Intelligence Platform    │
└─────────────────────────────────────────────────┘
```

### v5.4 Authentication Flow

```
Browser → FastAPI /auth/login → Redirect to IdP
                                        │
IdP authenticates user ◄────────────────┘
        │
        ▼
IdP redirects to /auth/callback with authorization code
        │
        ▼
FastAPI exchanges code for tokens (server-side)
        │
        ▼
FastAPI creates session cookie (signed, httponly, secure)
        │
        ▼
FastAPI checks user_roles table for RBAC
        │
        ▼
Dashboard renders (role-appropriate views)
```

---

## 7. HTTPS Configuration

### Why HTTPS Matters Even on LAN

- Prevents credential sniffing (Basic Auth headers are base64-encoded, NOT encrypted)
- Required for secure cookies (`Secure` flag)
- Required for HTTP/2 performance benefits
- Required for OAuth2 callback URLs (most IdPs reject `http://`)

### Caddy (Automatic HTTPS — Recommended)

Caddy automatically provisions and renews TLS certificates from Let's Encrypt for public domains, and generates self-signed certificates for internal/LAN domains.

See `Caddyfile` in the repo root for the ready-to-use configuration.

### Manual Certificate (LAN Deployments)

For LAN deployments without public DNS:

```bash
# Generate self-signed cert (valid 365 days)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes \
  -subj "/CN=akb1.local" -addext "subjectAltName=DNS:akb1.local,IP:192.168.1.100"
```

---

## 8. API Key Authentication

### Mechanism

AKB1 generates a random API key on first run, stored in `app_settings` table. Used for:
- Programmatic data upload (CI/CD pipelines, cron jobs, Power Automate, Zapier)
- Headless API access without browser session

### Usage

```bash
# Include in Authorization header
curl -H "Authorization: Bearer akb1_sk_xxxxxxxxxxxxxxxxxxxx" \
     http://localhost:9001/api/v1/programs

# Or as query parameter (less secure — visible in logs)
curl "http://localhost:9001/api/v1/programs?api_key=akb1_sk_xxxxxxxxxxxxxxxxxxxx"
```

### Key Management

| Action | Method |
|--------|--------|
| View current key | Tab 11 → Settings → API Key (masked, reveal on click) |
| Rotate key | Tab 11 → Settings → Rotate API Key (invalidates previous immediately) |
| Disable API key auth | Set `API_KEY_ENABLED=false` in `.env` |

### Key Format

```
akb1_sk_{32-character-hex-random}
```

Generated via `secrets.token_hex(32)` in Python. Stored hashed (SHA-256) in `app_settings`; the plaintext is shown once at generation and never stored.

---

## 9. Rate Limiting

### Implementation

Rate limiting via `slowapi` (based on Starlette `limits`), using leaky bucket algorithm.

| Endpoint Type | Limit | Rationale |
|---------------|-------|-----------|
| GET (read) | 60/minute per IP | Normal dashboard polling (React Query refetch) |
| POST/PUT (write) | 10/minute per IP | Data upload, settings changes |
| POST /api/v1/upload | 5/minute per IP | Bulk import throttle |
| GET /health | Unlimited | Load balancer health checks |
| Swagger /docs | 30/minute per IP | API exploration |

### Configuration

```python
# backend/app/middleware/rate_limit.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])

# Per-endpoint override example
@app.post("/api/v1/upload")
@limiter.limit("5/minute")
async def upload_file(request: Request, file: UploadFile):
    ...
```

### Rate Limit Headers

Every response includes:
- `X-RateLimit-Limit: 60`
- `X-RateLimit-Remaining: 58`
- `X-RateLimit-Reset: 1682000000`

Exceeding the limit returns `429 Too Many Requests` with a `Retry-After` header.

---

## 10. Container Hardening

### Dockerfile Best Practices (CIS Docker Benchmark Aligned)

```dockerfile
# backend/Dockerfile — security-relevant sections
FROM python:3.12-slim AS builder

# Install dependencies in builder stage (no dev tools in final image)
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-slim AS runtime

# CIS 4.1: Non-root user
RUN groupadd -r akb1 && useradd -r -g akb1 -d /app -s /sbin/nologin akb1

# Copy only runtime artifacts
COPY --from=builder /root/.local /home/akb1/.local
COPY ./app /app/app

# CIS 4.6: Add HEALTHCHECK
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:9001/health')" || exit 1

# CIS 4.1: Run as non-root
USER akb1
WORKDIR /app

ENV PATH="/home/akb1/.local/bin:${PATH}"

EXPOSE 9001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9001", "--workers", "2"]
```

### docker-compose.yml Security Directives

```yaml
services:
  backend:
    # ... existing config ...
    security_opt:
      - no-new-privileges:true      # CIS 5.25: Prevent privilege escalation
    read_only: true                  # CIS 5.12: Read-only filesystem
    tmpfs:
      - /tmp:noexec,nosuid,size=64m # Writable temp (logs, cache) — no exec
    cap_drop:
      - ALL                          # CIS 5.3: Drop all capabilities
    cap_add:
      - NET_BIND_SERVICE             # Only capability needed (bind ports)
```

### Security Scanning

| Tool | Purpose | When |
|------|---------|------|
| Trivy | Container CVE scan | CI pipeline + pre-release |
| Docker Scout | Vulnerability database | On-demand |
| Grype | SBOM vulnerability matching | Release gate |
| Hadolint | Dockerfile best practices | Pre-commit hook |
| Bandit | Python security linter | CI pipeline |

---

## 11. RBAC Model

### Conceptual Roles (Enforced at Tier 2 via header claims, Tier 3 via database)

| Role | Read KPIs | Write Data | Admin Settings | API Access | Scope |
|------|-----------|-----------|---------------|-----------|-------|
| **Admin** | ✅ All | ✅ All | ✅ | ✅ Full | Global |
| **Portfolio Lead** | ✅ All | ✅ Own programmes | ❌ | ✅ Scoped | Programme-level |
| **Viewer** | ✅ All | ❌ | ❌ | ✅ Read-only | Global read |
| **API Service** | ✅ Scoped | ✅ Scoped | ❌ | ✅ Scoped | Per API key |

### Implementation by Tier

- **Tier 0–1:** Single implicit admin (no RBAC needed)
- **Tier 2:** OAuth2 Proxy passes `X-Auth-Request-Email` and `X-Auth-Request-Groups` headers. Backend can read these to enforce role-based UI visibility.
- **Tier 3:** Full database-backed RBAC via `users` + `user_roles` tables with FastAPI `Depends()` middleware.

---

## 12. Input Validation & Injection Prevention

### SQL Injection

- All database queries use SQLAlchemy ORM or parameterised aiosqlite queries
- No raw SQL string concatenation anywhere in the codebase
- Pydantic models validate all API inputs before they reach the database layer

### XSS (Cross-Site Scripting)

- React auto-escapes all rendered content by default
- `Content-Security-Policy` header restricts script sources to `'self'`
- No `dangerouslySetInnerHTML` usage except for sanitized narrative templates

### Path Traversal

- File upload handler validates filename with `pathlib.Path.name` (strips directory components)
- Upload directory is container-internal, not mapped to host filesystem
- File extension whitelist: `.csv`, `.xlsx` only

### SSRF (Server-Side Request Forgery)

- No user-controlled URL fetching in backend (no proxy features)
- Webhook URLs (Smart Ops) validated against private IP ranges (RFC 1918) before use

---

## 13. CORS & Header Security

### CORS Configuration

```python
# FastAPI CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),  # Default: http://localhost:9000
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

### Security Headers (Caddy/Nginx)

| Header | Value | Purpose |
|--------|-------|---------|
| `Strict-Transport-Security` | `max-age=63072000; includeSubDomains` | Force HTTPS |
| `X-Frame-Options` | `SAMEORIGIN` | Prevent clickjacking |
| `X-Content-Type-Options` | `nosniff` | Prevent MIME sniffing |
| `X-XSS-Protection` | `0` | Disabled (CSP supersedes) |
| `Content-Security-Policy` | `default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'` | Restrict resource loading |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Limit referrer leakage |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=()` | Disable unused APIs |

---

## 14. Data Protection

### At Rest

- SQLite database stored in Docker volume (`akb1-data`)
- Volume is on the host filesystem — inherits host-level encryption (FileVault/BitLocker/LUKS)
- Backup files stored in `./backups/` directory — same encryption applies
- API keys stored hashed (SHA-256) in `app_settings`

### In Transit

- **Tier 0:** Localhost — no network transit
- **Tier 1+:** TLS 1.2/1.3 via Caddy or Nginx
- Docker internal network: containers communicate over bridge network (not encrypted, but not exposed externally)

### Data Retention

| Data Type | Retention | Mechanism |
|-----------|----------|-----------|
| KPI snapshots | Indefinite (user manages) | Manual deletion via UI |
| Import snapshots | Last 10 imports | Auto-pruned by application |
| Backups | 30 days rolling | `backup.sh` cron cleanup |
| Audit log | Indefinite | Exportable, manual prune |
| Structured logs | 7 days | Docker log rotation config |

---

## 15. Logging & Audit Trail

### Structured Logging

```json
{
  "timestamp": "2026-04-16T10:30:00Z",
  "level": "info",
  "event": "data_import",
  "user": "admin",
  "source_file": "kpi_monthly.xlsx",
  "rows_imported": 60,
  "rows_rejected": 2,
  "snapshot_id": "snap_20260416_103000",
  "ip": "127.0.0.1",
  "duration_ms": 1200
}
```

### What Gets Logged

| Event | Level | Details |
|-------|-------|---------|
| Application start/stop | INFO | Version, config, port |
| Data import | INFO | File, rows, snapshot ID |
| Data rollback | WARN | Snapshot ID, reason |
| Settings change | INFO | Field, old value, new value |
| API key rotation | WARN | Rotation timestamp |
| Rate limit exceeded | WARN | IP, endpoint, limit |
| Validation failure | WARN | Field, value, error |
| Unhandled exception | ERROR | Stack trace (no sensitive data) |

### What Does NOT Get Logged

- Actual financial values (revenue, cost, margin amounts)
- User credentials or session tokens
- Full request/response bodies
- Individual KPI data points

---

## 16. Dependency & Supply Chain Security

### Python Dependencies

- All versions pinned with `>=minimum` in `requirements.txt`
- `pip-audit` run in CI to detect known vulnerabilities
- No transitive dependency with known critical CVEs at release

### Frontend Dependencies

- `package-lock.json` committed for reproducible builds
- `npm audit` run in CI
- No CDN dependencies in production (all bundled via Vite)

### Container Base Images

- Backend: `python:3.12-slim` (Debian-based, minimal attack surface)
- Frontend: `node:20-slim` (build stage) + `nginx:1.25-alpine` (runtime)
- All images pinned by digest in CI for reproducibility

### SBOM

- Generated at each release in CycloneDX JSON format
- Includes all Python packages, npm packages, and system libraries
- Published as a release artifact on GitHub

---

## 17. OWASP Top 10 Mapping

| # | OWASP 2021 | AKB1 Mitigation | Status |
|---|-----------|-----------------|--------|
| A01 | Broken Access Control | Localhost binding, CORS lock, RBAC model, rate limiting | ✅ Tier 0+ |
| A02 | Cryptographic Failures | HTTPS via Caddy/Nginx, bcrypt for passwords, SHA-256 for API keys | ✅ Tier 1+ |
| A03 | Injection | Parameterised SQL (SQLAlchemy), Pydantic input validation, React auto-escape | ✅ Tier 0 |
| A04 | Insecure Design | Threat model documented, rate limiting, file upload restrictions | ✅ Tier 0 |
| A05 | Security Misconfiguration | Hardened docker-compose, non-root, read-only fs, no defaults in prod | ✅ Tier 0 |
| A06 | Vulnerable Components | Trivy scan, pip-audit, npm audit, SBOM at release | ✅ CI |
| A07 | Auth Failures | 4-tier strategy, bcrypt, cookie security, session expiry | ✅ Tier 1+ |
| A08 | Data Integrity Failures | Import validation, snapshot rollback, Alembic migrations | ✅ Tier 0 |
| A09 | Logging Failures | structlog JSON, audit trail, no sensitive data in logs | ✅ Tier 0 |
| A10 | SSRF | No user-controlled URL fetching, webhook URL validation | ✅ Tier 0 |

---

## 18. Deployment Patterns

### Pattern 1: Personal Laptop (Tier 0)

```bash
docker compose up -d
# Dashboard at http://localhost:9000 — no auth needed
```

### Pattern 2: Team Server with Basic Auth (Tier 1)

```bash
docker compose -f docker-compose.yml -f docker-compose.proxy.yml up -d
# Dashboard at https://akb1.yourserver.com — Basic Auth required
```

### Pattern 3: Corporate with SSO (Tier 2)

```bash
docker compose -f docker-compose.yml -f docker-compose.sso.yml up -d
# Dashboard at https://akb1.yourcompany.com — SSO via Google/Azure AD/Okta
```

### Pattern 4: Kubernetes (v5.3+)

Helm chart planned for v5.3. Will support:
- Ingress with cert-manager for TLS
- oauth2-proxy as sidecar or standalone
- Persistent volume for SQLite (or PostgreSQL DAL upgrade)
- Resource limits and pod security policy

---

## 19. Security Checklist for Deployers

### Before Going Live

- [ ] **HTTPS enabled** (Caddy or Nginx with valid certificate)
- [ ] **Ports 9000/9001 not directly exposed** (routed through reverse proxy)
- [ ] **Authentication configured** (Basic Auth minimum for non-localhost)
- [ ] **Default API key rotated** (Tab 11 → Settings → Rotate)
- [ ] **CORS_ORIGINS updated** to match your actual domain
- [ ] **Container images scanned** (`trivy image akb1-backend`, `trivy image akb1-frontend`)
- [ ] **Backup verified** (check `./backups/` directory has recent files)
- [ ] **Log forwarding configured** (Docker JSON log driver → your SIEM)
- [ ] **Host firewall configured** (only ports 80/443 open externally)
- [ ] **Docker and host OS updated** to latest security patches

### Periodic Review (Monthly)

- [ ] Rotate API keys
- [ ] Review access logs for anomalies
- [ ] Run `docker scout cves` or `trivy` on running images
- [ ] Verify backup integrity (restore test)
- [ ] Check for AKB1 version updates

---

## 20. Incident Response

### If You Suspect a Breach

1. **Contain:** Stop the container: `docker compose down`
2. **Preserve:** Copy logs and database before any changes: `cp -r ./backups/ ./incident-$(date +%s)/`
3. **Investigate:** Review structured logs for unauthorized access patterns
4. **Rotate:** Generate new API keys, change Basic Auth passwords, rotate OAuth2 client secrets
5. **Patch:** Update to latest AKB1 version, rebuild containers
6. **Report:** If vulnerability found, report per [SECURITY.md](../SECURITY.md)

---

**Last updated:** 2026-04-16 | AKB1 Command Center v5.2
**Benchmark sources:** OWASP Top 10 (2021), OWASP ASVS v4.0 Level 1–2, CIS Docker Benchmark v1.6, NIST SP 800-53 Rev 5 (AC, AU, SC families)
