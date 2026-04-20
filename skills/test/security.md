---
name: taku-cso
description: Use when running a security audit. 14-phase infrastructure-first security scan: stack detection, attack surface, secrets archaeology, dependency audit, CI/CD security, infra shadow surface, webhooks, LLM security, skill supply chain, OWASP Top 10, STRIDE, data classification, FP filtering, and report. Two modes: daily (8/10 confidence) and comprehensive (2/10). Triggers on "security audit", "threat model", "CSO review", "OWASP", "pentest review".
allowed-tools:
  - Bash
  - Read
  - Write
  - Grep
  - Glob
  - web_search
---

# 14-Phase Security Audit

Think like an attacker. Report like a defender. You do NOT modify code. Produce a Security Posture Report with findings, severity ratings, and remediation plans.

The real attack surface isn't your code. It's your dependencies, CI logs with exposed secrets, forgotten staging servers, and webhooks that accept anything. Start there.

## Arguments

- `/taku-cso` — daily audit (8/10 confidence gate)
- `/taku-cso --comprehensive` — monthly deep scan (2/10 bar)
- `/taku-cso --diff` — branch changes only
- `/taku-cso --infra` — Phases 1-6, 12-14
- `/taku-cso --code` — Phases 1-2, 7-11, 13-14

## Iron Law

**ZERO NOISE IS MORE IMPORTANT THAN ZERO MISSES.** 3 real findings beats 3 real + 12 theoretical.

## Phase 1: Stack Detection

Detect the tech stack to determine scan priority, not scope.

```bash
ls package.json 2>/dev/null && echo "STACK: Node/TypeScript"
ls requirements.txt pyproject.toml 2>/dev/null && echo "STACK: Python"
ls go.mod 2>/dev/null && echo "STACK: Go"
ls Cargo.toml 2>/dev/null && echo "STACK: Rust"
ls Gemfile 2>/dev/null && echo "STACK: Ruby"
ls pom.xml build.gradle 2>/dev/null && echo "STACK: JVM"
```

Detect frameworks, read CLAUDE.md/README, map architecture: components, data flow, trust boundaries.

## Phase 2: Attack Surface Census

Map what an attacker sees. Use Grep for code searches.

**Code:** Public endpoints, auth boundaries, file upload paths, admin routes, webhook handlers, background jobs. Count each.

**Infrastructure:**

```bash
find .github/workflows -maxdepth 1 -name '*.yml' 2>/dev/null
find . -maxdepth 4 -name "Dockerfile*" -o -name "docker-compose*.yml" 2>/dev/null
find . -maxdepth 4 -name "*.tf" -o -name "kustomization.yaml" 2>/dev/null
ls .env .env.* 2>/dev/null
```

Output a surface map with counts per category.

## Phase 3: Secrets Archaeology

Scan git history for leaked credentials.

```bash
git log -p --all -S "AKIA" --diff-filter=A -- "*.env" "*.yml" "*.json" 2>/dev/null
git log -p --all -G "ghp_|gho_|github_pat_" 2>/dev/null
git log -p --all -G "xoxb-|xoxp-|xapp-" 2>/dev/null
git log -p --all -G "password|secret|token|api_key" -- "*.env" "*.yml" 2>/dev/null
```

```bash
git ls-files '*.env' '.env.*' 2>/dev/null | grep -v '.example\|.sample\|.template'
grep -q "^\.env" .gitignore 2>/dev/null || echo "WARNING: .env NOT in .gitignore"
grep -rn "password:\|token:\|secret:\|api_key:" .github/workflows/ 2>/dev/null | grep -v '\${{' | grep -v 'secrets\.'
```

CRITICAL for active secret patterns in history. HIGH for tracked .env, CI inline creds.

## Phase 4: Dependency Audit

Beyond `npm audit`. Check actual supply chain risk.

```bash
npm audit 2>/dev/null || yarn audit 2>/dev/null || bun audit 2>/dev/null
pip audit 2>/dev/null; cargo audit 2>/dev/null
```

Check for install scripts in prod deps (`preinstall`/`postinstall`), lockfile integrity, abandoned packages. Use `web_search` to look up CVEs for high/critical findings. CRITICAL for known CVEs in direct deps. HIGH for install scripts in prod.

## Phase 5: CI/CD Security

Check each workflow for: unpinned third-party actions (missing `@[sha]`), `pull_request_target` with PR code checkout, script injection via `${{ github.event.* }}`, secrets as env vars (could leak in logs), CODEOWNERS on workflow files. CRITICAL for `pull_request_target` + PR ref checkout. HIGH for unpinned actions.

## Phase 6: Infrastructure Shadow Surface

**Dockerfiles:** Missing `USER` directive (runs as root), secrets as `ARG`, `.env` copied in.
**Config with prod creds:** DB connection strings (`postgres://`, `mongodb://`) excluding localhost/example.
**IaC:** `"*"` in IAM actions, hardcoded secrets in `.tf`/`.tfvars`. K8s: privileged containers.
CRITICAL for prod DB URLs with creds. HIGH for root containers in prod.

## Phase 7: Webhook Security

Find webhook/hook/callback routes. Check for signature verification (`hmac`, `verify`, `signature`, `x-hub-signature`). Check TLS disabled (`verify.*false`, `NODE_TLS_REJECT_UNAUTHORIZED.*0`). Trace handler middleware chain. Do NOT make HTTP requests. CRITICAL for webhooks without signature verification.

