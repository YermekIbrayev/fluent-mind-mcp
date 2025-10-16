# CI/CD and Automation

**Version**: 1.0.0 | **Part of**: [Constitution](INDEX.md)

**Related**: [Governance](governance.md), [Quality Gates](principles/05-quality-gates.md)

---

## Pre-Commit Hooks

Run locally before each commit:

### Security
- Semgrep MCP security scan
- No high/critical vulnerabilities

### Code Quality
- Linting (flake8, pylint, etc.)
- Type checking (mypy, etc.)
- Format checking (black, prettier, etc.)

### Tests
- Run affected unit tests
- Fast tests only (<1 second)

---

## CI/CD Pipeline

Run on every push/PR:

### 1. Security Checks
- Semgrep MCP full scan
- Dependency vulnerability scan (Dependabot)
- Secret detection

### 2. Test Suite
- Full unit test suite
- Integration tests
- Coverage report
- Coverage threshold: ≥80% for Production Code

### 3. Code Quality
- IDE MCP diagnostics
- Cyclomatic complexity check (≤10)
- Duplicate code detection
- Code smell detection

### 4. Documentation
- Link validation
- README completeness check
- API documentation generation
- Changelog verification

### 5. Build & Package
- Build artifacts
- Run smoke tests
- Package for deployment

---

## Code Review Process

### Checklist

**Constitution Compliance**:
- [ ] Code follows constitution principles
- [ ] Correct work type identified (Production/Infrastructure/Experimental)
- [ ] Quality gates passed for work type

**TDD (if Production Code)**:
- [ ] Tests exist and pass
- [ ] Coverage ≥80% overall, 100% Critical Path
- [ ] Tests follow established patterns or approved

**Security**:
- [ ] Semgrep MCP scan clean (no high/critical)
- [ ] No secrets in code
- [ ] Input validation present
- [ ] Authentication/authorization correct

**Documentation**:
- [ ] README updated (if new directory)
- [ ] API docs updated (if public API)
- [ ] ADR created (if architectural decision)
- [ ] Comments explain "why" not "what"

**Code Quality**:
- [ ] Complexity ≤10 per function
- [ ] No code duplication
- [ ] Clear naming conventions
- [ ] File size ≤200 lines

### Approval Requirements

**Solo Developer**: Self-review + Vibe-Check MCP

**Small Team (2-5)**: 1 approver

**Large Team (6+)**: 2+ approvers

**See**: [Team Adaptations](team-adaptations.md)

---

## Token Metrics (Track Weekly)

### File Metrics
- Average lines per file
- Files exceeding 200 lines
- Files exceeding 150 lines (warning)

### Architecture Metrics
- Vertical slice adoption %
- Circular dependency count
- Cross-feature dependencies

### AI Efficiency Metrics
- Token consumption per feature
- Context loading time
- AI suggestion acceptance rate

### Quality Metrics
- Test coverage %
- Security vulnerabilities by severity
- Technical debt ratio

---

## Automated Deployment

### Staging Environment
- Automatic deployment on merge to `develop`
- Smoke tests after deployment
- Performance monitoring

### Production Environment
- Manual approval required
- Blue-green deployment
- Automatic rollback on failure
- Post-deployment verification

---

## Monitoring & Alerts

### Performance
- Response time P95, P99
- Error rate
- Resource utilization

### Security
- Vulnerability alerts (Dependabot)
- Security scan results
- Authentication failures

### Quality
- Test coverage trends
- Technical debt accumulation
- CI/CD pipeline health

---

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: feat, fix, docs, refactor, test, chore

**Example**:
```
feat(auth): add JWT token refresh

Implement automatic token refresh before expiration.
Reduces user re-authentication frequency.

Closes #123
```

---

**See Also**:
- [Principle V: Quality Gates](principles/05-quality-gates.md) - Gate details
- [Governance](governance.md) - Enforcement mechanisms
- [Team Adaptations](team-adaptations.md) - Review requirements
