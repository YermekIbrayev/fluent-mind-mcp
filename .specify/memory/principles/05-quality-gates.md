# Principle V: Security and Quality Gates

**Version**: 1.0.0 | **Part of**: [Constitution](../INDEX.md) > Core Principles

**Related**: [TDD](02-tdd.md), [Governance](../governance.md), [CI/CD](../cicd.md)

---

## Mandate

Before committing Production Code, all applicable gates must pass.

---

## 5.1 Security Scanning (Semgrep MCP)

| Severity | CVSS Score | Action | Timeline |
|----------|-----------|---------|----------|
| **Critical** | 9.0-10.0 | Block all commits immediately | Fix before any other work |
| **High** | 7.0-8.9 | Block commits in affected areas | Must fix within 7 days |
| **Medium** | 4.0-6.9 | Create GitHub issue, label `security-medium` | Address within 30 days |
| **Low** | 0.1-3.9 | Create GitHub issue, label `security-low` | Review quarterly |

---

## 5.2 Test Coverage Requirements

- Production Code: ≥80% overall coverage
- Critical Paths: 100% coverage (no exceptions)
- Integration Tests: <5s per test
- Unit Tests: <100ms per test
- All tests must pass (no flaky tests)
- Tests must be isolated (no shared state)

---

## 5.3 Code Quality Metrics

- IDE MCP Diagnostics: No type errors, syntax errors, unused imports
- Cyclomatic complexity: ≤10 per function
- Nesting depth: ≤3 levels
- Function length: ≤50 lines (guideline)
- Code duplication: No duplicates >6 lines
- Vibe-Check validation for new patterns

---

## 5.4 Quality Gates by Work Type

### Production Code (All Gates Required)
1. ✓ Semgrep MCP Security Scan - No high/critical vulnerabilities
2. ✓ IDE MCP Diagnostics - All checks pass
3. ✓ Test Suite (TDD Green) - All tests pass, coverage ≥80%
4. ✓ Vibe-Check MCP Validation - For new patterns/approaches
5. ✓ Code Quality Metrics - Complexity ≤10, no duplication
6. ✓ Documentation - Per decision tree (Principle VII)
7. ✓ Test Coverage - ≥80% overall, 100% Critical Path

### Infrastructure Code (Relaxed Gates)
1. ✓ Semgrep MCP Security Scan - High/critical only
2. ✓ IDE MCP Diagnostics - All checks pass
3. ⚠️ Tests - Recommended (validate configs, test scripts)
4. ⚠️ Links - Must be valid (if documentation)

### Experimental Code (Minimal Gates)
- No gates required during experimentation
- Must document learnings to Pieces MCP before closing
- Cannot merge to main without meeting Production Code standards

---

**See Also**:
- [Principle II: TDD](02-tdd.md) - Test requirements
- [Governance: Enforcement](../governance.md) - Gate enforcement details
- [CI/CD](../cicd.md) - Automated checks