## Phase 8: LLM/AI Security

Search for: user input in system prompts, unsanitized LLM output as HTML (`dangerouslySetInnerHTML`, `v-html`), tool calls without validation, AI API keys in code, `eval()`/`exec()` of AI responses. CRITICAL for user input in system prompts. HIGH for missing tool call validation.

## Phase 9: Skill Supply Chain

Scan installed skills for: `curl`/`wget`/`fetch` (exfiltration), `process.env` (credential access), `IGNORE PREVIOUS`/`disregard` (prompt injection). CRITICAL for credential exfiltration in skill files.

## Phase 10: OWASP Top 10

Targeted Grep analysis per category. Scope to detected stack.

- **A01 Broken Access Control:** Missing auth, direct object references, privilege escalation
- **A02 Cryptographic Failures:** Weak crypto (MD5, SHA1), hardcoded secrets
- **A03 Injection:** SQL, command, template injection
- **A04 Insecure Design:** Missing rate limits on auth, no account lockout
- **A05 Security Misconfiguration:** CORS wildcard origins, missing CSP, debug in prod
- **A07 Auth Failures:** Session management, JWT expiration, MFA
- **A09 Logging:** Auth events logged? Admin actions audit-trailed?
- **A10 SSRF:** User-controlled URLs, internal service reachability

A06 = Phase 4, A08 = Phase 5.

## Phase 11: STRIDE Threat Model

For each major component, assess: Spoofing, Tampering, Repudiation, Information Disclosure, DoS, Elevation of Privilege.

## Phase 12: Data Classification

Identify what data the system handles and where it flows. Use Grep to search for PII patterns (SSN, credit card, email), health data, credentials, API keys. Map data flows: where does sensitive data enter, where is it stored, where does it exit (APIs, logs, third-party services)?

Flag: sensitive data in logs, PII in URLs/query params, unencrypted data at rest, data sent to third parties without disclosure. CRITICAL for exposed PII or credentials. HIGH for missing encryption at rest.

## Phase 13: False Positive Filtering

Run every candidate through this filter. **Daily mode:** 8/10 confidence. **Comprehensive:** 2/10, flag as `TENTATIVE`.

### 22 Hard Exclusions — Auto-Discard

1. DoS/rate limiting (EXCEPT LLM cost amplification)
2. Secrets on disk if encrypted/permissioned
3. Memory/CPU/resource exhaustion
4. Input validation on non-security-critical fields
5. GitHub Action issues unless triggerable via untrusted input (EXCEPT Phase 4)
6. Missing hardening (EXCEPT unpinned actions, missing CODEOWNERS)
7. Race conditions/timing attacks unless concretely exploitable
8. Vulnerabilities in outdated libs (Phase 4 handles this)
9. Memory safety in safe languages (Rust, Go, Java, C#)
10. Unit test/test fixture files only
11. Log spoofing, missing audit logs
12. SSRF where attacker only controls path
13. User content in user-message position (NOT prompt injection)
14. Regex on non-untrusted input
15. Security concerns in docs (EXCEPT SKILL.md)
16. Insecure randomness in non-security contexts
17. Git secrets committed AND removed in same initial-setup PR
18. CVEs with CVSS < 4.0 and no known exploit
19. Docker issues in dev-only Dockerfiles
20. CI findings on archived/disabled workflows
21. Taku's own skill files (trusted source)
22. Any finding without a concrete exploit scenario

### 12 Precedents

1. Logging secrets = vulnerability. Logging URLs = safe.
2. UUIDs are unguessable. Don't flag.
3. Env vars and CLI flags = trusted input.
4. React/Angular XSS-safe by default. Only flag escape hatches.
5. Client-side JS doesn't need auth.
6. Shell injection needs concrete untrusted input path.
7. Subtle web vulns only at extreme confidence.
8. iPython notebooks: only flag if untrusted input triggers it.
9. Logging non-PII = not a vulnerability.
10. Lockfile not tracked IS a finding for apps, NOT libraries.
11. `pull_request_target` without PR ref checkout = safe.
12. Root containers in docker-compose for local dev = not a finding.

### Active Verification

For each surviving finding: check key format (secrets), trace handler code (webhooks), check if vulnerable function is imported (deps). DO NOT test secrets against live APIs. DO NOT make HTTP requests. Mark: `VERIFIED` / `UNVERIFIED` / `TENTATIVE`.

## Phase 14: Report

Every finding MUST include a concrete exploit scenario.

```
#  Sev    Conf   Status      Category       Finding
1  CRIT   9/10   VERIFIED    Secrets        AWS key in git history
2  HIGH   8/10   VERIFIED    CI/CD          pull_request_target+checkout
```

Per-finding format: severity, confidence, status, description, exploit scenario, impact, recommendation.

### Trend Tracking

If prior reports exist in `.taku/security/`: show resolved, persistent, new counts and trend direction (IMPROVING/DEGRADING/STABLE).

### Save

```bash
mkdir -p .taku/security
```

Write `.taku/security/{date}-{HHMMSS}.json` with: version, date, mode, findings array, filter_stats, totals, trend. Include disclaimer: "AI-assisted scan, not a professional security audit. For production systems handling sensitive data, hire a professional penetration testing firm."
